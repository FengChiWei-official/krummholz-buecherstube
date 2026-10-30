"""new: create a note from a scaffold, in the zone its state belongs to.

The doctrine is enforced here, not suggested: zone by state, genre by name
(name > path), `source:` for material (G2), a hook for unfinished work (rule 5).
These tests pin the refusals as much as the happy path.
"""

from __future__ import annotations

import json
import shutil

import pytest

from conftest import REPO, run_vault


@pytest.fixture()
def vault_with_templates(vault):
    """The fixture vault plus the real `template/` scaffolds."""
    shutil.copytree(REPO / "template", vault / "template")
    return vault


def test_node_lands_in_its_letter_fold(vault_with_templates):
    proc = run_vault(vault_with_templates, "new", "Vector Field", "--zone", "library")
    assert proc.returncode == 0
    assert "library/V_fold/Vector Field.md" in proc.stdout
    assert "template/node-temp.md" in proc.stdout
    assert "[dry-run]" in proc.stdout
    assert not (vault_with_templates / "library/V_fold/Vector Field.md").exists()


def test_digit_and_cjk_folds(vault_with_templates):
    assert "library/0_fold/3D Print.md" in run_vault(
        vault_with_templates, "new", "3D Print", "--zone", "library").stdout
    assert "library/中_fold/向量场.md" in run_vault(
        vault_with_templates, "new", "向量场", "--zone", "library").stdout


def test_root_is_the_default_zone(vault_with_templates):
    proc = run_vault(vault_with_templates, "new", "Loose Capture")
    assert proc.returncode == 0
    assert "落点: Loose Capture.md" in proc.stdout
    assert "入口队列" in proc.stdout


@pytest.mark.parametrize("name,expected", [
    ("Raw Index of Zed", "library/Raw/Raw Index of Zed.md"),
    ("Index of Zed", "library/Index/Index of Zed.md"),
    ("Links of A and C", "library/Links/Links of A and C.md"),
    ("Zed-MOC", "library/Index/Zed-MOC.md"),
])
def test_genre_names_land_in_their_home(vault_with_templates, name, expected):
    proc = run_vault(vault_with_templates, "new", name, "--zone", "library")
    assert proc.returncode == 0
    assert f"落点: {expected}" in proc.stdout


@pytest.mark.parametrize("zone", ["material", "work", "todos", "root"])
def test_genre_name_outside_library_refuses(vault_with_templates, zone):
    proc = run_vault(vault_with_templates, "new", "Raw Index of Zed", "--zone", zone)
    assert proc.returncode == 1
    assert "名字决定体裁" in proc.stdout
    assert (REPO / "library").exists()  # nothing written anywhere


def test_material_requires_a_source(vault_with_templates):
    proc = run_vault(vault_with_templates, "new", "Some Paper", "--zone", "material")
    assert proc.returncode == 1
    assert "G2 硬门" in proc.stdout
    proc = run_vault(vault_with_templates, "new", "Some Paper", "--zone", "material",
                     "--source", "arxiv:1234")
    assert proc.returncode == 0
    assert "template/lit-temp.md" in proc.stdout
    assert "source: arxiv:1234" in proc.stdout


def test_existing_name_refuses(vault_with_templates):
    proc = run_vault(vault_with_templates, "new", "Node A", "--zone", "library")
    assert proc.returncode == 1
    assert "已有同名笔记 `Node A`" in proc.stdout


def test_path_separator_refuses(vault_with_templates):
    proc = run_vault(vault_with_templates, "new", "sub/Thing")
    assert proc.returncode == 1
    assert "不能含路径分隔符" in proc.stdout


def test_unknown_template_refuses(vault_with_templates):
    proc = run_vault(vault_with_templates, "new", "Thing", "--template", "nope")
    assert proc.returncode == 1
    assert "没有模板 `nope`" in proc.stdout


def test_template_and_no_template_conflict(vault_with_templates):
    proc = run_vault(vault_with_templates, "new", "Thing", "--template", "node",
                     "--no-template")
    assert proc.returncode == 1
    assert "只能给一个" in proc.stdout


def test_todo_hook_needs_an_owner(vault_with_templates):
    proc = run_vault(vault_with_templates, "new", "Thing", "--todo", "补例子")
    assert proc.returncode == 1
    assert "补 --into" in proc.stdout


def test_todo_owner_must_exist(vault_with_templates):
    proc = run_vault(vault_with_templates, "new", "Thing", "--todo", "补例子",
                     "--into", "No Such Todo")
    assert proc.returncode == 1
    assert "顶层没有叫 `No Such Todo`" in proc.stdout


def test_apply_writes_the_note_the_hook_and_the_register(vault_with_templates):
    todo = run_vault(vault_with_templates, "new", "Math Todo", "--zone", "todos", "--apply")
    assert todo.returncode == 0
    todo_note = vault_with_templates / "a_sticker/todos/Math Todo.md"
    assert todo_note.exists()
    register = (vault_with_templates / "a_sticker/todos/Index of Todos.md").read_text(
        encoding="utf-8")
    assert "- [ ] [[Math Todo]]" in register

    proc = run_vault(vault_with_templates, "new", "Vector Field", "--zone", "library",
                     "--todo", "补定义与两个例子", "--into", "Math Todo", "--apply")
    assert proc.returncode == 0
    note = (vault_with_templates / "library/V_fold/Vector Field.md").read_text(encoding="utf-8")
    assert "## Definition" in note and "## **Related**" in note
    assert "- [ ] [[Vector Field]] — 补定义与两个例子" in todo_note.read_text(encoding="utf-8")


def test_apply_prints_link_candidates_from_the_real_graph(vault_with_templates):
    """S2: the tool offers candidates, the owner picks — it never links for you."""
    run_vault(vault_with_templates, "new", "Math Todo", "--zone", "todos", "--apply")
    proc = run_vault(vault_with_templates, "new", "Vector Field", "--zone", "library",
                     "--todo", "补定义", "--into", "Math Todo", "--apply")
    assert "S2 — 捕获时当场链 ≥1 篇旧笔记" in proc.stdout
    assert "[[Index of Todos]]" in proc.stdout or "[[Math Todo]]" in proc.stdout
    note = (vault_with_templates / "library/V_fold/Vector Field.md").read_text(encoding="utf-8")
    assert "[[Index of Todos]]" not in note  # candidates are printed, never inserted


def test_missing_template_dir_degrades_to_plain_markdown(vault):
    """No `template/` at all (the fixture) must not crash — scaffolds are optional."""
    assert not (vault / "template").exists()
    proc = run_vault(vault, "new", "Some Node", "--zone", "library")
    assert proc.returncode == 0
    assert "不存在——纯 markdown" in proc.stdout and "Traceback" not in proc.stderr
    proc = run_vault(vault, "new", "Some Node", "--zone", "library", "--template", "node")
    assert proc.returncode == 1
    assert "没有模板 `node`" in proc.stdout
    assert "Traceback" not in proc.stderr


def test_no_template_gives_plain_markdown(vault_with_templates):
    proc = run_vault(vault_with_templates, "new", "Bare Note", "--zone", "work",
                     "--no-template", "--apply")
    assert proc.returncode == 0
    assert (vault_with_templates / "archives/work/Bare Note.md").read_text(encoding="utf-8") == ""


def test_source_injected_when_the_scaffold_has_no_source_line(vault_with_templates):
    (vault_with_templates / "template" / "custom.md").write_text(
        "---\naliases:\n---\n\n## Body\n", encoding="utf-8")
    proc = run_vault(vault_with_templates, "new", "Paper", "--zone", "material",
                     "--source", "arxiv:1234", "--template", "custom.md", "--apply")
    assert proc.returncode == 0
    text = (vault_with_templates / "archives/material/Paper.md").read_text(encoding="utf-8")
    assert text.startswith("---\nsource: arxiv:1234\n")
    assert "## Body" in text


def test_check_stays_clean_after_creating_a_material_note(vault_with_templates):
    """The fixture has one seeded G2 violation; the new note must not add a second."""
    before = run_vault(vault_with_templates, "check")
    run_vault(vault_with_templates, "new", "Some Paper", "--zone", "material",
              "--source", "arxiv:1234", "--apply")
    after = run_vault(vault_with_templates, "check")
    assert before.stdout.count("no real source:") == after.stdout.count("no real source:")
    assert "archives/material/Some Paper.md" not in after.stdout


def test_json_payload(vault_with_templates):
    run_vault(vault_with_templates, "new", "Math Todo", "--zone", "todos", "--apply")
    proc = run_vault(vault_with_templates, "new", "Gauge Field", "--zone", "library",
                     "--todo", "补例子", "--into", "Math Todo", "--json")
    data = json.loads(proc.stdout)
    assert data["path"] == "library/G_fold/Gauge Field.md"
    assert data["genre"] == "node" and data["zone"] == "library"
    assert data["template"] == "template/node-temp.md"
    assert data["applied"] is False and data["exit"] == 0
    assert data["todo_file"] == "a_sticker/todos/Math Todo.md"
    assert data["todo_line"] == "- [ ] [[Gauge Field]] — 补例子"
    assert data["error"] is None
    assert any("登记边" in w for w in data["warnings"])
