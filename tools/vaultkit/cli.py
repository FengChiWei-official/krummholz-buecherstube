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
    "1": "hard gate failed (check), unknown target (place / suggest), "
         "a refused rename or a refused new, or a docs-sync violation under docs-check --gate",
    "2": "missing or unreadable config (also a missing list file under --strict)",
}


# ---------------------------------------------------------------- check


def cmd_check(cfg: Config, g: model.Graph, args) -> int:
    """Render every `check` rule from the registry (rules.py)."""
    ctx = rules.Context(cfg=cfg, graph=g)
    problems = 0
    payload_rules = []
    if not wants_json(args):
        print("# vault check — two-tier (D20): hard gates exit 1; report-level rules give increments\n")
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


# ---------------------------------------------------------------- place


def _vote_evidence(g: model.Graph, nbr: dict, target) -> list:
    """[{raw, votes, of, score, via}] — which Raw Indexes the neighborhood votes for.

    The DAG reading of "where does this belong": a Node's position is decided by
    the registrations of the notes around it. `via` names the voters, so the
    proposal can always be traced back to evidence (never a guess).
    """
    neighbours = nbr.get(target, set())
    votes: dict = collections.defaultdict(list)
    for z in neighbours:
        for r in g.reg.get(z, ()):
            votes[r].append(z)
    out = []
    for r, voters in votes.items():
        names = sorted(q.stem for q in voters)
        out.append({"raw": r.stem, "votes": len(voters), "of": len(neighbours),
                    "score": round(len(voters) / len(neighbours), 4) if neighbours else 0.0,
                    "via": names[:6]})
    out.sort(key=lambda d: (-d["votes"], d["raw"]))
    return out


def _role_of(g: model.Graph, cfg: Config, path) -> str:
    if path in set(g.raws):
        return "raw"
    if path in set(g.idxs):
        return "index"
    if path in set(g.linksn):
        return "links"
    if path in set(g.doctrine):
        return "doctrine"
    rel = g.rel(path)
    if rel.startswith(cfg.paths["archives_material"] + "/"):
        return "material"
    if rel.startswith(cfg.paths["todos"] + "/"):
        return "todo"
    if path in set(g.nodes):
        return "node"
    return "other"


def collect_place(cfg: Config, g: model.Graph, name: str) -> dict:
    """Where one note sits in the relation graph, and where it could sit.

    Read-only: it reports registrations, the neighborhood's voting evidence for
    further registration (the trunk is a DAG — several registration edges are
    legal), the semantic areas, the links, and the notes worth linking first.
    """
    data = {"command": "place", "target": name, "found": False, "did_you_mean": [],
            "stem": None, "path": None, "alias_of": None, "role": None, "genre": None,
            "zone": None, "registered": [], "proposals": [], "areas": [],
            "outlinks": [], "inlinks": [], "link_candidates": [], "signals": [],
            "note": None}
    target = g.resolve(name)
    if target is None:
        low = name.lower()
        data["did_you_mean"] = sorted(
            [s for s in g.stems if low in s.lower()]
            + [a for a in g.aliases if low in a.lower()])[:10]
        data["note"] = ("库里没有这个名字，图里也就没有它的位置——先 `vault.py new` 建一篇、"
                        "当场链 ≥1 篇旧笔记（S2），再跑 place 就有归队提议了")
        return data

    data["found"] = True
    data["stem"] = target.stem
    data["path"] = g.rel(target)
    data["role"] = _role_of(g, cfg, target)
    data["genre"] = cfg.genre(target.stem)
    data["zone"] = cfg.zone(target) or ""
    if name != target.stem and name in g.aliases:
        data["alias_of"] = target.stem

    nbr = g.binding_neighbors()
    data["registered"] = sorted(r.stem for r in g.reg.get(target, ()))
    proposals = _vote_evidence(g, nbr, target)
    data["proposals"] = proposals
    data["areas"] = sorted(i.stem for i in g.area.get(target, ()))
    data["outlinks"] = sorted(q.stem for q in g.out.get(target, ()))
    data["inlinks"] = sorted(p.stem for p, qs in g.out.items() if target in qs)
    data["link_candidates"] = [{"note": q.stem, "why": why}
                               for q, why in suggest_candidates(cfg, g, target, 3)]

    if data["role"] == "node" and not data["registered"]:
        data["signals"].append("未登记（I1a）——从上面的提议里挑一条追加登记边（D22，结构动作）")
    if data["role"] == "node" and not data["outlinks"]:
        data["signals"].append("零出链（I3）——捕获时至少链 1 篇旧笔记（S2）")
    if data["role"] == "raw":
        if target in set(g.raw_index_cycle_core()):
            data["signals"].append("在环上（I1c）——`Raw Index → Raw Index` 子图必须无环")
        parents = sorted(r.stem for r in g.raws if target in g.out.get(r, ()))
        if parents:
            data["signals"].append("被登记为子主干: " + ", ".join(parents))
    if data["role"] == "material" and not data["outlinks"]:
        data["signals"].append("未拆（D21）——材料被拆过的标记 = 有指向所拆 Node 的出链")
    if not data["inlinks"]:
        data["signals"].append("零入链——没有笔记指向它（先链别人，别人回链由你决定）")
    return data


def _render_place(cfg: Config, data: dict) -> None:
    if not data["found"]:
        print(f"# vault place — {data['target']}")
        print(f"  {data['note']}")
        if data["did_you_mean"]:
            print("  did you mean: " + " / ".join(data["did_you_mean"]))
        return
    print(f"# vault place — {data['stem']}")
    alias = f"  (经别名 `{data['target']}` 命中)" if data["alias_of"] else ""
    print(f"  在库: {data['path']}{alias}")
    print(f"  角色: {data['role']} | 体裁 {data['genre']} | 分区 {data['zone'] or '(root)'}")
    if data["registered"]:
        print(f"  登记于 {len(data['registered'])} 条边: {', '.join(data['registered'])}"
              "   ← DAG 允许 >1 条登记边")
    else:
        print("  登记: (queue — 未登记)")
    if data["proposals"]:
        print(f"  归队提议（邻居投票，{len(data['proposals'])} 个候选）:")
        for prop in data["proposals"][:5]:
            mark = "  ✓ 已登记" if prop["raw"] in data["registered"] else ""
            print(f"    {prop['score']:.0%} ({prop['votes']}/{prop['of']})  {prop['raw']}"
                  f"   ← via {', '.join(prop['via'])}{mark}")
    else:
        print("  归队提议: 无——邻居都没登记，先让周围几篇归队")
    if data["areas"]:
        print(f"  语义区域: {', '.join(data['areas'])}")
    print(f"  出链 {len(data['outlinks'])}: {data['outlinks'][:8]}")
    print(f"  入链 {len(data['inlinks'])}: {data['inlinks'][:8]}")
    if data["link_candidates"]:
        print("  先链这几篇（S2 候选，含 why）:")
        for i, cand in enumerate(data["link_candidates"], 1):
            print(f"    {i}. [[{cand['note']}]] — {cand['why']}")
    else:
        print("  先链候选: 无（周围还没有可投票的证据）")
    for signal in data["signals"]:
        print(f"  ⚠ {signal}")


def cmd_place(cfg: Config, g: model.Graph, args) -> int:
    """One note's position in the relation graph (read-only)."""
    data = collect_place(cfg, g, args.name)
    if wants_json(args):
        emit_json(data)
        return 0 if data["found"] else 1
    _render_place(cfg, data)
    return 0 if data["found"] else 1


# ---------------------------------------------------------------- links-candidates


def _area_names(g, path) -> set:
    return {i.stem for i in g.area.get(path, ())}


def _raw_names(g, path) -> set:
    return {r.stem for r in g.reg.get(path, ())}


def _links_evidence(g, nbr, path, seed, topic) -> tuple:
    """(score, why) — how strongly `path` belongs on a Links card seeded by `seed`.

    Evidence is graded, because a bare shared Index area is nearly meaningless in
    a large area: name/alias hit 3, a link to or from the seed 2, a shared Raw
    Index registration 2, a shared binding neighbour 1, a bare shared area 0
    (reported but never a membership reason).
    """
    low = topic.strip().lower()
    if low and (low in path.stem.lower()
                or any(low in a.lower() for a in _aliases_of(g, path))):
        return 3, f"名字含 `{topic}`"
    if seed is not None:
        if seed in g.out.get(path, ()):
            return 2, f"链到种子 [[{seed.stem}]]"
        if path in g.out.get(seed, ()):
            return 2, f"被种子 [[{seed.stem}]] 链"
        shared_raw = _raw_names(g, path) & _raw_names(g, seed)
        if shared_raw:
            return 2, f"同登记: {sorted(shared_raw)[0]}"
        shared = nbr.get(path, set()) & nbr.get(seed, set())
        if shared:
            names = " / ".join(p.stem for p in sorted(shared, key=lambda p: p.stem)[:3])
            return 1, f"共同邻居 {len(shared)}: {names}"
        shared_area = _area_names(g, path) & _area_names(g, seed)
        if shared_area:
            return 0, f"仅同区域: {sorted(shared_area)[0]}"
    return -1, ""


def _aliases_of(g, path) -> list:
    return sorted(a for a, p in g.aliases.items() if p == path)


def collect_links_candidates(cfg: Config, g: model.Graph, topic: str, n: int = 12) -> dict:
    """Candidate members of a Links card about `topic`, grouped by Index area.

    Doctrine: a Links card is one concept seen from several angles and must cross
    ≥2 Index areas. The tool proposes the member list and the shared evidence per
    member; the name and the commonality sentence stay the owner's (D16).
    """
    data = {"command": "links-candidates", "topic": topic, "found": False,
            "did_you_mean": [], "seeds": [], "areas": [], "groups": [],
            "members": [], "area_count": 0, "crosses_areas": False,
            "card_name_candidates": [], "warnings": []}
    low = topic.strip().lower()
    if not low:
        data["warnings"].append("主题为空")
        return data

    seeds = sorted((p for p in g.notes
                    if low in p.stem.lower() or any(low in a.lower() for a in _aliases_of(g, p))),
                   key=lambda p: p.stem)
    if not seeds:
        data["did_you_mean"] = sorted(
            {s for s in g.stems if low[:3] in s.lower()}
            | {a for a in g.aliases if low[:3] in a.lower()})[:10]
        data["warnings"].append(f"没有名字或别名含 `{topic}` 的笔记——用 `vault.py retrieve \"{topic}\"` "
                               "做整库检索，或换一个主题词")
        return data
    data["found"] = True
    data["seeds"] = [p.stem for p in seeds]

    nbr = g.binding_neighbors()
    seed_paths = set(seeds)
    scored: dict = {}
    for seed in seeds:
        scored[seed] = _links_evidence(g, nbr, seed, None, topic)
        for q in (g.out.get(seed, set()) | {p for p, qs in g.out.items() if seed in qs}):
            scored[q] = max(scored.get(q, (-1, "")), _links_evidence(g, nbr, q, seed, topic))
        for q in g.notes:
            if q in scored:
                continue
            hit = _links_evidence(g, nbr, q, seed, topic)
            if hit[0] > 0:
                scored[q] = hit

    members, weak, structural = [], 0, 0
    for path, (score, why) in scored.items():
        if score < 2:
            weak += 1          # a bare shared neighbour, or a bare shared area
            continue
        role = _role_of(g, cfg, path)
        if role in ("raw", "index", "links", "doctrine"):
            structural += 1
            continue  # a Links card links concepts, not the trees themselves
        members.append({"note": path.stem, "path": g.rel(path), "why": why, "score": score,
                        "role": role, "areas": sorted(_area_names(g, path)),
                        "seed": path in seed_paths})
    members.sort(key=lambda m: (not m["seed"], -m["score"], m["note"]))
    data["members"] = members[:n]
    data["member_total"] = len(members)
    if weak:
        data["warnings"].append(f"另有 {weak} 篇证据太弱（只共享邻居或区域，不算成员）——"
                                "它们可能是下一层")
    if structural:
        data["warnings"].append(f"另有 {structural} 篇结构笔记（Raw Index / Index / Links / doctrine）"
                                "是关系的中介，不是成员——已排除")
    if len(members) > n:
        data["warnings"].append(f"候选 {len(members)} 篇，只列前 {n} 篇（--n 可调）")

    areas: dict = collections.defaultdict(list)
    for member in data["members"]:
        for area in member["areas"] or ["(无区域)"]:
            areas[area].append(member)
    data["groups"] = [{"area": area, "members": sorted(ms, key=lambda m: m["note"])}
                      for area, ms in sorted(areas.items())]
    data["areas"] = sorted(a for a in areas if a != "(无区域)")
    data["area_count"] = len(data["areas"])
    data["crosses_areas"] = data["area_count"] >= 2
    if not data["crosses_areas"]:
        data["warnings"].append(f"只覆盖 {data['area_count']} 个 Index 区域——"
                                "Links 卡必须横跨 ≥2 个区域（先补另一侧的成员）")
    top = [m["note"] for m in data["members"] if m["seed"]][:2] or data["seeds"][:2]
    if len(top) == 2:
        data["card_name_candidates"] = [f"Links of {top[0]} and {top[1]}",
                                        f"Links of {topic}"]
    if not data["areas"]:
        data["warnings"].append("没有任何成员落在 Index 区域里——Links 卡要先有 ≥2 个区域")
    data["warnings"].append("卡片名与共性句由你写（D16）；共性句必须基于上面的共同证据")
    return data


def _render_links_candidates(cfg: Config, data: dict) -> None:
    print(f"# vault links-candidates — \"{data['topic']}\"")
    if not data["found"]:
        for warning in data["warnings"]:
            print(f"  ⚠ {warning}")
        if data["did_you_mean"]:
            print("  相近的名字: " + " / ".join(data["did_you_mean"]))
        return
    print(f"  种子（名字/别名命中）: {', '.join(data['seeds'][:8])}")
    print(f"  覆盖区域 {data['area_count']}: "
          f"{', '.join(data['areas']) if data['areas'] else '(无)'}")
    print(f"  成员 {len(data['members'])} 篇（按区域分组；跨区域的成员会在多个区域下重复出现）:")
    for group in data["groups"]:
        print(f"    [{group['area']}] {len(group['members'])} 篇")
        for member in group["members"]:
            mark = "  ★种子" if member["seed"] else ""
            print(f"      [[{member['note']}]] — {member['why']}{mark}")
    if data["card_name_candidates"]:
        print(f"  卡片名候选（D16，最终你定）: {data['card_name_candidates'][0]}")
    for warning in data["warnings"]:
        print(f"  ⚠ {warning}")


def cmd_links_candidates(cfg: Config, g: model.Graph, args) -> int:
    """Member candidates for a Links card about one topic (read-only)."""
    data = collect_links_candidates(cfg, g, args.topic, n=args.n)
    if wants_json(args):
        emit_json(data)
        return 0 if data["found"] else 1
    _render_links_candidates(cfg, data)
    return 0 if data["found"] else 1


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
    """Trunk operations: queue + L0 proposals; --clusters / --check / --sync."""
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
    # already look half-done. Empty notes (zero bytes) skip the age gate entirely:
    # they carry no link signal at all, so the window cannot see them (L21/L22).
    first_seen = git_first_seen_index(cfg)
    window = cfg.thresholds["halfdone_window_days"]
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
        if not g.notes[p].strip():
            findings["halfdone"].append(
                f"疑似半成品: {rel} — 空笔记（零字节）, 零出链, 无 todo 挂钩 (A1/L21)")
            continue
        created = first_seen.get(rel)
        if created is None:
            continue
        age_days = (now - created) / 86400
        if age_days > window:
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
    ctx = rules.Context(cfg=cfg, graph=g)
    check_rules = [{"id": rule.id, "tier": rule.tier, "title": rule.title,
                    "count": len(rule.fn(ctx))} for rule in rules.RULES if rule.title]
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


# ---------------------------------------------------------------- docs sync


def _ids_in(text: str) -> set:
    """Rule ids declared by rules.py (`Rule("G1", ...)`)."""
    return set(re.findall(r'Rule\(\s*"([^"]+)"', text or ""))


def _subcommands_in(text: str) -> set:
    """Subcommand names declared by build_parser (`add_parser("check", ...)`)."""
    return set(re.findall(r'add_parser\(\s*"([^"]+)"', text or ""))


_ENV_CALL = re.compile(
    r"""(?:environ\s*(?:\.get\s*\(\s*|\[\s*)|getenv\s*\(\s*)['"]([A-Za-z_][A-Za-z0-9_]*)['"]""")
_ENV_CONST = re.compile(
    r"""^\s*ENV_[A-Z0-9_]+\s*=\s*['"]([A-Za-z_][A-Za-z0-9_]*)['"]""", re.M)


def _env_names(text: str) -> set:
    """Environment variables a module reads: direct literals + `ENV_*` constants."""
    return set(_ENV_CALL.findall(text or "")) | set(_ENV_CONST.findall(text or ""))


_PROBES = {
    "ids_file": _ids_in,
    "subcommands_file": _subcommands_in,
    "env_files": _env_names,
}


def _probe_paths(rule: dict, field: str) -> list:
    """A probe field is one path or a list of paths."""
    value = rule.get(field)
    if value is None:
        return []
    return [value] if isinstance(value, str) else list(value)


def _sync_scope_match(entry: str, paths: set) -> bool:
    """A sync entry matches a changed path: exact, `dir/` prefix, or glob."""
    if entry.endswith("/"):
        return any(p.startswith(entry) for p in paths)
    return any(p == entry or Path(p).match(entry) for p in paths)


def collect_docs_sync(cfg: Config, *, changed: set, added: set,
                      texts: dict) -> dict:
    """Compare the diff against the docs sync map (`tools/vault.toml [docs_sync]`).

    Pure: `changed` / `added` are repo-relative paths; `texts` maps a probe file
    to `(base_text, current_text)` (either may be None). No git access here.
    """
    touched = set(changed) | set(added)
    findings = []
    manual = []
    for rule in cfg.docs_sync:
        rid = rule["id"]
        if not any(k in rule for k in ("paths", "paths_added", *_PROBES)):
            manual.append({"id": rid, "note": rule.get("note", ""),
                           "sync": list(rule.get("sync", ()))})
            continue
        fired = False
        if any(p in changed for p in rule.get("paths", ())):
            fired = True
        if not fired and any(Path(a).match(g) for a in added
                             for g in rule.get("paths_added", ())):
            fired = True
        for probe, extract in _PROBES.items():
            if fired:
                break
            for path in _probe_paths(rule, probe):
                if path not in changed:
                    continue
                base_text, cur_text = texts.get(path, (None, None))
                if base_text is None or extract(base_text) != extract(cur_text):
                    fired = True
                    break
        if not fired:
            continue
        missing = [s for s in rule.get("sync", ()) if not _sync_scope_match(s, touched)]
        if missing:
            findings.append({"id": rid, "note": rule.get("note", ""),
                             "missing": missing})
    return {"findings": findings, "manual": manual}


def cmd_docs_check(cfg: Config, g: model.Graph, args) -> int:
    """Docs sync map vs the diff: report-level by default, a gate under --gate."""
    base = args.against or "HEAD"
    gate = bool(getattr(args, "gate", False))
    diff = _git(cfg.root, ["diff", "--name-only", base])
    added_out = _git(cfg.root, ["diff", "--name-only", "--diff-filter=A", base])
    untracked = _git(cfg.root, ["ls-files", "--others", "--exclude-standard"])
    if diff is None or added_out is None or untracked is None:
        print(f"ERROR: cannot diff against {base} (no git repo, or unknown revision)")
        return 2
    untracked = {p for p in untracked.splitlines() if p}
    changed = {p for p in diff.splitlines() if p} | untracked
    added = {p for p in added_out.splitlines() if p} | untracked

    texts = {}
    for rule in cfg.docs_sync:
        for probe in _PROBES:
            for path in _probe_paths(rule, probe):
                if path in texts or path not in changed:
                    continue
                cur = cfg.root / path
                base_text = _git(cfg.root, ["show", f"{base}:{path}"])
                texts[path] = (base_text,
                               cur.read_text(encoding="utf-8") if cur.exists() else None)

    data = collect_docs_sync(cfg, changed=changed, added=added, texts=texts)
    data.update({"base": base, "changed": sorted(changed),
                 "gate": gate, "exit": 1 if (gate and data["findings"]) else 0})

    if wants_json(args):
        emit_json(data)
        return data["exit"]

    print(f"# vault docs-check — sync map vs {base} (two-tier: report-level unless --gate)\n")
    for finding in data["findings"]:
        print(f"## {finding['id']} fired — 未同步 {len(finding['missing'])} 处")
        if finding["note"]:
            print(f"  {finding['note']}")
        for path in finding["missing"]:
            print(f"  - {path}")
        print()
    if not data["findings"]:
        print("OK — every triggered sync row carries its co-owners")
    if data["manual"]:
        print(f"\nmanual rows (no path probe — read `doctrine/Vault Extension.md` §同步面): "
              f"{', '.join(m['id'] for m in data['manual'])}")
    if data["findings"]:
        print(f"\n{len(data['findings'])} violation(s) — "
              f"{'exit 1 (--gate)' if gate else 'report-level, exit 0 (add --gate to gate)'}")
    else:
        print("\n0 violations — nothing to sync")
    return data["exit"]


# ---------------------------------------------------------------- rename


def _rename_scan(cfg: Config):
    """The G3 scan scope, split by writability.

    `zzz_output/` is the owner's area and `template/` holds scaffolds — the tool
    rewrites neither. `[[NAME]]` inside a scaffold is a placeholder, not a link,
    so "renaming" it would corrupt the scaffold instead of fixing anything.
    """
    writable, unwritable, scaffolds = [], [], []
    zzz = cfg.paths["zzz"] + "/"
    tpl = cfg.paths["template"] + "/"
    for path in sorted(parse.iter_notes(cfg.root, cfg.skip_dirs)):
        rel = _rel(cfg, path)
        if rel.startswith(zzz):
            unwritable.append(path)
        elif rel.startswith(tpl):
            scaffolds.append(path)
        else:
            writable.append(path)
    return writable, unwritable, scaffolds


def _agent_notes(cfg: Config) -> list:
    return sorted((cfg.root / ".agent").rglob("*.md"))


def collect_rename(cfg: Config, g: model.Graph, old: str, new: str) -> dict:
    """Plan a rename without writing anything (P6: writes need `--apply`).

    `error` is a refusal reason (exit 1) or None. Warnings are hints that need
    the owner's judgement, not blockers.
    """
    data = {"command": "rename", "old": old, "new": new, "error": None,
            "warnings": [], "hits": [], "unwritable": [], "agent_hits": 0,
            "scaffold_hits": [], "case_variants": [], "genre_change": None,
            "refs": 0, "files": 0, "old_path": None, "new_path": None,
            "self_alias": False, "whitelist": old in cfg.whitelist_unresolved,
            "applied": False, "remaining": None}

    name = new.strip()
    if name.endswith(".md"):
        name = name[:-3].strip()
        data["warnings"].append("已去掉 `.md` 后缀——这里给的是笔记名")
    data["new"] = name
    if not name:
        data["error"] = "新名字为空"
        return data
    if "/" in name or "\\" in name:
        data["error"] = "新名字不能含路径分隔符——改名不是搬家（移动不破坏链接，改名才要级联）"
        return data

    candidates = [p for p in parse.iter_notes(cfg.root, cfg.skip_dirs) if p.stem == old]
    if not candidates:
        data["error"] = f"没有叫 `{old}` 的笔记"
        return data
    if len(candidates) > 1:
        data["error"] = (f"`{old}` 有 {len(candidates)} 个同名文件，改哪个不明："
                         + ", ".join(_rel(cfg, p) for p in candidates))
        return data
    old_path = candidates[0]
    data["old_path"] = _rel(cfg, old_path)
    data["new_path"] = _rel(cfg, old_path.parent / f"{name}.md")
    if data["old_path"].startswith(cfg.paths["zzz"] + "/"):
        data["error"] = "拒绝改名：文件在 zzz_output/（owner 区，工具不写）"
        return data
    if old_path.parent == cfg.root and old_path.name in cfg.root_allowed:
        data["error"] = (f"拒绝改名：`{old_path.name}` 是 root 契约文件"
                         "（AGENTS 硬规则 2 只允许它俩常驻 root）")
        return data
    if old_path.stem == name:
        data["warnings"].append("新旧同名——无需改名")
        return data

    # Genre is decided by the name (name > path): a rename can move a note
    # between the trunk, the semantic tree and the fold — that is a meaning
    # change, so it is called out loudly.
    old_genre, new_genre = cfg.genre(old), cfg.genre(name)
    if old_genre != new_genre:
        data["genre_change"] = [old_genre, new_genre]
        data["warnings"].append(f"体裁会变：{old_genre} → {new_genre}"
                                "——名字决定体裁（名字 > 路径），这会把它挪出原来的树/区")

    # A name a wikilink could resolve to is taken: `[[name]]` would be ambiguous.
    stems = {p.stem: p for p in parse.iter_notes(cfg.root, cfg.skip_dirs)}
    agent = {p.stem: p for p in _agent_notes(cfg)}
    taken = (set(stems) | set(agent)) - {old}
    if name in taken:
        where = stems.get(name) or agent.get(name)
        data["error"] = (f"已有同名笔记 `{name}`：{_rel(cfg, where)}"
                         "——`[[{0}]]` 会二义，改名会让链接指向错的笔记".format(name))
        return data
    if name in g.aliases:
        data["warnings"].append(f"`{name}` 已是另一篇笔记的别名（{_rel(cfg, g.aliases[name])}）"
                                "——本工具里 stem 优先，Obsidian 可能二义")
    case_only = sorted(n for n in taken if n.lower() == name.lower())
    if case_only:
        data["warnings"].append(f"仅大小写不同的同名：{', '.join(case_only)}"
                                "——本工具大小写敏感，Obsidian 不敏感")

    writable, unwritable, scaffolds = _rename_scan(cfg)
    for path in writable:
        _, count = parse.rename_links(path.read_text(encoding="utf-8", errors="replace"),
                                      old, name)
        if count:
            data["hits"].append({"path": _rel(cfg, path), "count": count})
            data["refs"] += count
            data["files"] += 1
    for key, paths in (("unwritable", unwritable), ("scaffold_hits", scaffolds)):
        for path in paths:
            _, count = parse.rename_links(path.read_text(encoding="utf-8", errors="replace"),
                                          old, name)
            if count:
                data[key].append({"path": _rel(cfg, path), "count": count})
    for path in writable:
        variants = sum(1 for link in parse.extract_links(
            path.read_text(encoding="utf-8", errors="replace"))
            if (nm := parse.link_name(link.target)).lower() == old.lower() and nm != old)
        if variants:
            data["case_variants"].append({"path": _rel(cfg, path), "count": variants})
    if data["case_variants"]:
        total = sum(h["count"] for h in data["case_variants"])
        data["warnings"].append(f"{total} 处引用只差大小写（未改）：本工具大小写敏感、"
                                "Obsidian 不敏感——Obsidian 里它们会指向旧名")
    data["agent_hits"] = sum(
        parse.rename_links(p.read_text(encoding="utf-8", errors="replace"), old, name)[1]
        for p in _agent_notes(cfg))

    aliases = parse.parse_frontmatter(old_path.read_text(encoding="utf-8")).get("aliases") or []
    data["self_alias"] = old in aliases
    if data["self_alias"]:
        data["warnings"].append(f"本文件的 `aliases:` 里仍有 `{old}`——`[[{old}]]` 仍会解析到它；"
                                "要清掉须 owner 决定（别名改变解析，不是结构动作）")
    if data["whitelist"]:
        data["warnings"].append(f"`{old}` 在 whitelist_unresolved 里——改名后这条白名单作废")
    return data


def _render_rename(cfg: Config, data: dict, apply: bool) -> None:
    print(f"# vault rename — {data['old']} → {data['new']}"
          f"{'' if apply else '  [dry-run]'}")
    if data["error"]:
        print(f"REFUSED: {data['error']}")
        return
    print(f"  文件: {data['old_path']} → {data['new_path']}")
    if data["hits"]:
        print(f"  引用: {data['refs']} 处 / {data['files']} 个文件")
        for hit in data["hits"][:12]:
            print(f"    {hit['path']}: {hit['count']}")
        if len(data["hits"]) > 12:
            print(f"    … ({len(data['hits']) - 12} more files)")
    else:
        print("  引用: 0 处——没有任何链接指向它（改名不影响别的笔记）")
    if data["unwritable"]:
        total = sum(h["count"] for h in data["unwritable"])
        print(f"  ⚠ zzz_output/ 另有 {total} 处引用：工具不写那里（owner 手工），"
              "G3 也只扫载入的笔记，扫不到它们")
        for hit in data["unwritable"][:5]:
            print(f"    {hit['path']}: {hit['count']}")
    if data["scaffold_hits"]:
        total = sum(h["count"] for h in data["scaffold_hits"])
        print(f"  ⚠ template/ 另有 {total} 处引用（未改）：脚手架里的 `[[NAME]]` 是占位符，"
              "不是链接")
        for hit in data["scaffold_hits"][:5]:
            print(f"    {hit['path']}: {hit['count']}")
    if data["agent_hits"]:
        print(f"  ⚠ .agent/ 另有 {data['agent_hits']} 处引用，未改（AI 指令区，多为占位示例）")
    for warning in data["warnings"]:
        print(f"  ⚠ {warning}")


def cmd_rename(cfg: Config, g: model.Graph, args) -> int:
    """Rename one note and cascade every inbound wikilink (dry-run by default)."""
    data = collect_rename(cfg, g, args.old, args.new)
    apply = bool(getattr(args, "apply", False))
    if apply and not data["error"]:
        data["applied"] = _apply_rename(cfg, data)
    data["exit"] = 1 if data["error"] else 0

    if wants_json(args):
        emit_json(data)
        return data["exit"]

    _render_rename(cfg, data, apply)
    if data["error"]:
        return 1
    if not apply:
        print("  （不改文件；确认后加 --apply 落地）")
        return 0
    if not data["applied"]:
        print("  未改动（见上）")
        return 1
    print(f"  已改 {data['files']} 个文件 / {data['refs']} 处引用，复检剩余 {data['remaining']}")
    return 0 if data["remaining"] == 0 else 1


def _apply_rename(cfg: Config, data: dict) -> bool:
    """Move the file, then rewrite every inbound link. Returns True when done."""
    old_path = cfg.root / data["old_path"]
    new_path = cfg.root / data["new_path"]
    moved = _git(cfg.root, ["mv", data["old_path"], data["new_path"]]) is not None
    if not moved:
        try:
            old_path.rename(new_path)
        except OSError as exc:
            print(f"ERROR: 改名失败 {exc}")
            return False
    print(f"  {'git mv' if moved else 'rename'}: {data['old_path']} → {data['new_path']}")
    for hit in data["hits"]:
        path = new_path if hit["path"] == data["old_path"] else cfg.root / hit["path"]
        text = path.read_text(encoding="utf-8")
        new_text, _ = parse.rename_links(text, data["old"], data["new"])
        path.write_text(new_text, encoding="utf-8")
    data["remaining"] = sum(
        parse.rename_links(path.read_text(encoding="utf-8", errors="replace"),
                           data["old"], data["new"])[1]
        for path in _rename_scan(cfg)[0])
    return True


# ---------------------------------------------------------------- new

ZONES = ("root", "library", "material", "work", "todos")


def _fold_for(cfg: Config, name: str) -> str:
    """Fold directory for a Node name: A–Z, digits, CJK (v6 convention)."""
    first = name.lstrip()[:1]
    if first and first.isascii() and first.isalpha():
        return f"{first.upper()}{cfg.zones['node_suffix']}"
    if first.isdigit():
        return cfg.zones["digit_fold"]
    return cfg.zones["cjk_fold"]


def _zone_target(cfg: Config, zone: str, genre: str, name: str):
    """(directory, template key) for a zone plus the name's genre."""
    if zone == "library":
        home = {"raw": cfg.zones["raw"], "index": cfg.zones["index"],
                "links": cfg.zones["links"]}
        sub = home.get(genre) or _fold_for(cfg, name)
        return f"{cfg.paths['library']}/{sub}", (genre if genre in home else "node")
    if zone == "material":
        return cfg.paths["archives_material"], "material"
    if zone == "work":
        return cfg.paths["archives_work"], "work"
    if zone == "todos":
        return cfg.paths["todos"], "todos"
    return "", "root"


def _template_path(cfg: Config, key_or_file):
    """A template key (`node`) or a file name under `template/`, or None.

    Existence is checked in BOTH branches: a configured key whose file is absent
    (no `template/` dir at all, say) must degrade to plain markdown, not crash.
    """
    if not key_or_file:
        return None
    candidate = cfg.root / cfg.paths["template"] / cfg.templates.get(key_or_file, key_or_file)
    return candidate if candidate.exists() else None


def _render_template(text: str, name: str, source) -> str:
    """Fill the scaffold's placeholders. Everything else stays verbatim (D30)."""
    text = text.replace("[[NAME]]", f"[[{name}]]")
    if not source:
        return text
    lines, in_front, filled = text.splitlines(keepends=True), False, False
    for i, line in enumerate(lines):
        if i == 0 and line.strip() == "---":
            in_front = True
        elif in_front and line.strip() == "---":
            in_front = False
        elif in_front and re.match(r"^source:\s*$", line):
            lines[i] = f"source: {source}\n"
            filled = True
    return "".join(lines) if filled else f"---\nsource: {source}\naliases:\n---\n\n" + text


def _append_line(path: Path, line: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + line + "\n", encoding="utf-8")


def collect_new(cfg: Config, g: model.Graph, args) -> dict:
    """Plan a note: zone from state, genre from name, scaffold from the config map.

    The doctrine is enforced, not suggested: a name decides its genre (so a
    genre name may not land outside its home), `archives/material/` needs a real
    `source:` (G2), and a name that already exists is refused (it would make
    `[[name]]` ambiguous). Nothing is written without `--apply`.
    """
    data = {"command": "new", "name": args.name, "zone": args.zone, "genre": None,
            "dir": None, "path": None, "template": None, "content": None,
            "todo_file": None, "todo_line": None, "register": None, "register_line": None,
            "suggestions": [], "warnings": [], "error": None, "applied": False}

    name = args.name.strip()
    if name.endswith(".md"):
        name = name[:-3].strip()
        data["warnings"].append("已去掉 `.md` 后缀——这里给的是笔记名")
    data["name"] = name
    if not name:
        data["error"] = "名字为空"
        return data
    if "/" in name or "\\" in name:
        data["error"] = "名字不能含路径分隔符——分区由 --zone 决定"
        return data
    if args.template and args.no_template:
        data["error"] = "--template 与 --no-template 只能给一个"
        return data

    zone, genre = args.zone, cfg.genre(name)
    data["genre"] = genre
    home = {"raw": f"{cfg.paths['library']}/{cfg.zones['raw']}",
            "index": f"{cfg.paths['library']}/{cfg.zones['index']}",
            "links": f"{cfg.paths['library']}/{cfg.zones['links']}"}
    if genre in home and zone != "library":
        data["error"] = (f"`{name}` 的体裁是 {genre}（名字决定体裁），只能落在 {home[genre]}/"
                         "——去掉 --zone，或写 --zone library")
        return data
    if genre != "node" and zone in ("material", "work", "todos"):
        data["error"] = (f"`{name}` 的体裁是 {genre}（名字决定体裁），不能放进 {zone}"
                         "——改名字，或换 --zone")
        return data

    dir_rel, key = _zone_target(cfg, zone, genre, name)
    target = (cfg.root / dir_rel / f"{name}.md") if dir_rel else (cfg.root / f"{name}.md")
    data["dir"], data["path"] = dir_rel, target.relative_to(cfg.root).as_posix()
    if target.exists():
        data["error"] = f"已存在：{data['path']}"
        return data
    taken = {p.stem for p in parse.iter_notes(cfg.root, cfg.skip_dirs)}
    taken |= {p.stem for p in (cfg.root / ".agent").rglob("*.md")}
    if name in taken:
        data["error"] = f"已有同名笔记 `{name}`——同名会让 [[{name}]] 二义（先改名，或换名字）"
        return data

    if zone == "material" and not args.source:
        data["error"] = ("archives/material/ 每篇必须有真实 `source:`（G2 硬门）"
                         "——补 --source，或换 --zone")
        return data
    if args.source and zone != "material":
        data["warnings"].append("--source 只对 archives/material/ 是硬门；这里记下无害")

    template = None if args.no_template else _template_path(cfg, args.template or key)
    if args.no_template:
        data["template"] = None
    elif template is not None:
        data["template"] = _rel(cfg, template)
        data["content"] = _render_template(template.read_text(encoding="utf-8"), name, args.source)
    else:
        if args.template:
            data["error"] = (f"没有模板 `{args.template}`：`{cfg.paths['template']}/` 里找不到，"
                             f"配置里的键是 {', '.join(sorted(cfg.templates))}")
            return data
        if key in cfg.templates:
            data["warnings"].append(f"脚手架 `{cfg.paths['template']}/{cfg.templates[key]}` "
                                    "不存在——纯 markdown（工具不依赖模板，D30）")
        else:
            data["warnings"].append(f"`{zone}` 没有默认脚手架——纯 markdown（工具不依赖模板，D30）")
        data["content"] = f"---\nsource: {args.source}\naliases:\n---\n\n" if args.source else ""

    if args.todo:
        if not args.into:
            data["error"] = "挂 todo 得知道挂在哪个 todo 笔记上——补 --into \"<todo 笔记名>\""
            return data
        todo_note = next((p for p in sorted(cfg.todos_dir.glob("*.md"))
                          if p.stem == args.into), None)
        if todo_note is None:
            data["error"] = (f"`{cfg.paths['todos']}/` 顶层没有叫 `{args.into}` 的 todo 笔记"
                             "（archived/ 里的不算）")
            return data
        data["todo_file"] = _rel(cfg, todo_note)
        data["todo_line"] = f"- [ ] [[{name}]] — {args.todo.strip()}"
    elif zone != "todos":
        data["warnings"].append("没挂 todo 钩子：未完成的活必须在 todo 树里写 "
                                "`- [ ] [[NAME]] — 5–10 词续写说明`（硬规则 5）")

    if zone == "todos":
        register = cfg.todos_dir / "Index of Todos.md"
        if register.exists():
            data["register"] = _rel(cfg, register)
            data["register_line"] = f"- [ ] [[{name}]]"
        else:
            data["warnings"].append(f"没找到 {cfg.paths['todos']}/Index of Todos.md——todo 树靠它登记")
    if zone == "root":
        data["warnings"].append("落在入口队列：`triage` 会把它列出来，定好分区再搬"
                                "（搬家不破坏链接，改名才要级联）")
    if not data["content"]:
        data["warnings"].append("空笔记没有链接信号，`triage` 会一直列为疑似半成品——写完再走")
    if zone == "library" and genre == "node":
        data["warnings"].append("新 Node 还没有登记边（I1a）——`vault.py rawindex` 给归队提议")
    return data


def _render_new(cfg: Config, data: dict, apply: bool) -> None:
    print(f"# vault new — {data['name']}{'' if apply else '  [dry-run]'}")
    if data["error"]:
        print(f"REFUSED: {data['error']}")
        return
    print(f"  落点: {data['path']}  (zone={data['zone']}, genre={data['genre']})")
    print(f"  脚手架: {data['template'] or '无（纯 markdown）'}")
    if data["content"]:
        body = data["content"].splitlines()
        print("  内容:")
        for line in body[:10]:
            print(f"    {line}")
        if len(body) > 10:
            print(f"    … ({len(body) - 10} more lines)")
    if data["todo_line"]:
        print(f"  todo 钩子 → {data['todo_file']}:")
        print(f"    {data['todo_line']}")
    if data["register_line"]:
        print(f"  登记 → {data['register']}:")
        print(f"    {data['register_line']}")
    for warning in data["warnings"]:
        print(f"  ⚠ {warning}")


def cmd_new(cfg: Config, g: model.Graph, args) -> int:
    """Create one note from a scaffold, in the zone its state belongs to."""
    data = collect_new(cfg, g, args)
    apply = bool(getattr(args, "apply", False))
    if apply and not data["error"]:
        data["applied"] = _apply_new(cfg, data)
        if data["applied"]:
            model.clear_cache()
            fresh = model.build(cfg)
            target = cfg.root / data["path"]
            data["suggestions"] = [{"note": q.stem, "why": why}
                                   for q, why in suggest_candidates(cfg, fresh, target, 3)]

    if wants_json(args):
        data["exit"] = 1 if data["error"] else 0
        emit_json(data)
        return data["exit"]

    _render_new(cfg, data, apply)
    if data["error"]:
        return 1
    if not apply:
        print("  （不改文件；确认后加 --apply 落地）")
        return 0
    if not data["applied"]:
        print("  未创建（见上）")
        return 1
    print(f"  已建 {data['path']}")
    if data["suggestions"]:
        print("\n  S2 — 捕获时当场链 ≥1 篇旧笔记，写一句 why。候选（你选一个，AI 不替你选）：")
        for item in data["suggestions"]:
            print(f"    [[{item['note']}]] — {item['why']}")
        print(f"    选好后把链接写进 {data['path']} 的 `## Related`。")
    else:
        print("  S2 — 还没算出候选链接：写几句内容后再跑 "
              f"`vault.py suggest \"{data['name']}\"`。")
    print("  下一步：`python3 tools/vault.py check`")
    return 0


def _apply_new(cfg: Config, data: dict) -> bool:
    """Write the note, then the todo hook and the todo-tree registration."""
    path = cfg.root / data["path"]
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data["content"] or "", encoding="utf-8")
        if data["todo_line"]:
            _append_line(cfg.root / data["todo_file"], data["todo_line"])
        if data["register_line"]:
            _append_line(cfg.root / data["register"], data["register_line"])
    except OSError as exc:
        print(f"ERROR: 创建失败 {exc}")
        return False
    return True


# ---------------------------------------------------------------- main


HELP_TOPICS = {
    "check": """check — two-tier invariant report

    python3 tools/vault.py check [--json]

Renders every rule from the registry (`tools/vaultkit/rules.py`), so the same
rules appear in `rawindex --check` and in the `status` check summary.

  hard gates (G1/G2/G3) — any finding exits 1
    G1 root drained; G2 every `archives/material/` note has a real `source:`;
    G3 no NEW unresolved wikilink (a dangling link is a hook; only NEW blocks)
  report-level (I1a…I9, D21) — weekly increments, never block. The vault's own
    rule is 门常红 = 门失效, so exactly 3 gates exist and no more.

Change a rule → also update the docs named by sync-map row T2 (README §工具,
AGENTS §Invariants, Agent Contract §6, Vault Design §判据两级制, the memory-base
card, tests/). `python3 tools/vault.py docs-check --gate` checks that for you.""",
    "docs-check": """docs-check — docs sync map vs the diff (report-level)

    python3 tools/vault.py docs-check [--against REV] [--gate] [--json]

The sync map (`doctrine/Vault Extension.md` §同步面; machine copy in
`tools/vault.toml [docs_sync]`) says: change this, also change these. This
command diffs the working tree against REV (default HEAD) and reports every
triggered row whose co-owners were not touched.

Two-tier, like `check`: report-level by default (exit 0, prints); a gate under
--gate (exit 1). Probes are precise — a row fires only when its own probe fires:
a path changed, a NEW file appeared, the rule-id set in rules.py changed, or the
subcommand set in cli.py changed. A comment-only edit to rules.py fires nothing.
Rows with no probe are listed as `manual` (read the handbook for those).

Run it before committing a change to rules.py / cli.py / model.py / vault.toml,
or when adding a doctrine file. Content checks that always gate live in
`tests/test_docs.py` (rule ids present and non-ghost, no id ranges, no threshold
value copies, sync-map id parity, doctrine version/sync-group headers).""",
    "status": """status — session entry (read-only)

    python3 tools/vault.py status [--json]

The first command of any session. Sections: 节律 (days since 整理 / 聚簇 / 问箱 /
产出 — git + mtime derived), git state, the check summary (the same registry as
`check`), triage counts, trunk counts, zzz_output git-state, and numbered next
moves (each with a copy-pasteable command).

`--json` is the machine entry point: an AI with zero context can bootstrap from
`status --json` alone (contract path, state location, exit codes included).

On a fresh clone the rhythm line reads 今天 — it takes the max of git commit
time and mtime, and a checkout refreshes mtime. Known limitation, not a signal.""",
    "links-candidates": """links-candidates — members for a Links card about one topic

    python3 tools/vault.py links-candidates TOPIC [--n 12] [--json]

A Links card is one concept seen from several angles, and doctrine requires it
to cross ≥2 Index areas. This proposes the member list, grouped by area, with
the evidence for each member named:

  种子               notes whose name or alias contains TOPIC (the seed set)
  覆盖区域 / 成员     members grouped by Index area, each with a why-line:
                     name hit · 链到/被种子链 · 同登记 (shared Raw Index) ·
                     同区域 (shared Index area) · 共同邻居 (shared neighbours,
                     named) · ★种子
  卡片名候选          `Links of X and Y` (D16: the name and the commonality
                     sentence are yours — the sentence must rest on the evidence
                     printed above)
  ⚠                  fewer than 2 areas covered → not a Links card yet

Read-only. No seed found → exit 1, with the pointer to `retrieve` for a
whole-vault search instead of a name match.""",
    "place": """place — where a note sits in the relation graph (read-only)

    python3 tools/vault.py place NAME [--json]

One call answers "where does this belong, and what should it link first":

  in库 / 角色 / 体裁 / 分区   what the name resolves to (alias-aware; unknown
                             name → exit 1 with did-you-mean, and an honest note
                             that a note with no links has no graph position yet)
  登记于                     its registration edges (the trunk is a DAG: several
                             edges are legal)
  归队提议                   for an unregistered Node: which Raw Index the
                             neighborhood votes for, with the score (voters /
                             neighbours) and `via` — the names that voted, so the
                             proposal is always traceable to evidence
  语义区域                   the Index areas it belongs to
  出链 / 入链                Node↔Node edges
  先链这几篇                 up to 3 candidate links with a why-line (S2) — the
                             owner picks one; the tool never links for you
  ⚠ 信号                     未登记 (I1a), 零出链 (I3), 在环上 (I1c),
                             未拆 (D21), 零入链

Read-only: it reports, it never registers or links (registration edges are a
structural action you may take yourself afterwards, D22).""",
    "new": """new — create a note from a scaffold, in the zone its state belongs to

    python3 tools/vault.py new NAME [--zone Z] [--template KEY] [--no-template]
                              [--source SRC] [--todo NOTE --into TODO_NOTE]
                              [--apply] [--json]

Dry-run by default (P6): nothing is written without --apply.

Zone from STATE (AGENTS hard rule 2), genre from NAME (rule 4, name > path):
  root      (default)  the entry queue — reversible, but triage will list it
  library              Raw / Index / Links by the name's genre, else <A–Z>_fold
                       (a leading digit and CJK each get their own fold — the
                       names live in tools/vault.toml [zones])
  material             archives/material/ — needs --source (G2 hard gate)
  work                 archives/work/
  todos                a_sticker/todos/ (also registers it in Index of Todos.md)

The scaffold is OPTIONAL (D30) and comes from `tools/vault.toml [templates]` by
genre; --no-template gives plain markdown. Filled in: `[[NAME]]` and an empty
`source:` line. Everything else in the template is written verbatim.

Refuses (exit 1) rather than leaving the vault in a state its gates would flag:
  - a name that already exists (it would make `[[name]]` ambiguous);
  - a genre name outside its home zone (the name decides the genre, so it would
    be 体裁错位 the moment it exists);
  - --zone material without --source;
  - --todo without --into, or --into naming no todo note;
  - an unknown --template key.

Warns: no todo hook yet (rule 5); a new Node has no registration edge (I1a); an
empty note carries no link signal, so triage keeps listing it; landing in the
root queue. After --apply it rebuilds the graph and prints 3 candidate links
(S2) — the owner picks one and writes the why-line; the tool never links for you.""",
    "rename": """rename — rename one note and cascade every inbound wikilink

    python3 tools/vault.py rename OLD NEW [--apply] [--json]

Wikilinks resolve by note NAME, so renaming a file breaks every `[[OLD]]` that
pointed at it. This rewrites them all in one pass. Dry-run by default (L13):
nothing moves until `--apply`. The file stays in its folder — that is a move,
and moves never break links.

Forms rewritten in the same pass:
  [[OLD]] · [[OLD|alias]] · [[OLD#Heading]] · [[OLD#Heading|alias]]
  ![[OLD]] (embed) · [[folder/OLD]] · [[folder/OLD|alias]]
The `#Heading` and the `|alias` are kept verbatim: an alias is display text, not
the target. Only the LAST path segment is compared, and it must equal OLD
exactly — renaming `Old` never touches `[[OldName]]`. Fenced code blocks and
inline code spans are skipped, exactly as the resolver sees them.

Refuses (exit 1) when:
  - no note is named OLD, or several files share that stem (ambiguous);
  - a note named NEW already exists — `[[NEW]]` would resolve to the wrong one;
  - NEW contains a path separator (that is a move, not a rename);
  - OLD lives in zzz_output/ (owner's area — the tool never writes there).

Warns, never blocks: NEW is another note's `aliases:` entry, or differs from an
existing name only by case (this tool is case-sensitive, Obsidian is not); OLD
is in whitelist_unresolved; OLD is in the note's own `aliases:`; and a hit in
`zzz_output/` or `template/`, neither of which the tool rewrites — G3 does not
scan them either (it reads loaded notes only), and `[[NAME]]` in a scaffold is
a placeholder, not a link.

After --apply it re-scans and prints the remaining references in the writable
scope; that number must be 0. Renames need the owner's sign-off (AGENTS hard
rule 8): the dry-run is the proposal, --apply is the decision.""",
    "triage": """triage — placement debt (read-only)

    python3 tools/vault.py triage [--json]

Six categories, all mtime/edge heuristics — treat as prompt, not verdict:
  root        root files beyond the ones allowed in tools/vault.toml (root is the
              entry queue)
  todo_stale  todo notes untouched beyond todo_stale_days (file-level mtime, top
              scan only; a_sticker/todos/archived/ is exempt)
  halfdone    created within halfdone_window_days + zero outlink + no todo hook (A1);
              zero-byte notes are listed regardless of age — they carry no link
              signal at all, so the window could never see them (L21/L22)
  unhooked    root-queue note with no todo hook (S5 anti-loss)
  genre       name says Raw Index* / Index of* / Links of* but the file is not in
              its home zone; `-MOC` also counts as index; `a_sticker/todos/Index
              of Todos.md` is the todo-tree register (genre exception)
  dead_todo   `- [x]` reference to a name that does not resolve

All thresholds: tools/vault.toml. Nothing is written; `status` shows the same
counts inline.""",
    "rawindex": """rawindex — trunk operations

    python3 tools/vault.py rawindex [--clusters] [--check] [--sync [--apply]]
                                    [--top N] [--json]

  (no flag)    queue + L0 affiliation proposals: for every unregistered Node, the
               Raw Index its neighbors' registrations vote for. Proposals at or
               above l0_confidence (tools/vault.toml) may be appended directly (D22).
  --clusters   L1 direct-interlink components, L2 shared-neighbor clusters at
               theta = cluster_theta_percentile (binding evidence = common
               neighbors), L3 isolated points. Group clusters into coarse Raw
               Indexes — never one Raw Index per cluster (D10-P3).
  --check      the report-level rules again, from the same registry `check` uses
               (I1a/I1b/I1c, I2, I3, I5, I6, I7, I8, I9, D21).
  --sync       dry-run: prints the intended `## Core Concepts` member list of
               `Raw Index of Everything`. Add --apply to write (L13 write safety).
  --top        L0 proposals to show (default rawindex_top in tools/vault.toml).

One note's own position — registrations, the neighborhood's voting evidence,
Index areas, in/out links and the notes worth linking first — is `vault.py
place NAME` (this command works the queue as a whole).""",
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
                "1 = hard gate failed (check), unknown target (place / suggest), "
                "a refused rename or new, or a docs-sync violation under docs-check --gate; "
                "2 = missing/unreadable config (or a missing list file under --strict). "
                "Topics: `vault.py help check|status|triage|rawindex|dag|links|random|suggest"
                "|docs-check|rename|new|place|links-candidates`."),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strict", action="store_true", default=argparse.SUPPRESS,
                        help="missing config / list files are fatal (exit 2), not warnings")
    parser.add_argument("--json", action="store_true", default=argparse.SUPPRESS,
                        help="machine-readable output (one JSON document on stdout)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", parents=[common],
                   help="two-tier invariant report: hard gates exit 1; report-level rules never block")
    p_docs = sub.add_parser("docs-check", parents=[common],
                            help="docs sync map vs the diff: report-level, --gate gates")
    p_docs.add_argument("--against", metavar="REV", default=None,
                        help="base revision to diff against (default HEAD)")
    p_docs.add_argument("--gate", action="store_true", default=argparse.SUPPRESS,
                        help="exit 1 on a violation (default: report only)")
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

    p_place = sub.add_parser("place", parents=[common],
                             help="where a note sits in the relation graph (read-only)")
    p_place.add_argument("name", help="note name or alias")

    p_lc = sub.add_parser("links-candidates", parents=[common],
                          help="member candidates for a Links card about one topic")
    p_lc.add_argument("topic", help="topic word, or a note name/alias to seed from")
    p_lc.add_argument("--n", type=int, default=12, help="members to list (default 12)")

    p_new = sub.add_parser("new", parents=[common],
                           help="create a note from a scaffold, placed by zone (dry-run)")
    p_new.add_argument("name", help="note name (stem)")
    p_new.add_argument("--zone", choices=ZONES, default="root",
                       help="root (entry queue, default) / library / material / work / todos")
    p_new.add_argument("--template", metavar="KEY", default=None,
                       help="scaffold key or file under template/ (default: by genre)")
    p_new.add_argument("--no-template", action="store_true",
                       help="plain markdown — scaffolds are optional (D30)")
    p_new.add_argument("--source", metavar="SRC", default=None,
                       help="required for --zone material (G2 hard gate)")
    p_new.add_argument("--todo", metavar="NOTE", default=None,
                       help="5–10 word continuation note; also appends the todo hook")
    p_new.add_argument("--into", metavar="TODO_NOTE", default=None,
                       help="which todo note owns the hook (required with --todo)")
    p_new.add_argument("--apply", action="store_true",
                       help="actually create it (default: dry-run)")

    p_ren = sub.add_parser("rename", parents=[common],
                           help="rename a note + cascade every inbound wikilink (dry-run)")
    p_ren.add_argument("old", help="current note name (stem)")
    p_ren.add_argument("new", help="new note name (stem; the file stays in its folder)")
    p_ren.add_argument("--apply", action="store_true",
                       help="actually rename and rewrite (default: dry-run)")

    p_raw = sub.add_parser("rawindex", parents=[common],
                           help="trunk operations: queue + L0 归队提议")
    p_raw.add_argument("--clusters", action="store_true",
                       help="L1/L2 clusters + binding evidence + grouping advice")
    p_raw.add_argument("--check", action="store_true",
                       help="the report-level rules again, from the same registry as check")
    p_raw.add_argument("--sync", action="store_true",
                       help="B6: rewrite the trunk root member list (dry-run unless --apply)")
    p_raw.add_argument("--apply", action="store_true",
                       help="with --sync: actually write the trunk root (default: dry-run)")
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
    if args.command == "docs-check":
        return cmd_docs_check(cfg, g, args)
    if args.command == "triage":
        return cmd_triage(cfg, g, args)
    if args.command == "status":
        return cmd_status(cfg, g, args)
    if args.command == "random":
        return cmd_random(cfg, g, args)
    if args.command == "suggest":
        return cmd_suggest(cfg, g, args)
    if args.command == "rename":
        return cmd_rename(cfg, g, args)
    if args.command == "new":
        return cmd_new(cfg, g, args)
    if args.command == "place":
        return cmd_place(cfg, g, args)
    if args.command == "links-candidates":
        return cmd_links_candidates(cfg, g, args)
    return cmd_rawindex(cfg, g, args)


if __name__ == "__main__":
    sys.exit(main())
