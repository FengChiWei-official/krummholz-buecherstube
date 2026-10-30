"""rename: cascade every inbound wikilink, and refuse the cases that would lie.

Wikilinks resolve by note NAME, so a rename without a cascade silently breaks
every inbound link. These tests pin both halves: the rewrite forms, and the
refusals/warnings that keep the operation honest.
"""

from __future__ import annotations

import json

import pytest

from conftest import run_vault
from vaultkit import parse

FORMS = [
    ("[[Old]]", "[[New]]", 1),
    ("[[Old|显示名]]", "[[New|显示名]]", 1),                  # alias is display text
    ("[[Old#标题]]", "[[New#标题]]", 1),                      # anchor kept
    ("[[Old#标题|别名]]", "[[New#标题|别名]]", 1),
    ("![[Old]]", "![[New]]", 1),                              # embed
    ("[[library/A_fold/Old]]", "[[library/A_fold/New]]", 1),  # path prefix kept
    ("[[library/A_fold/Old|x]]", "[[library/A_fold/New|x]]", 1),
    ("[[Old.md]]", "[[New.md]]", 1),                          # Obsidian's .md form
    ("[[OldName]]", "[[OldName]]", 0),                        # substring safety
    ("[[Oldest]]", "[[Oldest]]", 0),
    ("[[Other|Old]]", "[[Other|Old]]", 0),                    # alias is not a target
    ("[[ Old ]]", "[[ New ]]", 1),                            # surrounding space kept
    ("```\n[[Old]]\n```", "```\n[[Old]]\n```", 0),            # fence: not a link
    ("`[[Old]]`", "`[[Old]]`", 0),                            # inline code: not a link
    ("[[Old]] 与 [[Old|x]]", "[[New]] 与 [[New|x]]", 2),
]

FORM_IDS = [source for source, _, _ in FORMS]


@pytest.mark.parametrize("source,expected,count", FORMS, ids=FORM_IDS)
def test_rename_links_forms(source, expected, count):
    got, replacements = parse.rename_links(source, "Old", "New")
    assert got == expected
    assert replacements == count


def test_rename_links_agrees_with_the_resolver_on_what_a_link_is():
    """A fenced `[[Old]]` is not an edge for the graph, so it is not rewritten."""
    text = "[[Old]]\n\n```\n[[Old]]\n```\n"
    assert parse.rename_links(text, "Old", "New")[1] == 1
    assert [n for n, _ in parse.extract_wikilinks(text)].count("Old") == 1


# ---------------------------------------------------------------- CLI


def _g3_section(stdout: str) -> str:
    return stdout.split("## G3", 1)[1].split("\n## ", 1)[0] if "## G3" in stdout else ""


def test_dry_run_writes_nothing(vault):
    proc = run_vault(vault, "rename", "Node A", "Node A2")
    assert proc.returncode == 0
    assert "[dry-run]" in proc.stdout
    assert "（不改文件；确认后加 --apply 落地）" in proc.stdout
    assert (vault / "library/A_fold/Node A.md").exists()
    assert "[[Node A]]" in (vault / "library/Raw/Raw Index of Alpha.md").read_text(encoding="utf-8")


def test_apply_moves_the_file_and_cascades_every_link(vault):
    proc = run_vault(vault, "rename", "Node A", "Node A2", "--apply")
    assert proc.returncode == 0
    assert "复检剩余 0" in proc.stdout
    assert not (vault / "library/A_fold/Node A.md").exists()
    assert (vault / "library/A_fold/Node A2.md").exists()
    for rel in ("library/Raw/Raw Index of Alpha.md", "library/Index/Alpha-MOC.md",
                "library/Links/Links of A and B.md", "doctrine/Vault Design.md"):
        assert "[[Node A2]]" in (vault / rel).read_text(encoding="utf-8")


def test_apply_keeps_the_hard_gate_green(vault):
    """The point of the cascade: G3 must not gain a dangling link."""
    before = run_vault(vault, "check")
    assert "OK — no violations" in _g3_section(before.stdout)
    run_vault(vault, "rename", "Node A", "Node A2", "--apply")
    after = run_vault(vault, "check")
    assert "OK — no violations" in _g3_section(after.stdout)


def test_fenced_link_is_left_alone(vault):
    run_vault(vault, "rename", "Node A", "Node A2", "--apply")
    fence = (vault / "library/A_fold/Fence Node.md").read_text(encoding="utf-8")
    assert "[[Node A]] inside a fence" in fence


def test_alias_only_links_are_not_rewritten_and_still_resolve(vault):
    """`[[别名A]]` names an alias, not the note — the alias travels with the file."""
    run_vault(vault, "rename", "Node A", "Node A2", "--apply")
    node_b = (vault / "library/B_fold/Node B.md").read_text(encoding="utf-8")
    assert "[[别名A]]" in node_b
    assert "[[Node A2]]" not in node_b


def test_self_link_is_rewritten_too(vault):
    note = vault / "library/A_fold/Node Zero.md"
    note.write_text(note.read_text(encoding="utf-8") + "\n- 自指 [[Node Zero]]\n",
                    encoding="utf-8")
    run_vault(vault, "rename", "Node Zero", "Zero Two", "--apply")
    moved = (vault / "library/A_fold/Zero Two.md").read_text(encoding="utf-8")
    assert "[[Zero Two]]" in moved and "[[Node Zero]]" not in moved


def test_substring_names_are_never_touched(vault):
    """Renaming `Node A` must not corrupt `[[Node A2]]`-style longer names."""
    (vault / "library/A_fold/Node A.md").write_text(
        "# Node A\n\n- [[Node ABC]]\n", encoding="utf-8")
    (vault / "library/A_fold/Node ABC.md").write_text("# Node ABC\n", encoding="utf-8")
    run_vault(vault, "rename", "Node A", "Node A2", "--apply")
    moved = (vault / "library/A_fold/Node A2.md").read_text(encoding="utf-8")
    assert "[[Node ABC]]" in moved
    assert (vault / "library/A_fold/Node ABC.md").exists()


def test_collision_with_an_existing_name_refuses(vault):
    proc = run_vault(vault, "rename", "Node Zero", "Node B")
    assert proc.returncode == 1
    assert "已有同名笔记 `Node B`" in proc.stdout
    assert (vault / "library/A_fold/Node Zero.md").exists()


def test_collision_with_a_case_variant_warns_but_proceeds(vault):
    proc = run_vault(vault, "rename", "Node Zero", "node b")
    assert proc.returncode == 0
    assert "仅大小写不同的同名" in proc.stdout


def test_alias_collision_warns(vault):
    proc = run_vault(vault, "rename", "Node Zero", "别名A")
    assert proc.returncode == 0
    assert "已是另一篇笔记的别名" in proc.stdout


def test_unknown_name_refuses(vault):
    proc = run_vault(vault, "rename", "Nope", "X")
    assert proc.returncode == 1
    assert "没有叫 `Nope` 的笔记" in proc.stdout


def test_ambiguous_stem_refuses(vault):
    (vault / "library/B_fold/Node A.md").write_text("# 另一个 Node A\n", encoding="utf-8")
    proc = run_vault(vault, "rename", "Node A", "Node A2")
    assert proc.returncode == 1
    assert "2 个同名文件" in proc.stdout


def test_path_separator_refuses(vault):
    proc = run_vault(vault, "rename", "Node Zero", "sub/Zero")
    assert proc.returncode == 1
    assert "不能含路径分隔符" in proc.stdout


def test_root_contract_file_refuses(vault):
    proc = run_vault(vault, "rename", "README", "README2")
    assert proc.returncode == 1
    assert "root 契约文件" in proc.stdout


def test_same_name_is_a_no_op(vault):
    proc = run_vault(vault, "rename", "Node Zero", "Node Zero")
    assert proc.returncode == 0
    assert "新旧同名" in proc.stdout


def test_md_suffix_is_stripped(vault):
    proc = run_vault(vault, "rename", "Node Zero", "Zero 2.md")
    assert proc.returncode == 0
    assert "已去掉 `.md` 后缀" in proc.stdout
    assert "library/A_fold/Zero 2.md" in proc.stdout


def test_genre_change_is_called_out(vault):
    proc = run_vault(vault, "rename", "Node A", "Raw Index of Zed")
    assert proc.returncode == 0
    assert "体裁会变：node → raw" in proc.stdout


def test_template_placeholders_are_never_rewritten(vault):
    """`[[NAME]]` in a scaffold is a placeholder, not a link to a note."""
    (vault / "template").mkdir()
    scaffold = vault / "template/todo-temp.md"
    scaffold.write_text("# t\n\n- [ ] [[NAME]] — 续写说明\n", encoding="utf-8")
    (vault / "library/A_fold/NAME.md").write_text("# NAME\n", encoding="utf-8")

    proc = run_vault(vault, "rename", "NAME", "Renamed")
    assert "template/ 另有 1 处引用（未改）" in proc.stdout

    proc = run_vault(vault, "rename", "NAME", "Renamed", "--apply")
    assert proc.returncode == 0
    assert scaffold.read_text(encoding="utf-8") == "# t\n\n- [ ] [[NAME]] — 续写说明\n"
    assert (vault / "library/A_fold/Renamed.md").exists()


def test_unwritable_zzz_output_links_are_reported_but_do_not_block(vault):
    """G3 does not scan zzz_output, so a stale link there cannot turn a gate red."""
    zzz = vault / "zzz_output"
    zzz.mkdir()
    (zzz / "out.md").write_text("terminal output [[Node Zero]]\n", encoding="utf-8")

    proc = run_vault(vault, "rename", "Node Zero", "Zero Two")
    assert proc.returncode == 0
    assert "zzz_output/ 另有 1 处引用" in proc.stdout
    assert "扫不到它们" in proc.stdout

    proc = run_vault(vault, "rename", "Node Zero", "Zero Two", "--apply")
    assert proc.returncode == 0
    assert (vault / "library/A_fold/Zero Two.md").exists()
    assert (zzz / "out.md").read_text(encoding="utf-8") == "terminal output [[Node Zero]]\n"
    assert "OK — no violations" in _g3_section(run_vault(vault, "check").stdout)


def test_renaming_a_note_inside_zzz_output_refuses(vault):
    zzz = vault / "zzz_output"
    zzz.mkdir()
    (zzz / "Out Note.md").write_text("# out\n", encoding="utf-8")
    proc = run_vault(vault, "rename", "Out Note", "Other")
    assert proc.returncode == 1
    assert "owner 区" in proc.stdout


def test_json_payload(vault):
    proc = run_vault(vault, "rename", "Node A", "Node A2", "--json")
    data = json.loads(proc.stdout)
    assert data["old"] == "Node A" and data["new"] == "Node A2"
    assert data["error"] is None and data["applied"] is False
    assert data["refs"] >= 5 and data["files"] >= 5
    assert data["remaining"] is None
    assert any(hit["path"] == "library/Index/Alpha-MOC.md" for hit in data["hits"])


def test_whitelist_and_self_alias_are_reported(vault):
    (vault / "tools").mkdir(exist_ok=True)
    (vault / "tools/whitelist_unresolved.txt").write_text("Node A\n", encoding="utf-8")
    note = vault / "library/A_fold/Node A.md"
    note.write_text(note.read_text(encoding="utf-8").replace("aliases: [别名A]",
                                                            "aliases: [别名A, Node A]"),
                    encoding="utf-8")
    proc = run_vault(vault, "rename", "Node A", "Node A2")
    assert "whitelist_unresolved 里" in proc.stdout
    assert "本文件的 `aliases:` 里仍有" in proc.stdout
