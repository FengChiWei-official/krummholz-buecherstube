"""CLI tests: run the real entry point against a throwaway fixture vault."""

from __future__ import annotations

from conftest import run_vault

MATERIAL = "archives/material/No Source Lit.md"


def test_check_fails_on_missing_source(vault):
    proc = run_vault(vault, "check")
    assert proc.returncode == 1
    assert f"{MATERIAL}: no real source:" in proc.stdout
    assert "PROBLEMS: 1 (hard gates failed)" in proc.stdout


def test_check_clean_once_source_is_recorded(vault):
    path = vault / MATERIAL
    path.write_text("---\naliases: []\nsource: 某处\n---\n\n# No Source Lit\n\nbody\n",
                    encoding="utf-8")
    proc = run_vault(vault, "check")
    assert proc.returncode == 0
    assert "CLEAN — hard gates hold" in proc.stdout
    assert "no real source" not in proc.stdout


def test_check_flags_new_unresolved_link(vault):
    (vault / "library" / "A_fold" / "Dangling.md").write_text(
        "# Dangling\n\n- [[Nothing Here]]\n", encoding="utf-8")
    proc = run_vault(vault, "check")
    assert proc.returncode == 1
    assert "unresolved [[Nothing Here]]" in proc.stdout


def test_check_flags_root_file(vault):
    (vault / "Loose.md").write_text("# Loose\n", encoding="utf-8")
    proc = run_vault(vault, "check")
    assert proc.returncode == 1
    assert "Loose.md: file me (root is the entry queue)" in proc.stdout


def test_check_reports_trunk_numbers(vault):
    proc = run_vault(vault, "check")
    assert "未登记: 2  (queue — see rawindex L0)" in proc.stdout
    assert "多重登记: Node Shared -> ['Raw Index of Alpha', 'Raw Index of Beta']" in proc.stdout
    assert "零出链: 2/5 (40%)" in proc.stdout
    assert "绑定邻居排除 doctrine(1) 与 Raw(3)" in proc.stdout


def test_triage_categories_and_dead_todo(vault):
    # `Index of Todos.md` itself is exempt from the dead-reference scan, so seed
    # the finished reference in a normal todo note.
    (vault / "a_sticker" / "todos" / "Scratch Todo.md").write_text(
        "# Scratch Todo (fixture)\n\n- [x] [[Gone Note]] — finished\n", encoding="utf-8")
    proc = run_vault(vault, "triage")
    assert proc.returncode == 0
    assert "# root: 0" in proc.stdout
    assert "# dead_todo: 1" in proc.stdout
    assert "dead todo reference: Scratch Todo.md:3: [[Gone Note]]" in proc.stdout


def test_status_renders_all_sections(vault):
    proc = run_vault(vault, "status")
    assert proc.returncode == 0
    for heading in ("## 节律", "## git", "## check (two-tier summary)", "## triage (counts)",
                    "## 主干 (trunk)", "## zzz_output", "## next moves"):
        assert heading in proc.stdout
    assert "nodes 5 | Raw Index 3 | Index 3 | Links 1" in proc.stdout
    assert "queue (未登记): 2" in proc.stdout


def test_rawindex_around_known_node(vault):
    proc = run_vault(vault, "rawindex", "--around", "Node Shared")
    assert proc.returncode == 0
    assert "## Node Shared" in proc.stdout
    assert "登记: ['Raw Index of Alpha', 'Raw Index of Beta']" in proc.stdout
    assert "区域: ['Index of Alpha Area']" in proc.stdout


def test_rawindex_around_unknown_exits_1(vault):
    proc = run_vault(vault, "rawindex", "--around", "No Such Note")
    assert proc.returncode == 1
    assert "not found." in proc.stdout


def test_rawindex_check_renders_the_rule_registry(vault):
    proc = run_vault(vault, "rawindex", "--check")
    assert proc.returncode == 0
    assert "## I1a 每个 Node 至少登记在一个 Raw Index" in proc.stdout
    assert "未登记: 2  (queue — see rawindex L0)" in proc.stdout
    assert "## I1b 重复登记边（同一 (Raw Index, Node) 出现两次）" in proc.stdout
    assert "重复登记边: 0   多重登记: 1" in proc.stdout
    assert "## I1c Raw Index 子图无环" in proc.stdout
    assert "Raw Index 环: 0  (登记边构成的子图无环)" in proc.stdout
    assert "零出链: 2/5 (40%) — 捕获规则增量,不阻断 (B5)" in proc.stdout
    assert "## 材料 出链=已拆 (D21)" in proc.stdout
    assert "未拆材料: 1/1  (零出链 = 未拆)" in proc.stdout


def test_check_reports_i1c_cycle_and_i1b_duplicate(vault):
    alpha = vault / "library" / "Raw" / "Raw Index of Alpha.md"
    beta = vault / "library" / "Raw" / "Raw Index of Beta.md"
    alpha.write_text(alpha.read_text(encoding="utf-8") + "- [[Node A]]\n", encoding="utf-8")
    beta.write_text(beta.read_text(encoding="utf-8") + "- [[Raw Index of Alpha]]\n",
                    encoding="utf-8")
    proc = run_vault(vault, "check")
    assert proc.returncode == 1                      # only the seeded G2 gate
    assert "PROBLEMS: 1 (hard gates failed)" in proc.stdout
    assert "重复登记边: 1   多重登记: 1" in proc.stdout
    assert "重复边: Raw Index of Alpha -> Node A ×2" in proc.stdout
    assert "Raw Index 环: 2 个 Raw Index 落在环上" in proc.stdout
    assert "环上: Raw Index of Alpha" in proc.stdout
    assert "环上: Raw Index of Beta" in proc.stdout


def test_g3_scope_line_is_stated(vault):
    proc = run_vault(vault, "check")
    assert "扫描范围: 除 .agent、.git、.obsidian 之外的全部 *.md" in proc.stdout
    assert "笔记载入另跳过 template、zzz_output" in proc.stdout


def test_new_rule_renders_in_check_and_rawindex_check(vault, monkeypatch, capsys):
    """Adding a rule = appending one Rule; both renderers pick it up."""
    from vaultkit import cli, rules

    def fake_rule(ctx):
        return ["假规则: 1"]

    fake = rules.Rule("Z9", "report", "Z9 假规则 (report)", fake_rule,
                      short="Z9 假规则（rawindex 视图）")
    monkeypatch.setattr(rules, "RULES", [*rules.RULES, fake])
    monkeypatch.setenv("VAULT_ROOT", str(vault))

    assert cli.main(["check"]) == 1                  # the fixture's seeded G2 gate
    out = capsys.readouterr().out
    assert "## Z9 假规则 (report)" in out
    assert "假规则: 1" in out

    assert cli.main(["rawindex", "--check"]) == 0
    out = capsys.readouterr().out
    assert "## Z9 假规则（rawindex 视图）" in out
    assert "假规则: 1" in out


def test_sync_is_dry_run_without_apply(vault):
    before = (vault / "library" / "Raw" / "Raw Index of Everything.md").read_text(encoding="utf-8")
    proc = run_vault(vault, "rawindex", "--sync")
    assert proc.returncode == 0
    assert "[dry-run] 将注册 2 个 child Raw Index" in proc.stdout
    assert "- [[Raw Index of Alpha]] (2)" in proc.stdout
    assert (vault / "library" / "Raw" / "Raw Index of Everything.md").read_text(
        encoding="utf-8") == before


def test_sync_apply_writes_member_list(vault):
    proc = run_vault(vault, "rawindex", "--sync", "--apply")
    assert proc.returncode == 0
    assert "已注册 2 个 child Raw Index" in proc.stdout
    text = (vault / "library" / "Raw" / "Raw Index of Everything.md").read_text(encoding="utf-8")
    assert "## Core Concepts\n\n- [[Raw Index of Alpha]] (2)\n- [[Raw Index of Beta]] (2)\n" in text
    # idempotent: a second apply changes nothing
    again = run_vault(vault, "rawindex", "--sync", "--apply")
    assert again.returncode == 0
    assert (vault / "library" / "Raw" / "Raw Index of Everything.md").read_text(
        encoding="utf-8") == text


def test_strict_exits_2_on_missing_list_file(vault):
    lenient = run_vault(vault, "check")
    assert lenient.returncode == 1                      # only the seeded G2 violation
    assert "WARNING: missing config" in lenient.stderr

    strict = run_vault(vault, "check", "--strict")
    assert strict.returncode == 2
    assert "ERROR: missing config" in strict.stdout
    assert "whitelist_unresolved.txt" in strict.stdout


def test_status_renders_dash_when_nothing_to_measure(vault):
    proc = run_vault(vault, "status")
    assert proc.returncode == 0
    assert "- 上次产出: —" in proc.stdout
    assert "- 上次聚簇: 今天" in proc.stdout
