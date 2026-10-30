"""Parser tests: the single truth for wikilinks, aliases and frontmatter."""

from __future__ import annotations

from vaultkit import parse

FENCED = """# Note

- [[Real Target]] — counts
- `[[Inline Code]]` — must not count
- ![[Embedded Target]] — embed counts

```cpp
// [[Fenced Target]] must not count
```

- [[Page|Alias Label]] — alias label kept separately
- [[folder/Path Target#Heading]] — anchor and path stripped by link_name
"""


def test_extract_links_records_target_alias_line():
    links = parse.extract_links(FENCED)
    assert ("Real Target", None, 3) in links
    assert ("Embedded Target", None, 5) in links
    assert ("Page", "Alias Label", 11) in links
    assert ("folder/Path Target#Heading", None, 12) in links


def test_extract_links_skips_code_spans_and_fences():
    targets = [link.target for link in parse.extract_links(FENCED)]
    assert "Inline Code" not in targets
    assert "Fenced Target" not in targets


def test_link_name_normalizes_path_anchor_and_alias():
    assert parse.link_name("folder/Path Target#Heading") == "Path Target"
    assert parse.link_name("Page|Alias Label") == "Page"
    assert parse.link_name("  Spaced  ") == "Spaced"


def test_extract_wikilinks_is_the_target_only_view():
    assert ("Real Target", 3) in parse.extract_wikilinks(FENCED)
    assert all(isinstance(name, str) and name for name, _ in parse.extract_wikilinks(FENCED))


def test_parse_frontmatter_scalar_and_list():
    text = "---\naliases: [one, 'two']\nsource: somewhere\n---\n\nbody\n"
    fm = parse.parse_frontmatter(text)
    assert fm["aliases"] == ["one", "two"]
    assert fm["source"] == "somewhere"


def test_parse_frontmatter_block_list_and_absent():
    text = "---\nsource:\n  - \"first origin\"\n  - \"second origin\"\n---\nbody\n"
    assert parse.parse_frontmatter(text)["source"] == ["first origin", "second origin"]
    assert parse.parse_frontmatter("no frontmatter here\n") == {}


def test_is_image_embed():
    assert parse.is_image_embed("diagram.svg")
    assert parse.is_image_embed("photo.JPEG")
    assert not parse.is_image_embed("Node A")


def test_alias_map(tmp_path):
    a = tmp_path / "Node A.md"
    b = tmp_path / "Node B.md"
    a.write_text("---\naliases: [别名A]\n---\n", encoding="utf-8")
    b.write_text("---\naliases: 别名B\n---\n", encoding="utf-8")
    out = parse.alias_map({a: a.read_text(), b: b.read_text()})
    assert out == {"别名A": a, "别名B": b}


def test_iter_notes_skips_directories(tmp_path):
    (tmp_path / "keep").mkdir()
    (tmp_path / "skip").mkdir()
    (tmp_path / "keep" / "a.md").write_text("a", encoding="utf-8")
    (tmp_path / "skip" / "b.md").write_text("b", encoding="utf-8")
    assert [p.name for p in parse.iter_notes(tmp_path, {"skip"})] == ["a.md"]


SECTIONS = """# Note

## 时间轴

| 世代 | 年份 |
|---|---|
| 一 | 1950 |

## 地图

| 挂点 | 合同 |
|---|---|
| [[Node A]] | ISA |

## Mapping

| 实例 | 章节 |
|---|---|
| [[Node B]] | ch4 |
| [[Node C]] | ch5 |

```cpp
## 地图
[[Not A Link]]
```
"""


def test_section_lines_distinguishes_missing_from_empty():
    assert parse.section_lines(SECTIONS, "时间轴") is not None
    assert parse.section_lines(SECTIONS, "地图") is not None
    assert parse.section_lines(SECTIONS, "不存在") is None


def test_table_rows_counts_body_only():
    assert parse.table_rows(SECTIONS, "时间轴") == 1
    assert parse.table_rows(SECTIONS, "地图") == 1
    assert parse.table_rows(SECTIONS, "Mapping") == 2
    assert parse.table_rows(SECTIONS, "不存在") is None
    assert parse.table_rows("## 实例化\n\n| a | b |\n|---|---|\n", "实例化") == 0


def test_section_links_stays_inside_the_section_and_skips_fences():
    links = parse.section_links(SECTIONS, "地图")
    assert [link.target for link in links] == ["Node A"]
    assert [link.target for link in parse.section_links(SECTIONS, "Mapping")] == ["Node B",
                                                                                  "Node C"]
    assert parse.section_links(SECTIONS, "不存在") == []
