"""Command shells: thin renderers over config/model/parse.

No parsing, no graph building and no thresholds live here — commands read the
shared `Graph` and print.
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random as random_module
import re
import subprocess
import sys
import time
from itertools import combinations
from pathlib import Path

from . import __version__, model, parse, rules
from .config import Config, ConfigError, load as load_config


# ---------------------------------------------------------------- git helpers


def _git(root: Path, args: list):
    """Run one git command; return stdout, or None when git/repo is unavailable."""
    try:
        proc = subprocess.run(["git", "-C", str(root), *args],
                              capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


_FIRST_SEEN_CACHE: dict = {}


def git_first_seen_index(cfg: Config) -> dict:
    """{repo-relative path: first commit time} in ONE git pass.

    Creation time that survives moves/migrations (unlike mtime). Renames are
    left to git's own rename detection: a moved path simply has no entry, which
    is safer than reporting the move as a creation.
    """
    key = str(cfg.root)
    if key in _FIRST_SEEN_CACHE:
        return _FIRST_SEEN_CACHE[key]
    index: dict = {}
    top = _git(cfg.root, ["rev-parse", "--show-toplevel"])
    # Paths are reported relative to the repository root, so only trust the index
    # when the vault root *is* the repository root.
    if top is not None and Path(top.strip()).resolve() == cfg.root.resolve():
        out = _git(cfg.root, ["log", "--diff-filter=A", "--name-only", "--format=%ct"])
        if out is not None:
            stamp = None
            for line in out.splitlines():
                line = line.strip()
                if not line:
                    continue
                if line.isdigit():
                    stamp = float(line)
                elif stamp is not None:
                    index[line] = stamp      # newest-first: the last write is the oldest
    _FIRST_SEEN_CACHE[key] = index
    return index


def _git_last_commit(cfg: Config, paths: list):
    """mtime of the last commit touching any of `paths`, else None (no git/no commit)."""
    for p in paths:
        out = _git(cfg.root, ["log", "-1", "--format=%ct", "--", str(p)])
        if out and out.strip():
            return float(out.strip())
    return None


def _git_porcelain(cfg: Config):
    """git status --porcelain lines, or None when git/repo is unavailable."""
    out = _git(cfg.root, ["status", "--porcelain"])
    if out is None:
        return None
    return [ln for ln in out.splitlines() if ln.strip()]


# ---------------------------------------------------------------- render helpers


def _rel(cfg: Config, path: Path) -> str:
    return path.relative_to(cfg.root).as_posix()


def wants_json(args) -> bool:
    return bool(getattr(args, "json", False))


def emit_json(payload: dict) -> None:
    """Machine-readable output: one JSON document on stdout, nothing else."""
    print(json.dumps(payload, ensure_ascii=False, indent=2))


EXIT_CODES = {
    "0": "ok — every report, and any check whose hard gates are green",
    "1": "hard gate failed (check) or unknown target (rawindex --around / suggest)",
    "2": "missing or unreadable config (also a missing list file under --strict)",
}


# ---------------------------------------------------------------- check


def collect_check(cfg: Config, g: model.Graph):
    """Gather all check findings, two-tier (D20).

    Returns an ordered list of (tier, title, findings):
    tier "gate"    -> hard gate: any finding makes check exit 1.
    tier "report"  -> report-level: weekly increments, never blocks.
    tier "info"    -> informational baseline, never blocks.
    """
    basenames = g.resolvable()

    # ---- G1 (gate): root drained
    root_findings = [f"{p.name}: file me (root is the entry queue)"
                     for p in cfg.root.glob("*.md") if p.name not in cfg.root_allowed]

    # ---- G2 (gate): every archives/material/ note has a real source:
    # lit detection by PATH (doctrine v5: material/ is the lit zone).
    lit_findings = []
    lit_baseline = []
    material_prefix = cfg.paths["archives_material"] + "/"
    for p, text in g.notes.items():
        rel = _rel(cfg, p)
        if not rel.startswith(material_prefix):
            continue
        source = parse.parse_frontmatter(text).get("source", "")
        if not source or str(source).strip() in ("", '""', "''"):
            entry = f"{rel}: no real source:"
            if p.stem in cfg.baseline_lit_nosource_stems:
                lit_baseline.append(entry)
            else:
                lit_findings.append(entry)

    # ---- G3 (gate): wikilink integrity (NEW unresolved only)
    unresolved_findings = []
    for p, text in g.notes.items():
        for target, line_no in parse.extract_wikilinks(text):
            if target in basenames or target in cfg.whitelist_unresolved:
                continue
            if parse.is_image_embed(target):
                continue
            unresolved_findings.append(f"{_rel(cfg, p)}:{line_no}: unresolved [[{target}]]")

    # ---- R-I1..R-I4 (report): the weekly increments
    nodes = g.nodes

    i1_unregistered = g.unregistered()
    i1_lines = [f"未登记: {len(i1_unregistered)}  (queue — see rawindex L0)"]
    for stem, raws in sorted(g.multi_registered().items())[:8]:
        i1_lines.append(f"  多重登记: {stem} -> {raws}")

    area = g.area
    i2_lines = []
    cross = intra = noarea = 0
    for L in g.linksn:
        members = [q for q in g.out[L] if q in area]
        areas = set().union(*[area[q] for q in members]) if members else set()
        if len(areas) >= 2:
            cross += 1
        elif areas:
            intra += 1
            i2_lines.append(f"  同区域(违规): {L.stem} ({len(members)} 成员)")
        else:
            noarea += 1
    i2_lines.insert(0, f"跨界 {cross} | 同区域 {intra}(违规) | 无区域 {noarea}(提示)")

    zero = g.zero_outlink()
    i3_lines = [f"零出链: {len(zero)}/{len(nodes)} ({len(zero) * 100 // max(1, len(nodes))}%)"
                " — 捕获规则增量,不阻断 (B5)"]

    # I4: doctrine & Raw excluded from binding neighbors — enforced structurally
    # by the trunk-graph builder; report the exclusion counts.
    i4_lines = [f"绑定邻居排除 doctrine({len(g.doctrine)}) 与 Raw({len(g.raws)}) — "
                "结构性排除,无违规"]

    return [
        ("gate", "G1 root drained (hard gate)", root_findings),
        ("gate", "G2 archives/material/ has real source (hard gate)", lit_findings),
        ("info", "G2-baseline material without source (2026-09 baseline, informational)",
         lit_baseline),
        ("gate", "G3 wikilink integrity — NEW unresolved only (hard gate)",
         unresolved_findings),
        ("report", "I1 唯一归属 (report: weekly increment)", i1_lines),
        ("report", "I2 Links 跨区域 — 同区域=违规 无区域=提示 (report)", i2_lines),
        ("report", "I3 Node ≥1 出链 (report: weekly increment)", i3_lines),
        ("report", "I4 doctrine/Raw 不做绑定邻居 (report)", i4_lines),
    ]


def cmd_check(cfg: Config, g: model.Graph, args) -> int:
    """Render every `check` rule from the registry (rules.py)."""
    ctx = rules.Context(cfg=cfg, graph=g)
    problems = 0
    payload_rules = []
    if not wants_json(args):
        print("# vault check — two-tier (D20): hard gates exit 1; I1–I4 report-level\n")
    for rule in rules.RULES:
        if not rule.title:
            continue
        findings = rule.fn(ctx)
        payload_rules.append({"id": rule.id, "tier": rule.tier, "title": rule.title,
                              "count": len(findings), "findings": findings})
        if wants_json(args):
            if rule.tier == "hard" and findings:
                problems += 1
            continue
        print(f"## {rule.title}")
        if rule.note:
            print(f"  {rule.note(ctx)}")
        if findings:
            for item in findings:
                print(f"  {item}")
            if rule.tier == "hard":
                problems += 1
        elif rule.tier in ("hard", "info"):
            print("  OK — no violations")
        print()
    if wants_json(args):
        emit_json({"command": "check", "version": __version__, "vault_root": str(cfg.root),
                   "problems": problems, "clean": problems == 0,
                   "exit_codes": EXIT_CODES, "rules": payload_rules})
        return 1 if problems else 0
    print("CLEAN — hard gates hold; report-level numbers above are weekly increments"
          if problems == 0 else f"PROBLEMS: {problems} (hard gates failed)")
    return 1 if problems else 0


def collect_check(cfg: Config, g: model.Graph):
    """[{id, tier, title, findings}] for every `check` rule — used by `status`."""
    ctx = rules.Context(cfg=cfg, graph=g)
    return [{"id": rule.id, "tier": rule.tier, "title": rule.title, "findings": rule.fn(ctx)}
            for rule in rules.RULES if rule.title]


# ---------------------------------------------------------------- rawindex


def _rawindex_check(cfg: Config, g: model.Graph) -> None:
    """Render the registry rules that carry a `rawindex --check` heading."""
    ctx = rules.Context(cfg=cfg, graph=g)
    for rule in rules.RULES:
        if not rule.short:
            continue
        print(f"\n## {rule.short}")
        for line in rule.fn(ctx):
            print(f"  {line}")


def _rawindex_sync(cfg: Config, g: model.Graph, apply: bool) -> int:
    """B6: maintain the trunk root's member list (registration edges).

    Structural action per D22 — AI may append directly. The root's
    `## Core Concepts` section lists one [[Node]] line per registered member
    grouped under each child Raw Index; existing prose is left alone.
    Dry-run by default (L13 write safety): nothing is written without `--apply`.
    """
    root_note = None
    for r in g.raws:
        if r.stem == cfg.trunk_root_stem:
            root_note = r
            break
    if root_note is None:
        print(f"rawindex --sync: trunk root `{cfg.trunk_root_stem}.md` not found in "
              f"{_rel(cfg, cfg.raw_dir)}/")
        return 1

    children = sorted((r for r in g.raws if r is not root_note), key=lambda p: p.stem)
    lines = []
    for r in children:
        members = sorted((n for n in g.nodes if r in g.reg[n]), key=lambda p: p.stem)
        lines.append(f"- [[{r.stem}]] ({len(members)})")
    body = "\n".join(lines)

    text = root_note.read_text(encoding="utf-8")
    marker = "## Core Concepts"
    if marker in text:
        head, _, tail = text.partition(marker)
        rest = tail.split("\n## ", 1)
        after = "\n## " + rest[1] if len(rest) > 1 else ""
        new = head + marker + "\n\n" + body + "\n" + after
    else:
        new = text.rstrip("\n") + "\n\n" + marker + "\n\n" + body + "\n"

    verb = "已注册" if apply else "[dry-run] 将注册"
    print(f"rawindex --sync: {cfg.trunk_root_stem} — {verb} {len(children)} 个 child Raw Index")
    if not apply:
        print("  （不改文件；确认后加 --apply 落地）")
    for ln in lines[:10]:
        print(f"  {ln}")
    if len(lines) > 10:
        print(f"  … ({len(lines) - 10} more)")
    if apply:
        root_note.write_text(new, encoding="utf-8")
    return 0


def _rawindex_around(cfg: Config, g: model.Graph, nbr: dict, name: str, args=None) -> int:
    """One node's neighborhood: registrations, areas, links, neighbors."""
    target = g.stems.get(name)
    if target is None:
        low = name.lower()
        cands = [s for s in g.stems if low in s.lower()][:10]
        if wants_json(args):
            emit_json({"command": "rawindex --around", "target": name, "found": False,
                       "did_you_mean": cands})
            return 1
        print(f"rawindex --around: `{name}` not found.")
        if cands:
            print("  did you mean: " + " / ".join(cands))
        return 1
    registrations = [r.stem for r in sorted(g.reg.get(target, ()), key=lambda p: p.stem)]
    areas = [i.stem for i in sorted(g.area.get(target, ()), key=lambda p: p.stem)]
    outs = sorted(g.out.get(target, set()), key=lambda p: p.stem)
    ins = sorted((p for p, qs in g.out.items() if target in qs), key=lambda p: p.stem)
    nb = sorted(nbr.get(target, set()), key=lambda p: p.stem)
    if wants_json(args):
        emit_json({"command": "rawindex --around", "target": target.stem, "found": True,
                   "path": _rel(cfg, target), "registrations": registrations,
                   "areas": areas, "outlinks": [q.stem for q in outs],
                   "inlinks": [p.stem for p in ins], "neighbors": [p.stem for p in nb]})
        return 0
    print(f"## {target.stem}")
    print(f"  path: {_rel(cfg, target)}")
    print(f"  登记: {registrations}" if registrations else "  登记: (queue — 未登记)")
    if areas:
        print(f"  区域: {areas}")
    print(f"  出链 {len(outs)}: {[q.stem for q in outs][:12]}")
    print(f"  入链 {len(ins)}: {[p.stem for p in ins][:12]}")
    print(f"  邻居 {len(nb)} (绑定证据候选: {[p.stem for p in nb][:8]})")
    return 0


# ---------------------------------------------------------------- random / suggest


def _scope_notes(cfg: Config, g: model.Graph, scope: str) -> list:
    library_prefix = cfg.paths["library"] + "/"
    if scope == "all":
        return sorted(g.notes, key=lambda p: p.stem)
    if scope == "library":
        return sorted((p for p in g.notes if g.rel(p).startswith(library_prefix)),
                      key=lambda p: p.stem)
    return sorted(g.nodes, key=lambda p: p.stem)


def cmd_random(cfg: Config, g: model.Graph, args) -> int:
    """Random note + its backlinks — 问箱 material (S9). Signal only, never writes."""
    notes = _scope_notes(cfg, g, args.scope)
    if not notes:
        if wants_json(args):
            emit_json({"command": "random", "scope": args.scope, "found": False})
            return 0
        print(f"random: scope `{args.scope}` has no notes")
        return 0
    rng = random_module.Random(args.seed)
    pick = rng.choice(notes)
    backlinks = sorted((p for p, qs in g.out.items() if pick in qs), key=lambda p: p.stem)
    if wants_json(args):
        emit_json({"command": "random", "scope": args.scope, "seed": args.seed,
                   "note": pick.stem, "path": _rel(cfg, pick),
                   "backlinks": [p.stem for p in backlinks],
                   "outlinks": sorted(q.stem for q in g.out.get(pick, set()))})
        return 0
    print(f"## {pick.stem}  (scope {args.scope}, seed {args.seed})")
    print(f"  path: {_rel(cfg, pick)}")
    print(f"  入链 {len(backlinks)}: {[p.stem for p in backlinks][:12]}")
    print(f"  出链 {len(g.out.get(pick, set()))}: "
          f"{sorted(q.stem for q in g.out.get(pick, set()))[:12]}")
    print("  → 问箱: 补一条链接，产出落为 Links 卡 (S9)")
    return 0


def suggest_candidates(cfg: Config, g: model.Graph, target, n: int) -> list:
    """[(note, why)] candidate links for `target`, strongest evidence first."""
    nbr = g.binding_neighbors()
    mine = nbr.get(target, set())
    linked = set(g.out.get(target, set())) | {p for p, qs in g.out.items() if target in qs}
    my_areas = g.area.get(target, set())
    my_raws = g.reg.get(target, set())
    scored = []
    for q in sorted(g.notes, key=lambda p: p.stem):
        if q == target or q in linked:
            continue
        shared = mine & nbr.get(q, set())
        areas = my_areas & g.area.get(q, set())
        raws = my_raws & g.reg.get(q, set())
        if not shared and not areas and not raws:
            continue
        why = None
        if shared:
            names = " / ".join(p.stem for p in sorted(shared, key=lambda p: p.stem)[:3])
            why = f"共同邻居 {len(shared)}: {names}"
        elif raws:
            why = f"同登记: {sorted(r.stem for r in raws)[0]}"
        elif areas:
            why = f"同区域: {sorted(i.stem for i in areas)[0]}"
        scored.append((-len(shared), -len(raws), -len(areas), q.stem, q, why))
    scored.sort()
    return [(q, why) for _s, _r, _a, _stem, q, why in scored[:n]]


def cmd_suggest(cfg: Config, g: model.Graph, args) -> int:
    """Candidate links for one note — S2 capture. Signal only, never writes."""
    target = g.stems.get(args.name)
    if target is None:
        cands = [s for s in g.stems if args.name.lower() in s.lower()][:10]
        if wants_json(args):
            emit_json({"command": "suggest", "target": args.name, "found": False,
                       "did_you_mean": cands})
            return 1
        print(f"suggest: `{args.name}` not found.")
        if cands:
            print("  did you mean: " + " / ".join(cands))
        return 1
    picks = suggest_candidates(cfg, g, target, args.n)
    if wants_json(args):
        emit_json({"command": "suggest", "target": target.stem, "found": True,
                   "candidates": [{"note": q.stem, "why": why} for q, why in picks]})
        return 0
    print(f"## suggest {target.stem} — {len(picks)} 个候选链接 (S2, 只给信号)")
    for i, (q, why) in enumerate(picks, 1):
        print(f"  {i}. [[{q.stem}]] — {why}")
    return 0


def cmd_rawindex(cfg: Config, g: model.Graph, args) -> int:
    """Trunk operations: queue + L0 proposals; --clusters / --check / --sync / --around."""
    out, reg = g.out, g.reg
    nodes, raws = g.nodes, g.raws
    nbr = g.binding_neighbors()          # I4: doctrine/Raw are not binding neighbors

    registered = [n for n in nodes if reg[n]]
    queue = [n for n in nodes if not reg[n]]
    if not wants_json(args):
        print(f"nodes {len(nodes)} | Raw Index {len(raws)} | Index {len(g.idxs)} "
              f"| Links {len(g.linksn)}")
        print(f"registered {len(registered)} | queue {len(queue)}")

    if args.check and not wants_json(args):
        _rawindex_check(cfg, g)

    if args.sync:
        _rawindex_sync(cfg, g, apply=args.apply)

    if args.around:
        return _rawindex_around(cfg, g, nbr, args.around, args)

    # ---------------- L0: affiliation proposals for the queue
    props = _l0_proposals(g, nbr, queue)
    if not wants_json(args):
        print(f"\n## L0 归队提议（队列 {len(queue)} 条中，能定归属的）")
        for s, n, tot, v, r in props[:args.top]:
            print(f"  {s:.0%} ({n}/{tot})  {v.stem}  ->  {r.stem}")
        if props:
            conf = sum(1 for p in props if p[0] >= cfg.thresholds["l0_confidence"])
            print(f"\n  ≥{cfg.thresholds['l0_confidence']:.0%} 置信的提议: {conf} 条 — "
                  "登记边是结构动作, AI 可直接追加 (D22); "
                  "其余照人机分工: 共性/命名你定 (D16)")

    if args.clusters:
        clusters = _cluster_data(cfg, g, nbr, queue)
        if not wants_json(args):
            _render_clusters(cfg, g, nbr, queue, clusters)

    if wants_json(args):
        payload = {
            "command": "rawindex",
            "version": __version__,
            "vault_root": str(cfg.root),
            "trunk": {"nodes": len(nodes), "raw_index": len(raws), "index": len(g.idxs),
                      "links": len(g.linksn), "registered": len(registered),
                      "queue": len(queue)},
            "l0": [{"node": v.stem, "raw_index": r.stem, "score": round(s, 4),
                    "votes": n, "neighbors": tot} for s, n, tot, v, r in props],
            "l0_high_confidence": sum(1 for p in props
                                      if p[0] >= cfg.thresholds["l0_confidence"]),
        }
        if args.check:
            payload["rules"] = [{"id": rule.id, "tier": rule.tier, "title": rule.short,
                                 "findings": rule.fn(rules.Context(cfg=cfg, graph=g))}
                                for rule in rules.RULES if rule.short]
        if args.clusters:
            payload["clusters"] = clusters
        emit_json(payload)
        return 0
    return 0


def _l0_proposals(g: model.Graph, nbr: dict, queue: list) -> list:
    """[(score, votes, neighbors, node, raw)] for queue notes with a voting neighborhood."""
    props = []
    for v in queue:
        nb = nbr[v]
        if not nb:
            continue
        sc: dict = collections.Counter()
        for z in nb:
            for r in g.reg.get(z, ()):
                sc[r] += 1
        if sc:
            r, n = min(sc.items(), key=lambda kv: (-kv[1], kv[0].stem))
            props.append((n / len(nb), n, len(nb), v, r))
    props.sort(reverse=True)
    return props


def _cluster_data(cfg: Config, g: model.Graph, nbr: dict, queue: list) -> dict:
    """L1 coarse components + L2 shared-neighbor clusters, as data."""
    Q = set(queue)
    dadj: dict = collections.defaultdict(set)
    for v in sorted(Q):
        for q in sorted(g.out[v]):
            if q in Q:
                dadj[v].add(q)
                dadj[q].add(v)
    seen, comps = set(), []
    for n in sorted(dadj):
        if n in seen:
            continue
        st, c = [n], set()
        while st:
            x = st.pop()
            if x in c:
                continue
            c.add(x)
            st += sorted(dadj[x])
        seen |= c
        comps.append(c)
    comps.sort(key=lambda c: (-len(c), min(x.stem for x in c)))

    z2u: dict = collections.defaultdict(set)
    for v in sorted(Q):
        for z in sorted(nbr[v]):
            z2u[z].add(v)
    w: dict = collections.defaultdict(float)
    for z in sorted(z2u):
        us = sorted(z2u[z])
        if len(us) < 2:
            continue
        inc = 1.0 / math.log(max(3, len(nbr[z]) + 1))
        for x, y in combinations(us, 2):
            w[(x, y)] += inc
    vals = sorted(w.values())
    pct = cfg.thresholds["cluster_theta_percentile"]
    th = vals[int(len(vals) * pct)] if vals else 0
    adj2: dict = collections.defaultdict(set)
    for (x, y), ww in w.items():
        if ww >= th:
            adj2[x].add(y)
            adj2[y].add(x)
    seen2, cs = set(), []
    for n in sorted(adj2):
        if n in seen2:
            continue
        st, c = [n], set()
        while st:
            x = st.pop()
            if x in c:
                continue
            c.add(x)
            st += sorted(adj2[x])
        seen2 |= c
        cs.append(c)
    cs.sort(key=lambda c: (-len(c), min(x.stem for x in c)))

    l2 = []
    for c in cs:
        sh: dict = collections.Counter()
        for x, y in combinations(sorted(c), 2):
            sh.update(nbr[x] & nbr[y])
        top = sorted(sh.items(), key=lambda kv: (-kv[1], kv[0].stem))[:3]
        l2.append({"members": sorted(x.stem for x in c),
                   "binding_evidence": [{"note": s.stem, "shared": n} for s, n in top]})
    return {
        "theta": th,
        "l1": {"count": len(comps), "covered": len(seen),
               "components": [sorted(x.stem for x in c) for c in comps]},
        "l2": {"count": len(cs), "largest": len(cs[0]) if cs else 0, "clusters": l2},
        "l3_isolated": len(Q) - len(seen | seen2),
    }


def _render_clusters(cfg: Config, g: model.Graph, nbr: dict, queue: list, data: dict) -> None:
    Q = set(queue)
    comps = data["l1"]["components"]
    print(f"\n## L1 直接互链粗簇: {data['l1']['count']} 个, "
          f"覆盖 {data['l1']['covered']}/{len(Q)}")
    for c in comps[:6]:
        print(f"  ({len(c)}) " + " / ".join(c[:6]))
    pct_label = f"P{round(cfg.thresholds['cluster_theta_percentile'] * 100)}"
    print(f"\n## L2 共享邻居细分 θ={pct_label}={data['theta']:.2f}: {data['l2']['count']} 簇, "
          f"最大 {data['l2']['largest']}")
    for cluster in data["l2"]["clusters"][:5]:
        print(f"  ({len(cluster['members'])}) " + " / ".join(cluster["members"][:5]))
        print(f"      绑定证据: {[e['note'] for e in cluster['binding_evidence']]}")
    print(f"\n## L3 孤点: {data['l3_isolated']}")
    print("\n## 粗主干归组 (D10-P3): AI 把簇归组进粗 Raw Index (一个含几个簇),")
    print("   细结构(簇+共性)进 Index — 绝不每簇一个 Raw Index。归组方案 AI 提,命名你定。")


# ---------------------------------------------------------------- triage


def collect_triage(cfg: Config, g: model.Graph) -> dict:
    """Gather placement-debt findings per category. Shared by `triage` and `status`.

    v5: todo aging (B1) + suspected half-done (A1) added; promote/stale-tag
    categories retired (no more status tags).
    """
    now = time.time()
    notes = sorted(g.notes.keys())
    findings = {"root": [], "todo_stale": [], "halfdone": [], "unhooked": [],
                "genre": [], "dead_todo": []}

    # 1. root files beyond allowed set
    for p in sorted(cfg.root.glob("*.md")):
        if p.name not in cfg.root_allowed:
            findings["root"].append(f"file me: {p.name} (root is the entry queue)")

    # 2. todo aging (B1): todo-note entries untouched beyond the stale threshold
    for p in sorted(cfg.todos_dir.glob("*.md")):
        age_days = (now - p.stat().st_mtime) / 86400
        if age_days > cfg.thresholds["todo_stale_days"]:
            findings["todo_stale"].append(
                f"todo 老化: {p.name} — {int(age_days)} 天未动 → 报告并清理 (B1)")

    # 3. suspected half-done (A1): created <= 7d + zero outbound + no todo hook
    todo_targets = set()
    for p in sorted(cfg.todos_dir.rglob("*.md")):
        for t, _ in parse.extract_wikilinks(g.notes.get(p, "")):
            todo_targets.add(t)
    root_queue = {p for p in notes
                  if len(p.relative_to(cfg.root).parts) == 1
                  and p.name not in cfg.root_allowed}
    # A1 scope: own-voice candidates only (library notes + root queue);
    # archives are reference material, a_sticker/or is AI-raw, doctrine is system.
    # Age = git first-commit time (creation), NOT mtime — mv/migration resets mtime.
    # The cheap filters run first so the git index is only consulted for notes that
    # already look half-done.
    first_seen = git_first_seen_index(cfg)
    for p in notes:
        rel = _rel(cfg, p)
        zone = cfg.zone(p)
        in_scope = rel.startswith(cfg.paths["library"] + "/") and zone \
            and zone.endswith(cfg.zones["node_suffix"])
        in_scope = bool(in_scope) or p in root_queue
        if not in_scope:
            continue
        if any(True for _ in parse.extract_wikilinks(g.notes[p])):
            continue
        if p.stem in todo_targets:
            continue
        created = first_seen.get(rel)
        if created is None:
            continue
        age_days = (now - created) / 86400
        if age_days > cfg.thresholds["halfdone_window_days"]:
            continue
        findings["halfdone"].append(
            f"疑似半成品: {rel} — git 创建 {int(age_days)} 天前, 零出链, 无 todo 挂钩 (A1)")

    # 4. unhooked notes in root queue without todo entry (S5 anti-loss)
    for p in sorted(root_queue):
        if p.stem not in todo_targets:
            findings["unhooked"].append(
                f"unhooked: {p.name} — root 队列且无 todo 挂钩 (S5)")

    # 5. genre placement: name says Raw/Index/Links but not in its home
    library_prefix = cfg.paths["library"] + "/"
    for p in notes:
        rel = _rel(cfg, p)
        if not rel.startswith(library_prefix) or len(p.relative_to(cfg.root).parts) < 3:
            continue
        gname = cfg.genre(p.stem)
        home = {"raw": cfg.zones["raw"], "index": cfg.zones["index"],
                "links": cfg.zones["links"]}.get(gname)
        sub = p.relative_to(cfg.root).parts[1]
        if home and sub != home:
            findings["genre"].append(f"体裁错位: {rel} ({gname} 应在 {cfg.paths['library']}/{home}/)")
        if gname == "node" and not sub.endswith(cfg.zones["node_suffix"]):
            findings["genre"].append(f"体裁错位: {rel} (node 应在 <fold>)")

    # 6. dead todo links
    basenames = g.resolvable()
    for p in sorted(cfg.todos_dir.glob("*.md")):
        text = g.notes[p]
        lines = text.splitlines()
        for target, line_no in parse.extract_wikilinks(text):
            if target in basenames or "Index of Todos" in str(p.name):
                continue
            if re.search(r"-\s*\[x\]", lines[line_no - 1], re.IGNORECASE):
                findings["dead_todo"].append(
                    f"dead todo reference: {p.name}:{line_no}: [[{target}]]")

    return findings


TRIAGE_CATEGORIES = ("root", "todo_stale", "halfdone", "unhooked", "genre", "dead_todo")


def cmd_triage(cfg: Config, g: model.Graph, args) -> int:
    findings = collect_triage(cfg, g)
    if wants_json(args):
        emit_json({"command": "triage", "version": __version__, "vault_root": str(cfg.root),
                   "counts": {c: len(findings[c]) for c in TRIAGE_CATEGORIES},
                   "findings": {c: findings[c] for c in TRIAGE_CATEGORIES},
                   "note": "mtime heuristic — treat as prompt, not verdict"})
        return 0
    print("# mtime heuristic — treat as prompt, not verdict\n")
    for category in TRIAGE_CATEGORIES:
        items = findings[category]
        print(f"# {category}: {len(items)}")
        for line in items:
            print(line)
        print()
    return 0


# ---------------------------------------------------------------- status


def _rhythm_line(cfg: Config) -> list:
    """B3+B7: 上次整理 / 聚簇 / 问箱 / 产出 — days since, git+mtime derived.

    整理 = last commit touching a_sticker/todos/* (todo grooming) or any
           library move commit; approximated by todos dir mtime + last
           commit touching todos.
    聚簇 = last commit touching library/Raw/ (registration = cluster output).
    问箱 = mtime of library/Links/ newest note (问箱产出直接落为 Links 卡, B4).
    产出 = last commit/mtime in zzz_output/ (B7 裁决: 手动创建即产出).
    """
    now = time.time()

    def days_since(paths: list) -> str:
        t = _git_last_commit(cfg, paths)
        mtimes = [p.stat().st_mtime for p in paths if p.exists()]
        if mtimes:
            t = max(mtimes) if t is None else max(t, max(mtimes))
        if t is None:
            return "—"
        d = int((now - t) / 86400)
        return f"{d} 天前" if d > 0 else "今天"

    return [
        f"上次整理: {days_since([cfg.todos_dir])}",
        f"上次聚簇: {days_since([cfg.raw_dir])}",
        f"上次问箱: {days_since([cfg.links_dir])}",
        f"上次产出: {days_since([cfg.zzz_dir])}",
    ]


def collect_status(cfg: Config, g: model.Graph) -> dict:
    """Everything `status` shows, as data — the base of `status --json`."""
    porcelain = _git_porcelain(cfg)
    check_rules = [{"id": rule["id"], "tier": rule["tier"], "title": rule["title"],
                    "count": len(rule["findings"])} for rule in collect_check(cfg, g)]
    triage = collect_triage(cfg, g)
    unreg = len(g.unregistered())
    zero = len(g.zero_outlink())

    moves = []
    if porcelain:
        moves.append("commit or tidy first (run `python3 tools/vault.py status` after)")
    if triage["root"]:
        moves.append(f"file me: {len(triage['root'])} root 笔记 — run triage, decide zone, move")
    if unreg:
        moves.append(f"聚簇: {unreg} 条未登记 — `python3 tools/vault.py rawindex --clusters`, "
                     "AI 归组进粗 Raw Index, 共性/命名你定 (D16)")
    if triage["todo_stale"]:
        moves.append(f"todo GC: {len(triage['todo_stale'])} 个 todo "
                     f">{cfg.thresholds['todo_stale_days']} 天未动 — review / resolve / archive (B1)")
    if triage["halfdone"]:
        moves.append(f"疑似半成品: {len(triage['halfdone'])} — 挂 todo 或补完 (A1)")
    if triage["unhooked"]:
        moves.append(f"unhooked root queue: {len(triage['unhooked'])} — todo-hook (S5)")
    if triage["genre"]:
        moves.append(f"体裁错位: {len(triage['genre'])} — name > path, 搬家归位")
    if triage["dead_todo"]:
        moves.append(f"dead todo references: {len(triage['dead_todo'])} — clean up")
    if zero:
        moves.append(f"零出链 {zero} — 捕获时 AI 给 3 候选链接 (S2); 存量靠 I3 增量,不设硬门 (B5)")
    if not moves:
        moves.append("vault clean — new capture (S2), 聚簇, or 问箱 available")

    return {
        "rhythm": _rhythm_line(cfg),
        "porcelain": porcelain,
        "check": check_rules,
        "triage": {c: len(triage[c]) for c in TRIAGE_CATEGORIES},
        "trunk": {"nodes": len(g.nodes), "raw_index": len(g.raws), "index": len(g.idxs),
                  "links": len(g.linksn), "registered": len(g.nodes) - unreg,
                  "queue": unreg, "zero_outlink": zero},
        "zzz_changes": [ln.strip() for ln in (porcelain or []) if "zzz_output/" in ln],
        "next_moves": moves,
    }


def status_json(cfg: Config, data: dict) -> dict:
    """`status --json` — the self-bootstrapping payload an AI needs."""
    return {
        "command": "status",
        "version": __version__,
        "vault_root": str(cfg.root),
        "contract": "doctrine/Agent Contract.md",
        "state_location": cfg.paths["todos"] + "/ (the todo tree is the only state store)",
        "rhythm": dict(zip(("整理", "聚簇", "问箱", "产出"), data["rhythm"])),
        "git": {
            "available": data["porcelain"] is not None,
            "clean": data["porcelain"] == [],
            "entries": data["porcelain"] or [],
        },
        "check": data["check"],
        "triage": data["triage"],
        "trunk": data["trunk"],
        "zzz_output": {"changed_files": len(data["zzz_changes"])},
        "next_moves": data["next_moves"],
        "exit_codes": EXIT_CODES,
    }


def cmd_status(cfg: Config, g: model.Graph, args) -> int:
    """Session-entry state report: rhythm + git + check summary + triage counts + next moves."""
    data = collect_status(cfg, g)
    if wants_json(args):
        emit_json(status_json(cfg, data))
        return 0

    porcelain = data["porcelain"]
    print("# vault status — session entry report (read-only)\n")

    # (0) rhythm line (B3+B7)
    print("## 节律 (B3+B7 — 停摆可见 = 停摆可治)")
    for line in data["rhythm"]:
        print(f"- {line}")
    print()

    # (a) git state
    print("## git")
    if porcelain is None:
        print("git: unavailable")
    elif not porcelain:
        print("clean")
    else:
        untracked = sum(1 for ln in porcelain if ln.startswith("??"))
        print(f"{len(porcelain)} entries ({untracked} untracked)")
        for ln in porcelain[:10]:
            print(f"  {ln.strip()}")
        if len(porcelain) > 10:
            print(f"  … ({len(porcelain) - 10} more)")

    # (b) check two-tier summary
    print("\n## check (two-tier summary)")
    for rule in data["check"]:
        state = "OK" if not rule["count"] else f"{rule['count']} findings"
        print(f"- [{rule['tier']}] {rule['title']}: {state}")

    # (c) triage counts
    triage = data["triage"]
    print("\n## triage (counts)")
    print(f"- root files: {triage['root']}")
    print(f"- todo 老化 (> {cfg.thresholds['todo_stale_days']} 天): {triage['todo_stale']}")
    print(f"- 疑似半成品 (≤{cfg.thresholds['halfdone_window_days']} 天 + 零出链 + 零挂钩): "
          f"{triage['halfdone']}")
    print(f"- unhooked root queue: {triage['unhooked']}")
    print(f"- 体裁错位: {triage['genre']}")
    print(f"- dead todo references: {triage['dead_todo']}")

    # (d) trunk summary
    trunk = data["trunk"]
    print("\n## 主干 (trunk)")
    print(f"- nodes {trunk['nodes']} | Raw Index {trunk['raw_index']} | "
          f"Index {trunk['index']} | Links {trunk['links']}")
    print(f"- queue (未登记): {trunk['queue']} — `vault.py rawindex` gives L0 归队提议")
    print(f"- 零出链: {trunk['zero_outlink']}/{trunk['nodes']} — I3 报告级增量 (B5)")

    # (e) zzz_output git-state (content never read)
    print("\n## zzz_output (owner's terminal output — git-state only)")
    if data["zzz_changes"]:
        print(f"unpublished-output changes: {len(data['zzz_changes'])} files")
    else:
        print("no uncommitted changes")

    # next moves
    print("\n## next moves")
    for i, move in enumerate(data["next_moves"], 1):
        print(f"{i}. {move}")
    return 0


# ---------------------------------------------------------------- main


HELP_TOPICS = {
    "triage": """triage — placement debt (read-only)

    python3 tools/vault.py triage [--json]

Six categories, all mtime/edge heuristics — treat as prompt, not verdict:
  root        root files beyond the ones allowed in tools/vault.toml (root is the
              entry queue)
  todo_stale  todo notes untouched beyond todo_stale_days (file-level mtime, top
              scan only; a_sticker/todos/archived/ is exempt)
  halfdone    created within halfdone_window_days + zero outlink + no todo hook (A1)
  unhooked    root-queue note with no todo hook (S5 anti-loss)
  genre       name says Raw Index* / Index of* / Links of* but the file is not in
              its home zone; `-MOC` also counts as index; `a_sticker/todos/Index
              of Todos.md` is the todo-tree register (genre exception)
  dead_todo   `- [x]` reference to a name that does not resolve

All thresholds: tools/vault.toml. Nothing is written; `status` shows the same
counts inline.""",
    "rawindex": """rawindex — trunk operations

    python3 tools/vault.py rawindex [--clusters] [--check] [--sync [--apply]]
                                    [--around NAME] [--top N] [--json]

  (no flag)    queue + L0 affiliation proposals: for every unregistered Node, the
               Raw Index its neighbors' registrations vote for. Proposals at or
               above l0_confidence (tools/vault.toml) may be appended directly (D22).
  --clusters   L1 direct-interlink components, L2 shared-neighbor clusters at
               theta = cluster_theta_percentile (binding evidence = common
               neighbors), L3 isolated points. Group clusters into coarse Raw
               Indexes — never one Raw Index per cluster (D10-P3).
  --check      the report-level rules again, from the same registry `check` uses
               (I1a/I1b/I1c, I2, I3, D21).
  --sync       dry-run: prints the intended `## Core Concepts` member list of
               `Raw Index of Everything`. Add --apply to write (L13 write safety).
  --around     one note's registrations, Index areas, in/out links and binding
               neighbors. Unknown name: exit 1 with did-you-mean.
  --top        L0 proposals to show (default rawindex_top in tools/vault.toml).""",
    "dag": """dag — why the trunk is a DAG, not a tree

The trunk is `Raw Index -> Node` registration edges:
  - every Node needs >=1 registration edge (I1a 未登记 reports the queue);
  - the same (Raw Index, Node) pair may not appear twice (I1b 重复登记边);
  - a Node MAY be registered by several Raw Indexes — uniqueness lives in the
    edge, not in the parent (multiple parents are legal since v6);
  - `Raw Index -> Raw Index` must stay acyclic (I1c). Peeling nodes without an
    in- or out-edge leaves exactly the union of all cycles.
Registration edges are structural: AI may append them directly (D22).
`Node <-> Node` and `Index -> Node` links change meaning and need owner approval.
See doctrine/Vault Design.md ("登记是边，不是父").""",
    "links": """links — Links notes

`library/Links/Links of X.md` is where a cross-cutting insight becomes a card.
  - a Links note must span >= 2 Index areas; same-area is a violation, no-area is
    a hint (I2, report-level);
  - Links notes are the natural output of 问箱 (S9): a random note plus its
    backlinks, then the link you actually found;
  - `Links of X` is a genre: name prefix `Links ` decides the zone, not the path.

    python3 tools/vault.py random --scope library   # 问箱 material
    python3 tools/vault.py suggest "Group"          # 3 candidate links + why""",
    "random": """random — 问箱 material (S9)

    python3 tools/vault.py random [--scope nodes|library|all] [--seed N] [--json]

Picks one note and prints its backlinks and outlinks. `--seed` makes the draw
reproducible. Scopes: `nodes` (default: every Node, i.e. a `<fold>` note),
`library` (anything under library/), `all` (every scanned note).
Signal only — the tool never writes a note.""",
    "suggest": """suggest — candidate links for a note (S2)

    python3 tools/vault.py suggest NAME [--n 3] [--json]

Ranks other notes by evidence and prints one why-line each:
  - shared binding neighbors (doctrine and Raw Index notes excluded, I4),
  - then same registration edge, then same Index area.
Notes already linked (either direction) are skipped. Unknown name: exit 1.
Signal only — the owner picks, the tool never writes a link.""",
}


def print_help(topic: str | None) -> int:
    if topic in HELP_TOPICS:
        print(HELP_TOPICS[topic])
        return 0
    if topic:
        print(f"unknown help topic: {topic}")
        print("topics: " + " / ".join(sorted(HELP_TOPICS)))
        return 2
    print(__doc__ or "vaultkit")
    print("help topics: " + " / ".join(sorted(HELP_TOPICS)))
    print("use `vault.py help <topic>`; exit codes: " + "; ".join(
        f"{k} {v}" for k, v in EXIT_CODES.items()))
    return 0


def build_parser() -> argparse.ArgumentParser:
    # --strict / --json are accepted both before and after the subcommand.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--strict", action="store_true", default=argparse.SUPPRESS,
                        help="missing config / list files are fatal (exit 2), not warnings")
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS,
                        help="machine-readable output (one JSON document on stdout)")

    parser = argparse.ArgumentParser(
        description="Vault operating procedures (v6)",
        epilog=("exit codes: 0 = ok (all reports, and any check with green hard gates); "
                "1 = hard gate failed (check) or unknown target (rawindex --around / suggest); "
                "2 = missing/unreadable config (or a missing list file under --strict). "
                "Topics: `vault.py help triage|rawindex|dag|links|random|suggest`."),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strict", action="store_true", default=argparse.SUPPRESS,
                        help="missing config / list files are fatal (exit 2), not warnings")
    parser.add_argument("--json", action="store_true", default=argparse.SUPPRESS,
                        help="machine-readable output (one JSON document on stdout)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", parents=[common],
                   help="two-tier invariant report: hard gates exit 1, I1–I4 report-level")
    sub.add_parser("triage", parents=[common],
                   help="placement-debt report: root, todo aging, suspected half-done (read-only)")
    sub.add_parser("status", parents=[common],
                   help="session entry: rhythm line + git + check + triage + trunk + next moves (read-only)")

    p_help = sub.add_parser("help", help="topic help: " + " / ".join(sorted(HELP_TOPICS)))
    p_help.add_argument("topic", nargs="?", default=None)

    p_rand = sub.add_parser("random", parents=[common],
                            help="random note + backlinks (S9 问箱 material)")
    p_rand.add_argument("--scope", choices=("nodes", "library", "all"), default="nodes",
                        help="which notes to draw from (default nodes)")
    p_rand.add_argument("--seed", type=int, default=None, help="reproducible draw")

    p_sug = sub.add_parser("suggest", parents=[common],
                           help="candidate links for a note (S2)")
    p_sug.add_argument("name", help="note name (stem)")
    p_sug.add_argument("--n", type=int, default=3, help="candidates to show (default 3)")

    p_raw = sub.add_parser("rawindex", parents=[common],
                           help="trunk operations: queue + L0 归队提议")
    p_raw.add_argument("--clusters", action="store_true",
                       help="L1/L2 clusters + binding evidence + grouping advice")
    p_raw.add_argument("--check", action="store_true", help="I1–I3 + material 未拆 report")
    p_raw.add_argument("--sync", action="store_true",
                       help="B6: rewrite the trunk root member list (dry-run unless --apply)")
    p_raw.add_argument("--apply", action="store_true",
                       help="with --sync: actually write the trunk root (default: dry-run)")
    p_raw.add_argument("--around", metavar="NAME", help="one node's neighborhood")
    p_raw.add_argument("--top", type=int, default=None, help="L0 proposals to show (default 10)")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "help":
        return print_help(args.topic)
    try:
        cfg = load_config(strict=getattr(args, "strict", False))
    except ConfigError as exc:
        print(f"ERROR: {exc}")
        return 2
    for warning in cfg.warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    if args.command == "rawindex" and args.top is None:
        args.top = cfg.thresholds["rawindex_top"]
    g = model.load(cfg)
    if args.command == "check":
        return cmd_check(cfg, g, args)
    if args.command == "triage":
        return cmd_triage(cfg, g, args)
    if args.command == "status":
        return cmd_status(cfg, g, args)
    if args.command == "random":
        return cmd_random(cfg, g, args)
    if args.command == "suggest":
        return cmd_suggest(cfg, g, args)
    return cmd_rawindex(cfg, g, args)


if __name__ == "__main__":
    sys.exit(main())
