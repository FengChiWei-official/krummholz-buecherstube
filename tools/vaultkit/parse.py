"""The ONLY wikilink / frontmatter / note-iteration code in vaultkit.

Everything that reads note text goes through here, so the vault has exactly one
parser: one answer to "what links does this note have?", code fences stripped,
aliases resolved the same way everywhere.
"""

from __future__ import annotations

import re
from collections import namedtuple
from pathlib import Path

# (target, alias, line) — target is the raw inner text (path/#anchor/|alias kept).
Link = namedtuple("Link", "target alias line")

_WIKILINK_RE = re.compile(r"(!?)\[\[([^\]\n]+?)(\|[^\]\n]*)?\]\]")
_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`]*`")

_IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".svg")


def iter_notes(root: Path, skip_dirs):
    """Yield every *.md under root whose path contains no skipped directory."""
    for path in root.rglob("*.md"):
        rel = path.relative_to(root)
        if any(part in skip_dirs for part in rel.parts):
            continue
        yield path


def parse_frontmatter(text: str) -> dict:
    """Parse the first --- block into a dict. Values stay strings; tags become a list."""
    fm: dict = {}
    if not text.startswith("---"):
        return fm
    lines = text.splitlines()
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return fm
    key = None
    for line in lines[1:end]:
        if not line.strip() or line.strip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            if value.startswith("[") and value.endswith("]"):
                inner = value[1:-1]
                fm[key] = [v.strip().strip("'\"") for v in inner.split(",") if v.strip()]
            elif value:
                fm[key] = value
            else:
                fm[key] = []
        elif re.match(r"^\s+-\s+", line) and key is not None:
            fm.setdefault(key, [])
            if isinstance(fm[key], list):
                fm[key].append(re.sub(r"^\s+-\s+", "", line).strip().strip("'\""))
    return fm


def _strip_fences(text: str) -> str:
    """Blank out fenced code blocks without losing their line count."""
    return _FENCE_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)


def extract_links(text: str) -> list:
    """Every [[...]] in text (embeds included), code spans and fences skipped."""
    text = _strip_fences(text)
    out = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        line = _INLINE_CODE_RE.sub("", line)
        for match in _WIKILINK_RE.finditer(line):
            alias = (match.group(3) or "")[1:].strip() or None
            out.append(Link(match.group(2), alias, line_no))
    return out


def link_name(target: str) -> str:
    """Normalize a wikilink target to its note name (drop #anchor, path, alias)."""
    name = target.split("#")[0].split("|")[0]
    return name.split("/")[-1].strip()


def extract_wikilinks(text: str):
    """(note name, line_no) for every [[...]] — the target-only view of extract_links."""
    return [(name, link.line) for link in extract_links(text)
            if (name := link_name(link.target))]


def is_image_embed(target: str) -> bool:
    return target.lower().endswith(_IMAGE_SUFFIXES)


def alias_map(texts: dict) -> dict:
    """{alias: note Path} — Obsidian resolves wikilinks through `aliases:`."""
    out: dict = {}
    for p, t in texts.items():
        aliases = parse_frontmatter(t).get("aliases", [])
        if isinstance(aliases, str):
            aliases = [aliases]
        for a in aliases:
            if a:
                out.setdefault(a.strip(), p)
    return out
