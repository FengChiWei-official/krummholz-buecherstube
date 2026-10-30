"""links-candidates: members for a Links card, grouped by Index area.

Doctrine: a Links card is one concept seen from several angles and must cross ≥2
Index areas. The tool proposes members + evidence; the name and the commonality
sentence stay the owner's (D16).
"""

from __future__ import annotations

import json

from conftest import run_vault


def test_members_are_grouped_by_area_with_evidence(vault):
    proc = run_vault(vault, "links-candidates", "Node")
    assert proc.returncode == 0
    assert "种子（名字/别名命中）: Fence Node, Node A, Node B, Node Shared, Node Zero" in proc.stdout
    assert "覆盖区域 3: Alpha-MOC, Index of Alpha Area, Index of Beta Area" in proc.stdout
    assert "[Index of Alpha Area] 2 篇" in proc.stdout
    assert "[[Node A]] — 名字含 `Node`  ★种子" in proc.stdout
    assert "★种子" in proc.stdout


def test_crossing_areas_is_reported_as_satisfied(vault):
    data = json.loads(run_vault(vault, "links-candidates", "Node", "--json").stdout)
    assert data["crosses_areas"] is True
    assert data["area_count"] >= 2
    assert all(m["why"] for m in data["members"])


def test_one_area_is_called_out_as_not_a_links_card_yet(vault):
    proc = run_vault(vault, "links-candidates", "Fence")
    assert proc.returncode == 0
    assert "只覆盖 0 个 Index 区域" in proc.stdout
    assert "Links 卡必须横跨 ≥2 个区域" in proc.stdout


def test_structural_notes_are_mediators_not_members(vault):
    proc = run_vault(vault, "links-candidates", "Node")
    assert "结构笔记（Raw Index / Index / Links / doctrine）是关系的中介，不是成员" in proc.stdout
    data = json.loads(run_vault(vault, "links-candidates", "Node", "--json").stdout)
    assert all(m["role"] not in ("raw", "index", "links", "doctrine") for m in data["members"])


def test_card_name_candidates_use_content_members(vault):
    data = json.loads(run_vault(vault, "links-candidates", "Node", "--json").stdout)
    assert data["card_name_candidates"][0].startswith("Links of ")
    assert "Raw Index" not in data["card_name_candidates"][0]
    assert "Index of" not in data["card_name_candidates"][0]


def test_no_seed_points_at_retrieve(vault):
    proc = run_vault(vault, "links-candidates", "zzzz")
    assert proc.returncode == 1
    assert "没有名字或别名含 `zzzz` 的笔记" in proc.stdout
    assert "retrieve" in proc.stdout


def test_members_can_be_capped(vault):
    proc = run_vault(vault, "links-candidates", "Node", "--n", "2")
    assert proc.returncode == 0
    assert "只列前 2 篇" in proc.stdout


def test_coverage_is_computed_before_the_cap(vault):
    """A small --n must not shrink the area verdict (found by running the example)."""
    full = json.loads(run_vault(vault, "links-candidates", "Node", "--json").stdout)
    capped = json.loads(run_vault(vault, "links-candidates", "Node", "--n", "2",
                                  "--json").stdout)
    assert capped["area_count"] == full["area_count"] == 3
    assert capped["crosses_areas"] is True
    assert capped["member_total"] == full["member_total"]
    assert len(capped["members"]) == 2
    assert sum(g["member_count"] for g in capped["groups"]) > len(capped["members"])


def test_read_only(vault):
    before = {p: p.read_text(encoding="utf-8") for p in vault.rglob("*.md")}
    run_vault(vault, "links-candidates", "Node")
    assert {p: p.read_text(encoding="utf-8") for p in vault.rglob("*.md")} == before


def test_json_payload_shape(vault):
    data = json.loads(run_vault(vault, "links-candidates", "Node", "--json").stdout)
    assert data["command"] == "links-candidates" and data["topic"] == "Node"
    assert data["found"] is True and data["seeds"]
    assert {"area", "members"} <= set(data["groups"][0])
    assert {"note", "path", "why", "role", "areas", "seed"} <= set(data["members"][0])
