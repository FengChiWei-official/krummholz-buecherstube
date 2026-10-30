"""place: where a note sits in the relation graph (read-only).

One call must answer "where does this belong, and what should it link first" —
with the evidence named, never a bare list.
"""

from __future__ import annotations

import json

from conftest import run_vault


def test_registered_node_reports_edges_position_and_candidates(vault):
    proc = run_vault(vault, "place", "Node A")
    assert proc.returncode == 0
    assert "在库: library/A_fold/Node A.md" in proc.stdout
    assert "角色: node | 体裁 node | 分区 A_fold" in proc.stdout
    assert "登记于 1 条边: Raw Index of Alpha" in proc.stdout
    assert "归队提议" in proc.stdout and "via " in proc.stdout
    assert "✓ 已登记" in proc.stdout
    assert "语义区域: Alpha-MOC, Index of Alpha Area" in proc.stdout
    assert "出链 1: ['Node B']" in proc.stdout
    assert "先链这几篇" in proc.stdout and "—" in proc.stdout


def test_unregistered_node_reports_the_queue_and_signals(vault):
    proc = run_vault(vault, "place", "Node Zero")
    assert proc.returncode == 0
    assert "登记: (queue — 未登记)" in proc.stdout
    assert "未登记（I1a）" in proc.stdout
    assert "零出链（I3）" in proc.stdout


def test_alias_resolves_and_is_named(vault):
    proc = run_vault(vault, "place", "别名A")
    assert proc.returncode == 0
    assert "# vault place — Node A" in proc.stdout
    assert "经别名 `别名A` 命中" in proc.stdout


def test_unknown_name_exits_1_with_a_did_you_mean_and_no_fake_position(vault):
    proc = run_vault(vault, "place", "Node Sha")
    assert proc.returncode == 1
    assert "库里没有这个名字" in proc.stdout
    assert "did you mean: Node Shared" in proc.stdout
    proc = run_vault(vault, "place", "Zzz Nothing")
    assert proc.returncode == 1
    assert "did you mean" not in proc.stdout


def test_raw_index_reports_cycle_and_parents(vault):
    proc = run_vault(vault, "place", "Raw Index of Beta")
    assert proc.returncode == 0
    assert "角色: raw" in proc.stdout
    assert "被登记为子主干: Raw Index of Alpha" in proc.stdout


def test_place_is_read_only(vault):
    before = {p: p.read_text(encoding="utf-8") for p in vault.rglob("*.md")}
    run_vault(vault, "place", "Node A")
    assert {p: p.read_text(encoding="utf-8") for p in vault.rglob("*.md")} == before


def test_json_payload(vault):
    data = json.loads(run_vault(vault, "place", "Node A", "--json").stdout)
    assert data["command"] == "place" and data["found"] is True
    assert data["stem"] == "Node A" and data["role"] == "node"
    assert data["registered"] == ["Raw Index of Alpha"]
    assert data["areas"] == ["Alpha-MOC", "Index of Alpha Area"]
    assert data["outlinks"] == ["Node B"]
    assert {"raw", "votes", "of", "score", "via"} <= set(data["proposals"][0])
    assert data["proposals"][0]["via"]  # the voters are always named
    assert data["link_candidates"][0]["why"]
    assert isinstance(data["signals"], list)


def test_json_unknown_name(vault):
    proc = run_vault(vault, "place", "Nope", "--json")
    assert proc.returncode == 1
    data = json.loads(proc.stdout)
    assert data["found"] is False and data["note"]
