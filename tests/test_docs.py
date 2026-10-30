"""Doc↔tool consistency: the checks that must never drift silently.

Machine version of `doctrine/Vault Extension.md` §自检 — they run in CI via
pytest, so a doc that contradicts `rules.py` or `vault.toml` fails the build
instead of waiting for someone to notice months later. The commit-level half of
the sync map is `vault.py docs-check`.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

from conftest import REPO, run_vault
from vaultkit import cli, config, rules

# Files that carry a copy of the rule list / wording (the T2 sync row).
COMPLETE = (
    REPO / "README.md",
    REPO / "AGENTS.md",
    REPO / "doctrine/Vault Design.md",
    REPO / "doctrine/Agent Contract.md",
    REPO / "a_sticker/or/记忆底座-首批卡片.md",
)
RULE_DOCS = COMPLETE + (
    REPO / "doctrine/Vault Extension.md",
    REPO / "tools/vaultkit/cli.py",
)
DOCTRINE = tuple(sorted((REPO / "doctrine").glob("*.md")))
SKILL = REPO / ".agent/skills/vault-ops/SKILL.md"

TOKEN = re.compile(r"(?<![A-Za-z0-9_])([GI]\d+[a-c]?)(?![0-9A-Za-z_])")
RANGE = re.compile(r"(?<![A-Za-z0-9_])([GI]\d+[a-c]?)\s*[–—-]\s*([GI]\d+[a-c]?)(?![0-9A-Za-z_])")
# Threshold values live once, in tools/vault.toml. Docs may cite the *key* only.
THRESHOLD_COPY = re.compile(r"(^|[^0-9])90([^0-9]|$)|0\.97|(^|[^0-9])0\.9([^0-9]|$)")
SYNC_ROW_REF = re.compile(r"\bT\d+\b")


def prose(path: Path) -> str:
    """File text minus fenced code blocks (an example is not a claim)."""
    out, fence = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            fence = None if fence else "```"
            continue
        if fence is None:
            out.append(line)
    return "\n".join(out)


def _named(path: Path) -> str:
    return path.name


@pytest.fixture()
def sync_cfg():
    return config.load(root=REPO)


# ---------------------------------------------------------------- doc content


@pytest.mark.parametrize("path", COMPLETE, ids=_named)
def test_every_rule_id_is_named_in_the_docs(path):
    """A rule that exists but is not written down anywhere is a hidden rule."""
    text = prose(path)
    missing = [r.id for r in rules.RULES if r.id not in text]
    assert not missing, f"{path.name} does not name {missing}"


@pytest.mark.parametrize("path", RULE_DOCS, ids=_named)
def test_docs_name_no_rule_id_that_does_not_exist(path):
    """Ghost ids (v5 leftovers like `I1`) are how a doc lies about the registry."""
    known = {r.id for r in rules.RULES}
    ghosts = sorted({t for t in TOKEN.findall(prose(path)) if t not in known})
    assert not ghosts, f"{path.name} names unknown rule ids: {ghosts}"


@pytest.mark.parametrize("path", RULE_DOCS, ids=_named)
def test_docs_write_no_rule_id_ranges(path):
    """`I1–I4` style ranges cannot be checked for membership and go stale first."""
    assert not RANGE.findall(prose(path)), f"{path.name} writes a rule-id range"


@pytest.mark.parametrize("path", sorted(set(RULE_DOCS) | set(DOCTRINE) | {SKILL}), ids=_named)
def test_docs_carry_no_threshold_value_copies(path):
    hits = [f"{i}: {ln.strip()}" for i, ln in enumerate(prose(path).splitlines(), 1)
            if THRESHOLD_COPY.search(ln)]
    assert not hits, f"{path.name} copies a threshold value: {hits}"


# ---------------------------------------------------------------- sync map


def test_sync_map_ids_match_the_handbook_table(sync_cfg):
    """`tools/vault.toml [docs_sync]` and the handbook table must not diverge."""
    table = prose(REPO / "doctrine/Vault Extension.md")
    table_ids = set(re.findall(r"^\|\s*(T\d+)\s*\|", table, re.M))
    assert table_ids == {r["id"] for r in sync_cfg.docs_sync}


def test_sync_map_paths_exist(sync_cfg):
    for rule in sync_cfg.docs_sync:
        targets = [*rule.get("sync", ()), *rule.get("paths", ())]
        for entry in targets:
            assert (REPO / entry.rstrip("/")).exists(), f"{rule['id']}: missing {entry}"


@pytest.mark.parametrize("path", DOCTRINE, ids=_named)
def test_doctrine_files_declare_version_and_sync_group(path, sync_cfg):
    text = path.read_text(encoding="utf-8")
    assert "> 版本：v6（" in text, f"{path.name} has no version header"
    match = re.search(r"^> 同步组：(.+)$", text, re.M)
    assert match, f"{path.name} has no 同步组 header line"
    known = {r["id"] for r in sync_cfg.docs_sync}
    for ref in SYNC_ROW_REF.findall(match.group(1)):
        assert ref in known, f"{path.name} references unknown sync row {ref}"


# ---------------------------------------------------------------- docs_sync core


def _changed(sync_cfg, *, changed=(), added=(), texts=None):
    return cli.collect_docs_sync(sync_cfg, changed=set(changed), added=set(added),
                                 texts=texts or {})


def test_rule_id_change_fires_t2_and_names_the_co_owners(sync_cfg):
    base = 'Rule("G1", "hard", "G1 root", fn)\n'
    out = _changed(sync_cfg, changed={"tools/vaultkit/rules.py"},
                   texts={"tools/vaultkit/rules.py": (base, base + 'Rule("Z9", "report", "Z9", fn)\n')})
    assert [f["id"] for f in out["findings"]] == ["T2"]
    assert "README.md" in out["findings"][0]["missing"]


def test_comment_only_rule_edit_fires_nothing(sync_cfg):
    """The gate must not go chronically red: an id set that did not change is quiet."""
    base = 'Rule("G1", "hard", "G1 root", fn)\n'
    out = _changed(sync_cfg, changed={"tools/vaultkit/rules.py"},
                   texts={"tools/vaultkit/rules.py": (base, "# a note\n" + base)})
    assert out["findings"] == []


def test_t2_is_satisfied_once_every_co_owner_moves(sync_cfg):
    base = 'Rule("G1", "hard", "G1 root", fn)\n'
    co_owners = {"tools/vaultkit/rules.py", "README.md", "AGENTS.md",
                 "doctrine/Agent Contract.md", "doctrine/Vault Design.md",
                 "tools/vaultkit/cli.py", "a_sticker/or/记忆底座-首批卡片.md",
                 "tests/test_docs.py"}
    out = _changed(sync_cfg, changed=co_owners,
                   texts={"tools/vaultkit/rules.py": (base, base + 'Rule("Z9", "report", "Z9", fn)\n')})
    assert out["findings"] == []


def test_new_doctrine_file_fires_t11(sync_cfg):
    out = _changed(sync_cfg, added={"doctrine/Whatever.md"})
    assert [f["id"] for f in out["findings"]] == ["T11"]


def test_editing_an_existing_doctrine_file_fires_nothing(sync_cfg):
    """T11 is about *new* files; edits are the semantic rows (manual, T9)."""
    assert _changed(sync_cfg, changed={"doctrine/Vault Design.md"})["findings"] == []


def test_rows_without_a_probe_are_reported_as_manual(sync_cfg):
    out = _changed(sync_cfg)
    assert out["findings"] == []
    assert {m["id"] for m in out["manual"]} == {"T3", "T6", "T7", "T8", "T9", "T10"}


def test_t1_never_produces_a_finding(sync_cfg):
    """tools/vault.toml is the single home — changing it requires no doc touch."""
    assert _changed(sync_cfg, changed={"tools/vault.toml"})["findings"] == []


# ---------------------------------------------------------------- docs-check CLI


def _git_repo(tmp_path: Path, rules_src: str) -> Path:
    root = tmp_path / "repo"
    (root / "tools" / "vaultkit").mkdir(parents=True)
    (root / "tools" / "vaultkit" / "rules.py").write_text(rules_src, encoding="utf-8")
    (root / "README.md").write_text("# readme\n", encoding="utf-8")
    run = ["git", "-C", str(root)]
    subprocess.run([*run, "init", "-q"], check=True, capture_output=True)
    subprocess.run([*run, "add", "-A"], check=True, capture_output=True)
    subprocess.run([*run, "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-qm", "seed"], check=True, capture_output=True)
    return root


def test_docs_check_reports_by_default_and_gates_with_the_flag(tmp_path):
    root = _git_repo(tmp_path, 'Rule("G1", "hard", "G1 root", fn)\n')
    (root / "tools" / "vaultkit" / "rules.py").write_text(
        'Rule("G1", "hard", "G1 root", fn)\nRule("Z9", "report", "Z9 假", fn)\n',
        encoding="utf-8")

    proc = run_vault(root, "docs-check")
    assert proc.returncode == 0, "report-level by default: never blocks"
    assert "## T2 fired" in proc.stdout
    assert "  - README.md" in proc.stdout
    assert "report-level, exit 0" in proc.stdout

    proc = run_vault(root, "docs-check", "--gate")
    assert proc.returncode == 1
    assert "exit 1 (--gate)" in proc.stdout


def test_docs_check_is_quiet_on_a_synced_tree(tmp_path):
    root = _git_repo(tmp_path, 'Rule("G1", "hard", "G1 root", fn)\n')
    (root / "README.md").write_text("# readme\n\nupdated\n", encoding="utf-8")
    proc = run_vault(root, "docs-check", "--gate")
    assert proc.returncode == 0
    assert "OK — every triggered sync row carries its co-owners" in proc.stdout
