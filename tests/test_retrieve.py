"""retrieve: whole-vault retrieval by evidence strength, with the reason per hit."""

from __future__ import annotations

import json

from conftest import run_vault


def test_name_hits_come_first_and_carry_context(vault):
    proc = run_vault(vault, "retrieve", "Node")
    assert proc.returncode == 0
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip().startswith(("1.", "2.", "3."))]
    assert "[[Fence Node]] — 名字含 `Node`" in lines[0]
    assert "[[Node A]] — 名字含 `Node`" in lines[1]
    assert "登记: Raw Index of Alpha" in proc.stdout
    assert "区域: Alpha-MOC, Index of Alpha Area" in proc.stdout


def test_name_hits_have_no_redundant_snippet(vault):
    data = json.loads(run_vault(vault, "retrieve", "Node", "--json").stdout)
    named = [h for h in data["hits"] if h["score"] >= 3]
    assert named and all(h["snippet"] is None for h in named)


def test_text_hits_show_the_matching_line(vault):
    (vault / "library/A_fold/Node Zero.md").write_text(
        "# Node Zero\n\nthe quantum wobble appears here\n", encoding="utf-8")
    data = json.loads(run_vault(vault, "retrieve", "quantum wobble", "--json").stdout)
    hit = data["hits"][0]
    assert hit["why"] == "正文命中 1 处"
    assert hit["snippet"]["line"] == 3
    assert "quantum wobble" in hit["snippet"]["text"]


def test_alias_hit(vault):
    data = json.loads(run_vault(vault, "retrieve", "别名A", "--json").stdout)
    assert data["hits"][0]["note"] == "Node A"
    assert data["hits"][0]["why"] == "别名含 `别名A`"


def test_structural_evidence_pulls_in_members(vault):
    data = json.loads(run_vault(vault, "retrieve", "Raw Index of Alpha", "--json").stdout)
    whys = {h["note"]: h["why"] for h in data["hits"]}
    assert whys.get("Node Shared") == "登记于 [[Raw Index of Alpha]]"


def test_no_hits_exits_1(vault):
    proc = run_vault(vault, "retrieve", "zzzz")
    assert proc.returncode == 1
    assert "没有命中" in proc.stdout


def test_scope_excludes_zzz_output_and_template(vault):
    """Same scope as G3: a note that is not loaded is not searched."""
    zzz = vault / "zzz_output"
    zzz.mkdir()
    (zzz / "out.md").write_text("unique-token-here\n", encoding="utf-8")
    proc = run_vault(vault, "retrieve", "unique-token-here")
    assert proc.returncode == 1
    assert "zzz_output/ 与 template/ 不参与" in proc.stdout


def test_hits_can_be_capped(vault):
    proc = run_vault(vault, "retrieve", "Node", "--n", "2")
    assert proc.returncode == 0
    assert "命中 13 篇，只列前 2 篇" in proc.stdout


def test_read_only(vault):
    before = {p: p.read_text(encoding="utf-8") for p in vault.rglob("*.md")}
    run_vault(vault, "retrieve", "Node")
    assert {p: p.read_text(encoding="utf-8") for p in vault.rglob("*.md")} == before


def test_json_payload_shape(vault):
    data = json.loads(run_vault(vault, "retrieve", "Node", "--json").stdout)
    assert data["command"] == "retrieve" and data["term"] == "Node"
    assert data["found"] is True and data["scanned"] > 0
    assert {"note", "path", "role", "score", "why", "snippet", "text_hits",
            "registered_by", "areas"} <= set(data["hits"][0])
    assert data["hits"][0]["score"] >= data["hits"][-1]["score"]
