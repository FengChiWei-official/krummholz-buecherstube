"""Rule registry: one definition per invariant, rendered by every command.

`check` and `rawindex --check` both render from `RULES`, so a rule's numbers
exist once. Adding a rule = appending one `Rule`.

Fields:
    id     short stable id (G1, I1a, …)
    tier   "hard"   — any finding fails the gate (exit 1)
           "report" — never blocks; findings printed, nothing when clean
           "info"   — never blocks; prints "OK — no violations" when clean
    title  heading used by `check` (None = not rendered there)
    fn     ctx -> list[str] findings; the first line is the summary
    short  heading used by `rawindex --check` (None = not rendered there)
    note   optional ctx -> str line printed under the `check` heading
"""

from __future__ import annotations

import collections
from collections import namedtuple
from dataclasses import dataclass

from . import parse

Rule = namedtuple("Rule", "id tier title fn short note", defaults=(None, None))


@dataclass(frozen=True)
class Context:
    """Everything a rule may read: the config and the one shared graph."""

    cfg: object
    graph: object

    def rel(self, path):
        return self.graph.rel(path)

    @property
    def material_prefix(self) -> str:
        return self.cfg.paths["archives_material"] + "/"

    def materials(self) -> list:
        return [p for p in self.graph.notes
                if self.rel(p).startswith(self.material_prefix) and p.suffix == ".md"]


# ---------------------------------------------------------------- hard gates


def rule_g1(ctx: Context) -> list:
    """G1: root is the entry queue — only the allowed files live there."""
    cfg = ctx.cfg
    return [f"{p.name}: file me (root is the entry queue)"
            for p in cfg.root.glob("*.md") if p.name not in cfg.root_allowed]


def _unsourced_materials(ctx: Context) -> list:
    out = []
    for p, text in ctx.graph.notes.items():
        if not ctx.rel(p).startswith(ctx.material_prefix):
            continue
        source = parse.parse_frontmatter(text).get("source", "")
        if not source or str(source).strip() in ("", '""', "''"):
            out.append(p)
    return out


def rule_g2(ctx: Context) -> list:
    """G2: every archives/material/ note carries a real `source:`."""
    return [f"{ctx.rel(p)}: no real source:"
            for p in _unsourced_materials(ctx)
            if p.stem not in ctx.cfg.baseline_lit_nosource_stems]


def rule_g2_baseline(ctx: Context) -> list:
    """G2-baseline: material notes already un-sourced at the 2026-09 snapshot."""
    return [f"{ctx.rel(p)}: no real source:"
            for p in _unsourced_materials(ctx)
            if p.stem in ctx.cfg.baseline_lit_nosource_stems]


def rule_g3(ctx: Context) -> list:
    """G3: no NEW unresolved wikilinks (dangling links are allowed as hooks)."""
    g, cfg = ctx.graph, ctx.cfg
    known = g.resolvable()
    out = []
    for p, text in g.notes.items():
        for target, line_no in parse.extract_wikilinks(text):
            if target in known or target in cfg.whitelist_unresolved:
                continue
            if parse.is_image_embed(target):
                continue
            out.append(f"{ctx.rel(p)}:{line_no}: unresolved [[{target}]]")
    return out


def g3_scope_note(ctx: Context) -> str:
    skip = "、".join(sorted(ctx.cfg.skip_dirs))
    notes_skip = "、".join(sorted(ctx.cfg.notes_skip_dirs - ctx.cfg.skip_dirs))
    return (f"扫描范围: 除 {skip} 之外的全部 *.md；笔记载入另跳过 {notes_skip}"
            f"（其笔记名仍可作为链接目标解析）。白名单: {ctx.cfg.source.name} 配置的 "
            f"whitelist_unresolved（当前 {len(ctx.cfg.whitelist_unresolved)} 条）")


# ---------------------------------------------------------------- report level


def rule_i1a(ctx: Context) -> list:
    """I1a: Nodes with no registration edge at all (the queue)."""
    return [f"未登记: {len(ctx.graph.unregistered())}  (queue — see rawindex L0)"]


def i1b_note(ctx: Context) -> str:
    return ("登记面 = Raw Index 笔记内的全部 [[Node]] 链接（含正文提及）；"
            "重复 = 同一 (Raw Index, Node) 对出现两次以上")


def rule_i1b(ctx: Context) -> list:
    """I1b: registration edges repeated, plus multi-parent under the tree model."""
    g = ctx.graph
    violations = g.registration_violations()
    dupes = violations["duplicate_edges"]
    lines = [f"重复登记边: {len(dupes)}"]
    if g.config.trunk_model == "tree":
        multi = violations["multi_parent"]
        lines[0] = f"{lines[0]}   多重登记: {len(multi)}"
        for stem, raws in sorted(multi.items())[:8]:
            lines.append(f"多重登记: {stem} -> {raws}")
    for raw, node, count in dupes[:8]:
        lines.append(f"重复边: {raw.stem} -> {node.stem} ×{count}")
    return lines


def rule_i1c(ctx: Context) -> list:
    """I1c: the Raw Index → Raw Index subgraph must stay acyclic."""
    core = ctx.graph.raw_index_cycle_core()
    if not core:
        return ["Raw Index 环: 0  (登记边构成的子图无环)"]
    lines = [f"Raw Index 环: {len(core)} 个 Raw Index 落在环上"]
    for raw in core[:8]:
        lines.append(f"环上: {raw.stem}")
    return lines


def rule_i2(ctx: Context) -> list:
    """I2: a Links note must span ≥2 Index areas (same-area = violation)."""
    g = ctx.graph
    area = g.area
    lines = []
    cross = intra = noarea = 0
    for note in g.linksn:
        members = [q for q in g.out[note] if q in area]
        areas = set().union(*[area[q] for q in members]) if members else set()
        if len(areas) >= 2:
            cross += 1
        elif areas:
            intra += 1
            lines.append(f"同区域(违规): {note.stem} ({len(members)} 成员)")
        else:
            noarea += 1
    return [f"跨界 {cross} | 同区域 {intra}(违规) | 无区域 {noarea}(提示)"] + lines


def rule_i3(ctx: Context) -> list:
    """I3: every Node should have ≥1 outbound link (capture rule, incremental)."""
    g = ctx.graph
    zero = g.zero_outlink()
    pct = len(zero) * 100 // max(1, len(g.nodes))
    return [f"零出链: {len(zero)}/{len(g.nodes)} ({pct}%) — 捕获规则增量,不阻断 (B5)"]


def rule_i4(ctx: Context) -> list:
    """I4: doctrine and Raw Index notes are not binding neighbors."""
    g = ctx.graph
    return [f"绑定邻居排除 doctrine({len(g.doctrine)}) 与 Raw({len(g.raws)}) — "
            "绑定邻居图已剔除两者,无违规"]


def rule_material(ctx: Context) -> list:
    """D21: material outbound links mean the note has been extracted (拆) from."""
    materials = ctx.materials()
    unsplit = [p for p in materials if not ctx.graph.out[p]]
    lines = [f"未拆材料: {len(unsplit)}/{len(materials)}  (零出链 = 未拆)"]
    lines += [ctx.rel(p) for p in unsplit[:8]]
    return lines


RULES = [
    Rule("G1", "hard", "G1 root drained (hard gate)", rule_g1),
    Rule("G2", "hard", "G2 archives/material/ has real source (hard gate)", rule_g2),
    Rule("G2b", "info", "G2-baseline material without source (2026-09 baseline, informational)",
         rule_g2_baseline),
    Rule("G3", "hard", "G3 wikilink integrity — NEW unresolved only (hard gate)", rule_g3,
         note=g3_scope_note),
    Rule("I1a", "report", "I1a 未登记 Nodes (report: weekly increment)", rule_i1a,
         short="I1a 每个 Node 至少登记在一个 Raw Index"),
    Rule("I1b", "report", "I1b 重复登记边 (report)", rule_i1b,
         short="I1b 重复登记边（同一 (Raw Index, Node) 出现两次）", note=i1b_note),
    Rule("I1c", "report", "I1c Raw Index 环 (report)", rule_i1c,
         short="I1c Raw Index 子图无环"),
    Rule("I2", "report", "I2 Links 跨区域 — 同区域=违规 无区域=提示 (report)", rule_i2,
         short="I2 Links 必须横跨 >=2 个 Index 区域"),
    Rule("I3", "report", "I3 Node ≥1 出链 (report: weekly increment)", rule_i3,
         short="I3 Node 必须 >=1 条出链（捕获规则）"),
    Rule("I4", "report", "I4 doctrine/Raw 不做绑定邻居 (report)", rule_i4),
    Rule("D21", "report", None, rule_material, short="材料 出链=已拆 (D21)"),
]
