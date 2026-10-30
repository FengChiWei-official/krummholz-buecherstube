"""index-candidates: a candidate card table for building an Index.

Doctrine (D10-P3): the coarse Raw Index stays coarse — the *clusters* and their
commonality go into the Index. The name and the sentence stay the owner's (D16).
"""

from __future__ import annotations

import json

from conftest import run_vault


def test_candidate_card_table(vault):
    proc = run_vault(vault, "index-candidates", "Raw Index of Alpha")
    assert proc.returncode == 0
    assert "主干: Raw Index of Alpha  (library/Raw/Raw Index of Alpha.md)" in proc.stdout
    assert "登记成员 2 篇" in proc.stdout
    assert "| 簇 | 成员 | 共同证据 | 共性句候选（草稿） | 建议 Index 名 |" in proc.stdout
    assert "Node A / Node Shared" in proc.stdout
    assert "绑定证据 = 共同邻居" in proc.stdout


def test_one_cluster_is_not_an_index_yet(vault):
    proc = run_vault(vault, "index-candidates", "Raw Index of Alpha")
    assert "只有一个簇——一个簇还撑不起一个 Index" in proc.stdout


def test_covering_links_cards_are_flagged_as_seeds(vault):
    """A Links card spanning ≥2 of the Raw Index's members is an Index seed."""
    links = vault / "library/Links/Links of A and B.md"
    links.write_text(links.read_text(encoding="utf-8") + "- [[Node Shared]]\n", encoding="utf-8")
    proc = run_vault(vault, "index-candidates", "Raw Index of Alpha")
    assert proc.returncode == 0
    assert "已有 Links 卡覆盖 ≥2 个成员: Links of A and B" in proc.stdout
    assert "Links 卡 Links of A and B（2 成员）" in proc.stdout
    assert "Links 卡是 Index 的天然种子" in proc.stdout


def test_non_raw_index_refuses(vault):
    proc = run_vault(vault, "index-candidates", "Node A")
    assert proc.returncode == 1
    assert "不是 Raw Index" in proc.stdout
    assert "Index 由主干成员长出来" in proc.stdout


def test_unknown_name(vault):
    proc = run_vault(vault, "index-candidates", "Raw Index of Zz")
    assert proc.returncode == 1
    assert "没有叫 `Raw Index of Zz` 的笔记" in proc.stdout


def test_d16_and_d10_reminders_are_always_printed(vault):
    proc = run_vault(vault, "index-candidates", "Raw Index of Alpha")
    assert "共性句与 Index 名由你写（D16）" in proc.stdout
    assert "绝不每簇一个 Index（D10-P3）" in proc.stdout


def test_clusters_can_be_capped(vault):
    proc = run_vault(vault, "index-candidates", "Raw Index of Alpha", "--n", "0")
    assert proc.returncode == 0
    assert "1 个簇，只列前 0 个" in proc.stdout
    assert "（1 个簇未列出——--n 太小）" in proc.stdout


def test_read_only(vault):
    before = {p: p.read_text(encoding="utf-8") for p in vault.rglob("*.md")}
    run_vault(vault, "index-candidates", "Raw Index of Alpha")
    assert {p: p.read_text(encoding="utf-8") for p in vault.rglob("*.md")} == before


def test_json_payload_shape(vault):
    data = json.loads(run_vault(vault, "index-candidates", "Raw Index of Alpha",
                                "--json").stdout)
    assert data["command"] == "index-candidates" and data["found"] is True
    assert data["raw"] == "Raw Index of Alpha"
    assert data["members"] == ["Node A", "Node Shared"]
    assert data["cluster_count"] == 1 and data["theta"] > 0
    row = data["clusters"][0]
    assert {"cluster", "size", "members", "evidence", "commonality_draft", "index_names"} <= set(row)
    assert row["commonality_draft"].startswith("共享 ")
    assert all(name.startswith("Index of ") for name in row["index_names"])
