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


_HEADING_RE = re.compile(r"^#{1,6}\s+(\S.*?)\s*$")
_TABLE_SEPARATOR_RE = re.compile(r"^\|[\s:|-]+\|$")


def section_lines(text: str, heading: str):
    """Raw lines under the first `#… heading`, up to the next heading.

    Headings inside fenced code blocks do not open or close a section, so a
    fenced example never leaks into the real section's body. Returns None when
    the heading is absent — callers use that to tell "section missing" from
    "section present but empty".
    """
    out = None
    capture = False
    fence = None
    for line in text.splitlines():
        stripped = line.lstrip()
        marker = stripped[:3]
        if marker in ("```", "~~~"):
            fence = None if fence == marker else (fence or marker)
            if capture:
                out.append(line)
            continue
        if fence is None:
            match = _HEADING_RE.match(line)
            if match:
                capture = match.group(1).strip() == heading
                if capture and out is None:
                    out = []
                continue
        if capture:
            out.append(line)
    return out


def section_links(text: str, heading: str) -> list:
    """[[...]] links inside one section, with section-relative line numbers."""
    lines = section_lines(text, heading)
    if lines is None:
        return []
    body = _strip_fences("\n".join(lines))
    out = []
    for line_no, line in enumerate(body.splitlines(), start=1):
        line = _INLINE_CODE_RE.sub("", line)
        for match in _WIKILINK_RE.finditer(line):
            alias = (match.group(3) or "")[1:].strip() or None
            out.append(Link(match.group(2), alias, line_no))
    return out


def table_rows(text: str, heading: str):
    """Body rows of the markdown table under `heading`; None when absent.

    Header row and separator are not counted, so an empty table is 0.
    """
    lines = section_lines(text, heading)
    if lines is None:
        return None
    rows = 0
    seen_separator = False
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if _TABLE_SEPARATOR_RE.match(stripped):
            seen_separator = True
            continue
        if seen_separator:
            rows += 1
    return rows


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
