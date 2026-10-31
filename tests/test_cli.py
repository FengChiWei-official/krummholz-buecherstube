"""CLI tests: run the real entry point against a throwaway fixture vault."""

from __future__ import annotations

import os
import signal
import subprocess
import sys

import pytest

from conftest import REPO, TOOLS, run_vault
from vaultkit import config

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
    assert "零出链: 2/5 (40%)" in proc.stdout
    assert "绑定邻居排除 doctrine(1) 与 Raw(3)" in proc.stdout
    # DAG: the fixture's two-parent Node is legal, so no multi-parent line appears.
    assert "多重登记" not in proc.stdout


def test_triage_lists_empty_notes(vault):
    """Zero-byte notes carry no link signal, so they bypass the age window."""
    (vault / "library" / "A_fold" / "Empty Node.md").write_text("", encoding="utf-8")
    proc = run_vault(vault, "triage")
    assert proc.returncode == 0
    assert "# halfdone: 1" in proc.stdout
    assert ("library/A_fold/Empty Node.md — 空笔记（零字节）, 零出链, 无 todo 挂钩 (A1/L21)"
            in proc.stdout)


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


def test_rawindex_no_longer_carries_a_per_note_view(vault):
    """One note's position is `place`; rawindex works the queue as a whole."""
    proc = run_vault(vault, "rawindex", "--around", "Node Shared")
    assert proc.returncode == 2  # argparse: unknown flag, loud not silent
    assert "--around" in proc.stderr


def test_rawindex_check_renders_the_rule_registry(vault):
    proc = run_vault(vault, "rawindex", "--check")
    assert proc.returncode == 0
    assert "## I1a 每个 Node 至少登记在一个 Raw Index" in proc.stdout
    assert "未登记: 2  (queue — see rawindex L0)" in proc.stdout
    assert "## I1b 重复登记边（同一 (Raw Index, Node) 出现两次）" in proc.stdout
    assert "重复登记边: 0" in proc.stdout
    assert "## I1c Raw Index 子图无环" in proc.stdout
    assert "Raw Index 环: 0  (登记边构成的子图无环 — 主干是 DAG,不是树)" in proc.stdout
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
    assert "重复登记边: 1" in proc.stdout
    assert "重复边: Raw Index of Alpha -> Node A ×2" in proc.stdout
    assert "Raw Index 环: 2 个 Raw Index 落在环上" in proc.stdout
    assert "环上: Raw Index of Alpha" in proc.stdout
    assert "环上: Raw Index of Beta" in proc.stdout


def test_g3_scope_line_is_rendered_from_the_config(vault):
    """The scope line must be built from `tools/vault.toml`, never hardcoded."""
    cfg = config.load(root=vault)
    proc = run_vault(vault, "check")
    skip = "、".join(sorted(cfg.skip_dirs))
    extra = "、".join(sorted(cfg.notes_skip_dirs - cfg.skip_dirs))
    assert f"扫描范围: 载入的笔记（除 {skip} 之外的全部 *.md，且不载入 {extra}）" in proc.stdout


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


def test_learning_mechanism_rules(vault):
    """I5–I8 count from 0 and follow the sections the owner adds."""
    idx = vault / "library" / "Index" / "Index of Alpha Area.md"
    idx.write_text(idx.read_text(encoding="utf-8")
                   + "\n## 时间轴\n\n| 世代 | 年份 | 代表 |\n|---|---|---|\n| 一 | 1950 | — |\n"
                   + "\n## 地图\n\n| 挂点 | 合同 |\n|---|---|\n| [[Node A]] | ISA |\n",
                   encoding="utf-8")
    node_b = vault / "library" / "B_fold" / "Node B.md"
    node_b.write_text(node_b.read_text(encoding="utf-8")
                      + "\n## Mapping\n\n| 实例 | 章节 |\n|---|---|\n| [[Node A]] | ch4 |\n",
                      encoding="utf-8")
    node_zero = vault / "library" / "A_fold" / "Node Zero.md"
    node_zero.write_text(node_zero.read_text(encoding="utf-8")
                         + "\n## 实例化\n\n| 实例 | 章节 |\n|---|---|\n",
                         encoding="utf-8")

    proc = run_vault(vault, "check")
    assert "Mapping 不足 2 行的笔记: 1" in proc.stdout
    assert "library/B_fold/Node B.md: ## Mapping 只有 1 行 (<2)" in proc.stdout
    assert "实例化 不足 2 行的笔记: 1" in proc.stdout
    assert "library/A_fold/Node Zero.md: ## 实例化 只有 0 行 (<2)" in proc.stdout
    assert "时间轴 未达标的学科 Index: 1" in proc.stdout
    assert "Index of Alpha Area: ## 时间轴 只有 1 行 (<2)" in proc.stdout
    # I8: Node A is a 地图 anchor, Node Shared reaches it, so coverage is full.
    assert "挂点覆盖率: 2/2 (100%) — 学科 Index 1 个" in proc.stdout
    assert "Index of Alpha Area: 2/2 (100%)" in proc.stdout


def test_learning_rules_are_quiet_without_the_sections(vault):
    proc = run_vault(vault, "check")
    assert "Mapping 不足 2 行的笔记: 0" in proc.stdout
    assert "实例化 不足 2 行的笔记: 0" in proc.stdout
    assert "时间轴 未达标的学科 Index: 0" in proc.stdout
    assert "挂点覆盖率: 0/0 (0%) — 学科 Index 0 个" in proc.stdout

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


def test_status_json_is_self_describing(vault):
    import json

    proc = run_vault(vault, "status", "--json")
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert data["command"] == "status"
    assert data["version"].startswith("6.")
    assert data["state_location"].startswith("a_sticker/todos/")
    assert data["contract"] == "doctrine/Agent Contract.md"
    assert set(data["exit_codes"]) == {"0", "1", "2"}
    assert data["trunk"]["nodes"] == 5
    assert data["triage"]["root"] == 0
    assert isinstance(data["next_moves"], list) and data["next_moves"]


def test_json_on_every_subcommand(vault):
    import json

    for argv in (("check", "--json"), ("triage", "--json"), ("rawindex", "--json")):
        proc = run_vault(vault, *argv)
        data = json.loads(proc.stdout)
        assert data["command"] in ("check", "triage", "rawindex")
        assert data["vault_root"].endswith("mini_vault")


def test_random_is_deterministic_with_a_seed(vault):
    first = run_vault(vault, "random", "--seed", "1")
    again = run_vault(vault, "random", "--seed", "1")
    assert first.returncode == 0
    assert first.stdout == again.stdout
    assert "→ 问箱" in first.stdout

    library = run_vault(vault, "random", "--scope", "library", "--seed", "2")
    assert library.returncode == 0
    assert "scope library" in library.stdout


def test_suggest_lists_candidates_with_why(vault):
    proc = run_vault(vault, "suggest", "Node A", "--n", "3")
    assert proc.returncode == 0
    assert "## suggest Node A" in proc.stdout
    assert "共同邻居" in proc.stdout
    # Node B already links to Node A, so it is not a candidate
    assert "[[Node B]]" not in proc.stdout


def test_suggest_unknown_name_exits_1(vault):
    proc = run_vault(vault, "suggest", "No Such Note")
    assert proc.returncode == 1
    assert "not found." in proc.stdout


def test_help_topics(vault):
    for topic in ("triage", "rawindex", "dag", "links", "random", "suggest"):
        proc = run_vault(vault, "help", topic)
        assert proc.returncode == 0
        assert topic in proc.stdout
    assert run_vault(vault, "help").returncode == 0
    assert run_vault(vault, "help", "nonsense").returncode == 2


def test_a_closed_downstream_pipe_does_not_print_a_traceback(vault):
    """`vault.py retrieve X | head` must end like `cat`, not raise BrokenPipeError."""
    if not hasattr(signal, "SIGPIPE"):
        pytest.skip("SIGPIPE is POSIX-only")
    read_fd, write_fd = os.pipe()
    proc = subprocess.Popen(
        [sys.executable, str(TOOLS / "vault.py"), "retrieve", "Node"],
        stdout=write_fd, stderr=subprocess.PIPE, text=True,
        env=dict(os.environ, VAULT_ROOT=str(vault)), cwd=str(REPO))
    os.close(write_fd)  # the child owns the only write end
    os.close(read_fd)   # ... and nothing is left to read it
    _, err = proc.communicate()
    assert proc.returncode == -signal.SIGPIPE, err
    assert "Traceback" not in err
    assert "BrokenPipeError" not in err
