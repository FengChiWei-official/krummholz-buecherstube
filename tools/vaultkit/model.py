"""The vault model: notes, links and the two-tree graph.

Built once per process (`Graph.load`), so `check`, `status` and `rawindex`
share one parse and one resolution map. Registration edges (Raw Index → Node)
are owned here: they are the structural trunk and their uniqueness rule lives
in this module.
"""

from __future__ import annotations

import collections
from dataclasses import dataclass, field
from pathlib import Path

from . import parse
from .config import Config

_CACHE: dict = {}


@dataclass
class Note:
    """One note file: path plus text, with lazy frontmatter."""

    path: Path
    text: str
    _frontmatter: dict | None = field(default=None, repr=False, compare=False)

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def frontmatter(self) -> dict:
        if self._frontmatter is None:
            self._frontmatter = parse.parse_frontmatter(self.text)
        return self._frontmatter

    @property
    def links(self) -> list:
        return parse.extract_links(self.text)


@dataclass
class Graph:
    config: Config
    notes: dict                 # Path -> text
    stems: dict                 # stem -> Path
    aliases: dict               # alias -> Path
    out: dict                   # Path -> set[Path] (resolved outbound links)
    reg: dict                   # Path -> set[Path] (Node -> registering Raw Indexes)
    area: dict                  # Path -> set[Path] (note -> Index areas)
    nodes: list
    raws: list
    idxs: list
    linksn: list
    doctrine: list

    # -- registration edges (the structural trunk) ------------------------
    @property
    def registration_edges(self) -> list:
        """Unique (Raw Index, Node) pairs — registration is an edge, not a parent."""
        return sorted({(r, n) for n, raws in self.reg.items() for r in raws},
                      key=lambda pair: (pair[0].stem, pair[1].stem))

    def multi_registered(self) -> dict:
        """{node: [Raw Indexes]} for nodes carrying more than one registration edge."""
        return {n.stem: [r.stem for r in sorted(self.reg[n], key=lambda p: p.stem)]
                for n in self.nodes if len(self.reg[n]) > 1}

    def unregistered(self) -> list:
        return [n for n in self.nodes if not self.reg[n]]

    def zero_outlink(self) -> list:
        return [n for n in self.nodes if not self.out[n]]

    # -- lookup -----------------------------------------------------------
    def rel(self, path: Path) -> str:
        return path.relative_to(self.config.root).as_posix()

    def resolve(self, target: str):
        name = parse.link_name(target)
        return self.stems.get(name) or self.aliases.get(name)

    def resolvable(self) -> set:
        """Every name a wikilink may legitimately resolve to."""
        names = {p.stem for p in self.notes}
        names |= {p.stem for p in (self.config.zzz_dir).rglob("*.md")}
        names |= {p.stem for p in (self.config.root / ".agent").rglob("*.md")}
        names |= set(self.aliases)
        return names

    def neighbors(self) -> dict:
        """Undirected adjacency over every note."""
        nbr: dict = collections.defaultdict(set)
        for p, qs in self.out.items():
            for q in qs:
                nbr[p].add(q)
                nbr[q].add(p)
        return nbr


def build(config: Config) -> Graph:
    notes = {p: p.read_text(encoding="utf-8", errors="replace")
             for p in sorted(parse.iter_notes(config.root, config.notes_skip_dirs))}
    stems: dict = {}
    for p in notes:
        stems.setdefault(p.stem, p)
    aliases = parse.alias_map(notes)

    def resolve(target: str):
        name = parse.link_name(target)
        return stems.get(name) or aliases.get(name)

    out: dict = {}
    for p, t in notes.items():
        links = set()
        for link in parse.extract_links(t):
            q = resolve(link.target)
            if q and q != p:
                links.add(q)
        out[p] = links

    zone = config.zone
    node_suffix = config.zones["node_suffix"]
    nodes = [p for p in notes if zone(p) and zone(p).endswith(node_suffix)]
    raws = [p for p in notes if zone(p) == config.zones["raw"]]
    idxs = [p for p in notes if zone(p) == config.zones["index"]]
    linksn = [p for p in notes if zone(p) == config.zones["links"]]
    doctrine = [p for p in notes
                if p.relative_to(config.root).parts[0] == config.paths["doctrine"]]

    reg: dict = collections.defaultdict(set)        # node -> {raw}
    for r in raws:
        for q in out[r]:
            if zone(q) and zone(q).endswith(node_suffix):
                reg[q].add(r)
    area: dict = collections.defaultdict(set)       # note -> {index}
    for i in idxs:
        for q in out[i]:
            area[q].add(i)

    return Graph(config=config, notes=notes, stems=stems, aliases=aliases, out=out,
                 reg=reg, area=area, nodes=nodes, raws=raws, idxs=idxs,
                 linksn=linksn, doctrine=doctrine)


def load(config: Config) -> Graph:
    """The one graph per process, keyed by (vault root, config file)."""
    key = (str(config.root), str(config.source))
    if key not in _CACHE:
        _CACHE[key] = build(config)
    return _CACHE[key]


def clear_cache() -> None:
    _CACHE.clear()
