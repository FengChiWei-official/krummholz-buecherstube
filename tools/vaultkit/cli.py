"""Command shells: thin renderers over config/model/parse.

No parsing, no graph building and no thresholds live here — commands read the
shared `Graph` and print.
"""

from __future__ import annotations

import argparse
import collections
import math
import re
import subprocess
import sys
import time
from itertools import combinations
from pathlib import Path

from . import model, parse
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


def _git_first_seen(cfg: Config, path: Path):
    """First commit time a path was tracked, or None. Creation time that
    survives moves/migrations (unlike mtime)."""
    rel = path.relative_to(cfg.root).as_posix()
    out = _git(cfg.root, ["log", "--diff-filter=A", "--follow", "--format=%ct", "--", rel])
    if out is None:
        return None
    stamps = [ln for ln in out.splitlines() if ln.strip()]
    return float(stamps[-1]) if stamps else None


def _git_last_commit(cfg: Config, paths: list) -> float:
    """mtime of the last commit touching any of `paths`, else 0."""
    for p in paths:
        out = _git(cfg.root, ["log", "-1", "--format=%ct", "--", str(p)])
        if out and out.strip():
            return float(out.strip())
    return 0.0


def _git_porcelain(cfg: Config):
    """git status --porcelain lines, or None when git/repo is unavailable."""
    out = _git(cfg.root, ["status", "--porcelain"])
    if out is None:
        return None
    return [ln for ln in out.splitlines() if ln.strip()]


# ---------------------------------------------------------------- render helpers


def report(title: str, findings: list) -> bool:
    print(f"## {title}")
    if findings:
        for item in findings:
            print(f"  {item}")
    else:
        print("  OK — no violations")
    print()
    return bool(findings)


def _rel(cfg: Config, path: Path) -> str:
    return path.relative_to(cfg.root).as_posix()


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
    problems = 0
    print("# vault check — two-tier (D20): hard gates exit 1; I1–I4 report-level\n")
    for tier, title, findings in collect_check(cfg, g):
        if tier == "gate":
            if report(title, findings):
                problems += 1
        elif tier == "report":
            print(f"## {title}")
            for item in findings:
                print(f"  {item}")
            print()
        else:
            report(title, findings)
    print("CLEAN — hard gates hold; report-level numbers above are weekly increments"
          if problems == 0 else f"PROBLEMS: {problems} (hard gates failed)")
    return 1 if problems else 0


# ---------------------------------------------------------------- rawindex


def _rawindex_check(cfg: Config, g: model.Graph) -> None:
    queue = g.unregistered()
    multi = g.multi_registered()
    print("\n## I1 每个 Node 恰好登记在一个 Raw Index")
    print(f"  未登记: {len(queue)}   多重登记: {len(multi)}")
    for stem, rs in sorted(multi.items())[:5]:
        print(f"    {stem}: {rs}")
    print("\n## I2 Links 必须横跨 >=2 个 Index 区域")
    area = g.area
    intra, cross, noarea = [], [], []
    for L in g.linksn:
        mem = [q for q in g.out[L] if q in area]
        ar = set().union(*[area[q] for q in mem]) if mem else set()
        (cross if len(ar) >= 2 else (intra if ar else noarea)).append((L, len(mem), len(ar)))
    print(f"  跨界 {len(cross)} | 同区域 {len(intra)}(违规) | 无区域 {len(noarea)}(提示)")
    for L, m, x in intra[:6]:
        print(f"    同区域: {L.stem} ({m} 成员, {x} 区域)")
    print("\n## I3 Node 必须 >=1 条出链（捕获规则）")
    zero = g.zero_outlink()
    print(f"  零出链: {len(zero)}/{len(g.nodes)}  "
          f"({len(zero)*100//max(1,len(g.nodes))}%)")
    print("\n## 材料 出链=已拆 (D21)")
    material_prefix = cfg.paths["archives_material"] + "/"
    materials = [p for p in g.notes
                 if _rel(cfg, p).startswith(material_prefix) and p.suffix == ".md"]
    unsplit = [p for p in materials if not g.out[p]]
    print(f"  未拆材料: {len(unsplit)}/{len(materials)}  (零出链 = 未拆)")
    for p in unsplit[:8]:
        print(f"    {_rel(cfg, p)}")


def _rawindex_sync(cfg: Config, g: model.Graph) -> int:
    """B6: maintain the trunk root's member list (registration edges).

    Structural action per D22 — AI may append directly. The root's
    `## Core Concepts` section lists one [[Node]] line per registered member
    grouped under each child Raw Index; existing prose is left alone.
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
    root_note.write_text(new, encoding="utf-8")
    print(f"rawindex --sync: {cfg.trunk_root_stem} — {len(children)} child Raw Indexes "
          "registered")
    for ln in lines[:10]:
        print(f"  {ln}")
    if len(lines) > 10:
        print(f"  … ({len(lines) - 10} more)")
    return 0


def _rawindex_around(cfg: Config, g: model.Graph, nbr: dict, name: str) -> int:
    """One node's neighborhood: registrations, areas, links, neighbors."""
    target = g.stems.get(name)
    if target is None:
        low = name.lower()
        cands = [s for s in g.stems if low in s.lower()][:10]
        print(f"rawindex --around: `{name}` not found.")
        if cands:
            print("  did you mean: " + " / ".join(cands))
        return 1
    print(f"## {target.stem}")
    print(f"  path: {_rel(cfg, target)}")
    if target in g.reg:
        print(f"  登记: {[r.stem for r in sorted(g.reg[target], key=lambda p: p.stem)]}")
    else:
        print("  登记: (queue — 未登记)")
    if target in g.area:
        print(f"  区域: {[i.stem for i in sorted(g.area[target], key=lambda p: p.stem)]}")
    outs = g.out.get(target, set())
    print(f"  出链 {len(outs)}: {[q.stem for q in sorted(outs, key=lambda p: p.stem)][:12]}")
    ins = [p for p, qs in g.out.items() if target in qs]
    print(f"  入链 {len(ins)}: {[p.stem for p in sorted(ins, key=lambda p: p.stem)][:12]}")
    nb = nbr.get(target, set())
    print(f"  邻居 {len(nb)} (绑定证据候选: "
          f"{[p.stem for p in sorted(nb, key=lambda p: p.stem)][:8]})")
    return 0


def cmd_rawindex(cfg: Config, g: model.Graph, args) -> int:
    """Trunk operations: queue + L0 proposals; --clusters / --check / --sync / --around."""
    out, reg = g.out, g.reg
    nodes, raws = g.nodes, g.raws
    nbr = g.neighbors()

    registered = [n for n in nodes if reg[n]]
    queue = [n for n in nodes if not reg[n]]
    print(f"nodes {len(nodes)} | Raw Index {len(raws)} | Index {len(g.idxs)} "
          f"| Links {len(g.linksn)}")
    print(f"registered {len(registered)} | queue {len(queue)}")

    if args.check:
        _rawindex_check(cfg, g)

    if args.sync:
        _rawindex_sync(cfg, g)

    if args.around:
        return _rawindex_around(cfg, g, nbr, args.around)

    # ---------------- L0: affiliation proposals for the queue
    print(f"\n## L0 归队提议（队列 {len(queue)} 条中，能定归属的）")
    props = []
    for v in queue:
        nb = nbr[v]
        if not nb:
            continue
        sc = collections.Counter()
        for z in nb:
            for r in reg.get(z, ()):
                sc[r] += 1
        if sc:
            r, n = min(sc.items(), key=lambda kv: (-kv[1], kv[0].stem))
            props.append((n / len(nb), n, len(nb), v, r))
    props.sort(reverse=True)
    for s, n, tot, v, r in props[:args.top]:
        print(f"  {s:.0%} ({n}/{tot})  {v.stem}  ->  {r.stem}")
    if props:
        conf = sum(1 for p in props if p[0] >= cfg.thresholds["l0_confidence"])
        print(f"\n  ≥90% 置信的提议: {conf} 条 — 登记边是结构动作, AI 可直接追加 (D22); "
              "其余照人机分工: 共性/命名你定 (D16)")

    if args.clusters:
        _rawindex_clusters(cfg, g, nbr, queue)

    return 0


def _rawindex_clusters(cfg: Config, g: model.Graph, nbr: dict, queue: list) -> None:
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
    print(f"\n## L1 直接互链粗簇: {len(comps)} 个, 覆盖 {len(seen)}/{len(Q)}")
    for c in comps[:6]:
        print(f"  ({len(c)}) " + " / ".join(sorted(x.stem for x in c)[:6]))

    z2u: dict = collections.defaultdict(set)
    for v in sorted(Q):
        for z in sorted(nbr[v]):
            z2u[z].add(v)
    w: dict = collections.defaultdict(float)
    ev: dict = collections.defaultdict(collections.Counter)
    for z in sorted(z2u):
        us = sorted(z2u[z])
        if len(us) < 2:
            continue
        inc = 1.0 / math.log(max(3, len(nbr[z]) + 1))
        for x, y in combinations(us, 2):
            w[(x, y)] += inc
            ev[(x, y)][z.stem] += 1
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
    print(f"\n## L2 共享邻居细分 θ=P97={th:.2f}: {len(cs)} 簇, "
          f"最大 {len(cs[0]) if cs else 0}")
    for c in cs[:5]:
        sh = collections.Counter()
        for x, y in combinations(sorted(c), 2):
            sh.update(nbr[x] & nbr[y])
        print(f"  ({len(c)}) " + " / ".join(sorted(x.stem for x in c)[:5]))
        top = sorted(sh.items(), key=lambda kv: (-kv[1], kv[0].stem))[:3]
        print(f"      绑定证据: {[s.stem for s, _ in top]}")
    print(f"\n## L3 孤点: {len(Q) - len(seen | seen2)}")
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

    # 2. todo aging (B1): todo-note entries untouched > 90 days
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
    for p in notes:
        rel = _rel(cfg, p)
        zone = cfg.zone(p)
        in_scope = rel.startswith(cfg.paths["library"] + "/") and zone \
            and zone.endswith(cfg.zones["node_suffix"])
        in_scope = bool(in_scope) or p in root_queue
        if not in_scope:
            continue
        created = _git_first_seen(cfg, p)
        if created is None:
            continue
        age_days = (now - created) / 86400
        if age_days > cfg.thresholds["halfdone_window_days"]:
            continue
        has_out = any(True for _ in parse.extract_wikilinks(g.notes[p]))
        if not has_out and p.stem not in todo_targets:
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


def cmd_triage(cfg: Config, g: model.Graph, args) -> int:
    findings = collect_triage(cfg, g)
    print("# mtime heuristic — treat as prompt, not verdict\n")
    for category in ("root", "todo_stale", "halfdone", "unhooked", "genre", "dead_todo"):
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
        for p in paths:
            if p.exists():
                t = max(t, p.stat().st_mtime)
        if not t:
            return "从未"
        d = int((now - t) / 86400)
        return f"{d} 天前" if d > 0 else "今天"

    return [
        f"上次整理: {days_since([cfg.todos_dir])}",
        f"上次聚簇: {days_since([cfg.raw_dir])}",
        f"上次问箱: {days_since([cfg.links_dir])}",
        f"上次产出: {days_since([cfg.zzz_dir])}",
    ]


def cmd_status(cfg: Config, g: model.Graph, args) -> int:
    """Session-entry state report: rhythm + git + check summary + triage counts + next moves."""
    print("# vault status — session entry report (read-only)\n")

    # (0) rhythm line (B3+B7)
    print("## 节律 (B3+B7 — 停摆可见 = 停摆可治)")
    for line in _rhythm_line(cfg):
        print(f"- {line}")
    print()

    # (a) git state
    porcelain = _git_porcelain(cfg)
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
    for tier, title, findings in collect_check(cfg, g):
        state = "OK" if not findings else f"{len(findings)} findings"
        print(f"- [{tier}] {title}: {state}")

    # (c) triage counts
    triage = collect_triage(cfg, g)
    print("\n## triage (counts)")
    print(f"- root files: {len(triage['root'])}")
    print(f"- todo 老化 (> {cfg.thresholds['todo_stale_days']} 天): {len(triage['todo_stale'])}")
    print(f"- 疑似半成品 (≤{cfg.thresholds['halfdone_window_days']} 天 + 零出链 + 零挂钩): "
          f"{len(triage['halfdone'])}")
    print(f"- unhooked root queue: {len(triage['unhooked'])}")
    print(f"- 体裁错位: {len(triage['genre'])}")
    print(f"- dead todo references: {len(triage['dead_todo'])}")

    # (d) trunk summary
    print("\n## 主干 (trunk)")
    print(f"- nodes {len(g.nodes)} | Raw Index {len(g.raws)} | "
          f"Index {len(g.idxs)} | Links {len(g.linksn)}")
    unreg = len(g.unregistered())
    print(f"- queue (未登记): {unreg} — `vault.py rawindex` gives L0 归队提议")
    zero = len(g.zero_outlink())
    print(f"- 零出链: {zero}/{len(g.nodes)} — I3 报告级增量 (B5)")

    # (e) zzz_output git-state (content never read)
    zzz_changes = [ln.strip() for ln in (porcelain or []) if "zzz_output/" in ln]
    print("\n## zzz_output (owner's terminal output — git-state only)")
    if zzz_changes:
        print(f"unpublished-output changes: {len(zzz_changes)} files")
    else:
        print("no uncommitted changes")

    # next moves
    print("\n## next moves")
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
    for i, move in enumerate(moves, 1):
        print(f"{i}. {move}")
    return 0


# ---------------------------------------------------------------- main


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Vault operating procedures (v6)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check",
                   help="two-tier invariant report: hard gates exit 1, I1–I4 report-level")
    sub.add_parser("triage",
                   help="placement-debt report: root, todo aging, suspected half-done (read-only)")
    sub.add_parser("status",
                   help="session entry: rhythm line + git + check + triage + trunk + next moves (read-only)")

    p_raw = sub.add_parser("rawindex", help="trunk operations: queue + L0 归队提议")
    p_raw.add_argument("--clusters", action="store_true",
                       help="L1/L2 clusters + binding evidence + grouping advice")
    p_raw.add_argument("--check", action="store_true", help="I1–I3 + material 未拆 report")
    p_raw.add_argument("--sync", action="store_true",
                       help="B6: maintain trunk root member list (structural, D22)")
    p_raw.add_argument("--around", metavar="NAME", help="one node's neighborhood")
    p_raw.add_argument("--top", type=int, default=None, help="L0 proposals to show (default 10)")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        cfg = load_config()
    except ConfigError as exc:
        print(f"ERROR: {exc}")
        return 2
    if args.command == "rawindex" and args.top is None:
        args.top = cfg.thresholds["rawindex_top"]
    g = model.load(cfg)
    if args.command == "check":
        return cmd_check(cfg, g, args)
    if args.command == "triage":
        return cmd_triage(cfg, g, args)
    if args.command == "status":
        return cmd_status(cfg, g, args)
    return cmd_rawindex(cfg, g, args)


if __name__ == "__main__":
    sys.exit(main())
