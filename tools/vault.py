#!/usr/bin/env python3
"""Vault operating procedures for the v5 system: two-tier invariant check,
placement triage (todo aging + suspected half-done), trunk registration
(rawindex), session-entry status with rhythm line.

Usage:
    python3 tools/vault.py check
    python3 tools/vault.py triage
    python3 tools/vault.py status
    python3 tools/vault.py rawindex [--clusters] [--check] [--sync] [--around NAME] [--top N]

Doctrine (see doctrine/Vault Design.md, doctrine/Vault Workflow.md):
    - Two trees: Raw Index = trunk (registration), Index = semantic areas.
    - Two-tier invariants: hard gates exit 1; I1-I4 are report-level.
    - Registration edges (Raw Index -> Node) are structural: --sync appends them.
    - State lives only in the todo tree; tags are retired.

Stdlib only. Vault root = parent of tools/. Works from any cwd.
"""

import argparse
import collections
import math
import re
import subprocess
import sys
import time
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def _load_extra_lines(path: Path) -> set:
    """Read one-entry-per-line file, skipping blanks and # comments."""
    if not path.exists():
        return set()
    result = set()
    for line in path.read_text().splitlines():
        line = line.strip().split("#")[0].strip()
        if line:
            result.add(line)
    return result


# ---------------------------------------------------------------- constants

# Root files that are allowed to live outside the zones.
ROOT_ALLOWED = {"README.md", "AGENTS.md"}

# Pre-existing unresolved wikilinks (baseline snapshot; owner doctrine:
# dangling links are allowed as new-note hooks; check flags only NEW unresolved).
# Baseline updated 2026-10-06 (post-migration).
WHITELIST_UNRESOLVED = {
    "Functional",
    "Pure",
    "Statically typed",
    "Partial Sum Sequence",
    "Inequality",
    "Consolidation",
    "Subset Traversal",
    "Class",
    "Rational Function that is 1 to 1",
    "Pre-condition Check",
    "Map of Concepts of Data",
    "Trigonometric Functions",
    "Trigonometric Substitution",
    "Accelerations",
    "Instantaneous Velocity",
    "Alignment between Ordered Data Beats Mapping",
    "Bucketing Chars",
}
_BASELINE_UNRESOLVED_NAMES = [
    '...',
    '1',
    '167. Two Sum II',
    'ARP Cache',
    'ARP Reply',
    'ARP Request',
    'Absolute velocity',
    'Algebraic Structures',
    'Arc Length Parametrization',
    'Arch Linux',
    'Backend',
    'Batch-processing System',
    'Bidirectional BFS',
    'Bijective Functions',
    'Binary Tree',
    'Bitwise Mask',
    'Bounded Knapsack DP',
    'Broadcast',
    'Calculus: The Substitution Rule',
    'Cancellation Law',
    'Characterization',
    'Chebyshev Polynomials',
    'Checksum Offload',
    'Clear Lowest Bit',
    'Complexity',
    'Composition',
    'Conda',
    'Consolidation',
    'Constraint',
    'Context Shift',
    'Contiguous',
    'Convex Hull Trick for DP',
    'Correctness',
    'Curvature Formula',
    'DFS',
    'DPO - 直接偏好优化',
    'DSU_example.png',
    'Data Base',
    'Dependency Constraints BFS',
    'Device Manager',
    'Difference list',
    'Differentiability',
    'Differential Geometry',
    'Diophantine Equations',
    'Direced Graphs',
    'Domain of Value',
    'ETH Frame',
    'EUI-64',
    'Efficiency & Low Storage',
    'Element',
    'Equal Bounds',
    'Eratosthenes.png',
    'FDM',
    'First Fundamental Form',
    'Fix -id',
    'Floating-point precision issues',
    'Frontend',
    'Functional',
    'Geek-derived Term',
    'Geodesics',
    'Gradient in ML',
    'Gradient in Math',
    'Grammar\\',
    'Grammer\\',
    'Greedy todo',
    'Grid BFS and DFS',
    'Hamming Weight & Distance',
    'History How do we design Limit',
    'Homeomorphisms in Topology',
    'Hub',
    'Hyprland',
    'Hyprland Custom Config File',
    'Hyprland Custom Workspace Config File',
    'Hyprland Custom Workspace Config File for 1 Monitor',
    'Hyprland Custom Workspace Config File for 2 Monitors',
    'Hyprland Custom Workspace Config File for Headless Monitor',
    'Hyprland Workspace Config - Optimization Map',
    'Hyprland Workspace Config 优化系统 - 完整地图',
    'Hyprland Workspace System - Tree Navigation',
    'IP Datagram',
    'Index',
    'Index of Precess',
    'Inequality',
    'Instance of Move Inverse Trigonometric Functions',
    'Integer scaling',
    'KDE',
    'KTO - 卡尼曼特维斯基优化',
    'Kernel Stack',
    'LLM Fine Tune',
    'Latin Prefix Poly-',
    'Law of Associative',
    'Links',
    'LoRA - 低秩适配',
    'Log-Linear Symmetry',
    'Lowbit Operation',
    'MAC Learning',
    'MSS',
    'Manifold learning',
    'Map of Programming Language',
    'Master Theorem',
    'Memory Info',
    'Message Queue',
    'Metric Reduction',
    'Metric Tensor',
    'Minimal Connected Graph',
    'Model',
    'Most of algorithm is try to traverse without duplication',
    'Multi-Source BFS',
    'Multiprogramming',
    'NAT',
    'NIC Specific',
    'Normal acceleration',
    'OFT - 正交微调',
    'OUI',
    'Object',
    'Odd Function Property',
    'Old Name',
    'Operator',
    'Orthogonal',
    'Oscillatory Non-differentiable Point',
    'PEFT - 参数高效微调',
    'POSIX',
    'PPO - 近端策略优化',
    'Page Table',
    'Parallel',
    'Partial Sum Sequence',
    'Perpendicular',
    'Pole',
    'Prefix Sum',
    'Prefix a-',
    'Prefix syn-',
    'Private IP',
    'Process State',
    'ProcessState.jpg',
    "Processes' Asynchronicity",
    "Processes' Concurrency",
    "Processes' Dynamicity",
    "Processes' Independency",
    'Program Counter',
    'Program Segment',
    'Progress',
    'Pure',
    'RNN',
    'Rational Substitution',
    'Raw Map of Sequence Toolkits',
    'Readability',
    'Reciprocal Transformation',
    'Recursive',
    'Register',
    'Regular Curve',
    'Relative velocity',
    'Reversibility',
    'Riemannian Manifold',
    'Robustness',
    'Root chron',
    'Rotation',
    'Router',
    'SFT - 监督式微调',
    'Scalar',
    'Sigmoid Function',
    'Single Number Problem',
    'Socket',
    'Stack Pointer',
    'Stand Out',
    'State Space',
    'Statically typed',
    'Strong Convergence',
    'Subsets & State Compression',
    'TCP Retransmission',
    'TDM',
    'Tangential acceleration',
    'Term Hypernym',
    'Thread',
    "Threads' Registers",
    'Todo Interval',
    'Transition Logic',
    'Translation',
    'Tree DP',
    'Two Points',
    'Unbounded Knapsack DP',
    'Undireced Graphs',
    'Unicast',
    'User Mode',
    'Variable',
    'View of General Coding Thoughts',
    "View of Haskell's Properties",
    'WDM',
    'Weak Convergence',
    'Weak- Convergence',
    'Windows 11',
    'Windows Registry',
    "Word's Root",
    'X',
    'XOR Logic',
    'archives',
    'binning-algo',
    'chunks',
    'coprime moduli',
    'history-of-dynamic-partitioning',
    'library',
    'list-patition-algo',
    'mailbox',
    'reserved-ip',
    'soft link',
    'system of congruences',
    'tcp-ip-set.png',
    'the Magic Polynomials',
    'time-sharing System',
    'uniqueness of power series expansions',
    'ws-lib.sh',
    '丁种句',
    '三平调',
    '丙种句',
    '乙种句',
    '人生规划2',
    '参数冻结策略',
    '句式',
    '孤平',
    '对仗',
    '我的底座',
    '拗救',
    '灾难性遗忘',
    '用韵',
    '甲种句',
    '黏对',
]
WHITELIST_UNRESOLVED |= set(_BASELINE_UNRESOLVED_NAMES)
# External overrides (one entry per line, # comments)
WHITELIST_UNRESOLVED |= _load_extra_lines(ROOT / "tools" / "whitelist_unresolved.txt")

# Legacy lit notes that already lacked a real source at the 2026-09 baseline.
# check reports these informationally; NEW un-sourced material still fails hard.
# Paths below are PRE-migration; we match by stem so the split into
# archives/material/ keeps working without rewriting the list.
_BASELINE_LIT_NOSOURCE_STEMS = {
    '对制度的一点思考', '职业规划-ai版', '风险评估', 'raw index of Number-theoretic',
    'GUIDE', 'terms sheet', 'Can we Learn about Semantic Space', 'Hypernetwork',
    'CiS 03', 'Latin Root -Nomial', 'Prefix Poly-', 'Project vs. Protrude vs. Stand out',
    'Prominent', 'Recognizance of Hook Function', 'Self-generated ANN',
    'Surplus Society', 'Term Polynomial', 'Turn to the definition of differentiability',
    'Word Family of Define', '01 Knapsack DP Classes', '2D Cost Knapsack Template',
    'Algorithm Decision Tree', 'CSP 42', 'CSP Difficulty 1', 'CSP Difficulty 3',
    'CSP Math', 'CSP Simulation', 'CSP-2020-06', 'CSP202006C. Markdown 渲染器',
    'CSP202104', 'Equivalence Class Proof', 'How do you Implement Unbounded Knapsack DP',
    'Implement of Regular Expression Matching', '数量级判断', 'Clash',
    'How to tech Backend', 'Tip ml4w kitty fish config error oh-my-posh',
    'finding the projection of the line onto the plane', 'Fix -ance -ence',
    'Gynecological AI', 'Gynecological Agent Backend Todo',
    'Gynecological Experiment Design',
    'How do you handle a cartesian movement equation for a_theta',
    'How to Implement a Openclaw for yourself', 'TODO polar coordinate',
    'Term Asynchronicity', 'Two Pointers TODO', 't2 Robot and coffee', '延毕条件',
    'Lyrics 13番目の彼女', 'Raw Vocabularies Sheet', 'YM-S1-E1 Open Government',
    'YM-S1-E2 The Official Visit', 'YM-S1-E5 The Writing on the Wall',
    'YM-S1-E6 The Right to Know', '命运石之门 序章', '看过的番剧',
    'MPD Installing', 'Trick Can not Find ISO of Windows 11',
    'Trick Clash verge rev bin Kernel IO error', 'Trick Install Windows via Libvirt',
    'Trick Neo vim for vs code', 'Trick Solve confliction between swaync and KDE on D-bus',
    'Trick UMU set up', 'Trick Windows ISO Fall back',
    'Trick fix can not open virt-manager', 'Trick for VirtIO FS in windows',
    'Trick for install virtio nic driver', 'Trick for installing all virtio driver',
    'Trick install Win Fsp', 'Trick keep hyprland and wayland plasma',
    'Trick mount ntfs', 'Trick qemu', 'Trick rotate-before-login-with-sddm',
    'Trick script toggle_workspace_conf', '番剧 机动战士Z高达', '聊天',
    'BFS Templates', 'C++ algorithm start up', 'DFS Template', 'DP problems todo',
    'fix -ory -atory', 'Gynecological AI', 'Gynecological Experiment Design',
    'Improved-DP (Greedy)', 'Instance of Fraction Hook Function',
    'Instance of Function defined via Limit', 'Latin 动词现在时词干 的派生',
    'Latin 变位中的主题元音', 'Latin 名词派生', 'Legacy View of Algorithm',
    'Next Greater Elements', 'Power-Exponential-like Limit Examples',
    'Prep Notwithstanding', 'Proof of Properties of Powers of Group Elements',
    'Proof of Reversed Trigonometric Inequality', 'Proving the Given Function is Bounded',
    'Reference Sheet of Series', 'Rock and Roll Road Map', 'roots and fixes sheet',
    'States Update Form', 'Template of Fixed Window', 'Template of Sliding Window',
    'Term Hyponym', 'Traversal Index to Traversal Object',
    'Template of BFS with Cycles', 'Raw math idea',
}
# External overrides (one entry per line, # comments) — pre-migration paths,
# reduced to stems on load.
for _p in _load_extra_lines(ROOT / "tools" / "baseline_lit_nosource.txt"):
    _BASELINE_LIT_NOSOURCE_STEMS.add(Path(_p).stem)

SKIP_DIRS = {".git", ".obsidian", ".agent"}

# Notes/latex areas of the vault. zzz_output is skipped for note-loading
# (owner content) but its stems still resolve wikilinks.
NOTES_SKIP_DIRS = SKIP_DIRS | {"zzz_output"}

TODO_STALE_DAYS = 90       # B1: todo entries older than this get reported
HALFDONE_WINDOW_DAYS = 7   # A1: recent + zero-outlink + unhooked = suspected half-done


def _git_first_seen(path: Path):
    """First commit time a path was tracked, or None. Creation time that
    survives moves/migrations (unlike mtime)."""
    try:
        proc = subprocess.run(
 ["git", "-C", str(ROOT), "log", "--diff-filter=A", "--follow",
             "--format=%ct", "--", str(path.relative_to(ROOT))],
            capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    stamps = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    return float(stamps[-1]) if stamps else None

TRUNK_ROOT_STEM = "Raw Index of Everything"

_notes_cache: dict | None = None

# ---------------------------------------------------------------- helpers


def iter_notes(root: Path = ROOT, skip=NOTES_SKIP_DIRS):
    """Yield every *.md under root, skipping showcase/config dirs."""
    for path in root.rglob("*.md"):
        rel = path.relative_to(root)
        if any(part in skip for part in rel.parts):
            continue
        yield path


def _load_notes() -> dict:
    """Return {Path: text} for all vault notes, cached for one command call."""
    global _notes_cache
    if _notes_cache is None:
        _notes_cache = {p: p.read_text(encoding="utf-8", errors="replace")
                        for p in sorted(iter_notes())}
    return _notes_cache


def _clear_notes_cache():
    global _notes_cache
    _notes_cache = None


def parse_frontmatter(text: str) -> dict:
    """Parse the first --- block into a dict. Values stay strings; tags become a list."""
    fm = {}
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


_WIKILINK_RE = re.compile(r"(!?)\[\[([^\]\n]+?)(\|[^\]\n]*)?\]\]")


def extract_wikilinks(text: str):
    """Yield (target, line_no) for every [[...]] in text (embeds included).

    Skips inline code spans and fenced code blocks.
    """
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    for line_no, line in enumerate(text.splitlines(), start=1):
        line = re.sub(r"`[^`]*`", "", line)
        for match in _WIKILINK_RE.finditer(line):
            target = match.group(2)
            target = target.split("#")[0]
            target = target.split("/")[-1]
            target = target.strip()
            if target:
                yield target, line_no


def is_image_embed(target: str) -> bool:
    return target.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg"))


def _alias_map(texts: dict) -> dict:
    """{alias: note Path} — Obsidian resolves wikilinks through `aliases:`."""
    out = {}
    for p, t in texts.items():
        b = parse_frontmatter(t)
        aliases = b.get("aliases", [])
        if isinstance(aliases, str):
            aliases = [aliases]
        for a in aliases:
            if a:
                out.setdefault(a.strip(), p)
    return out


def report(title: str, findings: list) -> bool:
    print(f"## {title}")
    if findings:
        for item in findings:
            print(f"  {item}")
    else:
        print("  OK — no violations")
    print()
    return bool(findings)


def _genre(path: Path) -> str:
    """Genre by NAME (doctrine: name > path)."""
    stem = path.stem
    if stem.startswith("Raw Index"):
        return "raw"
    if stem.startswith("Index of") or stem.endswith("-MOC"):
        return "index"
    if stem.startswith("Links "):
        return "links"
    return "node"


def _zone(path: Path) -> str | None:
    """library sub-zone: Raw / Index / Links / <fold>, else None."""
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if parts[0] != "library" or len(parts) < 3:
        return None
    return parts[1]


# ---------------------------------------------------------------- check


def _collect_check():
    """Gather all check findings, two-tier (D20).

    Returns an ordered list of (tier, title, findings):
    tier "gate"    -> hard gate: any finding makes check exit 1.
    tier "report"  -> report-level: weekly increments, never blocks.
    tier "info"    -> informational baseline, never blocks.
    """
    texts = _load_notes()
    notes = sorted(texts.keys())
    basenames = {p.stem for p in notes}
    basenames |= {p.stem for p in (ROOT / "zzz_output").rglob("*.md")}
    basenames |= {p.stem for p in (ROOT / ".agent").rglob("*.md")}
    basenames |= set(_alias_map(texts))

    # ---- G1 (gate): root drained
    root_findings = [f"{p.name}: file me (root is the entry queue)"
                     for p in ROOT.glob("*.md") if p.name not in ROOT_ALLOWED]

    # ---- G2 (gate): every archives/material/ note has a real source:
    # lit detection by PATH (doctrine v5: material/ is the lit zone).
    lit_findings = []
    lit_baseline = []
    for p, text in texts.items():
        try:
            rel = p.relative_to(ROOT)
        except ValueError:
            continue
        if not str(rel).startswith("archives/material/"):
            continue
        fm = parse_frontmatter(text)
        source = fm.get("source", "")
        if not source or str(source).strip() in ("", '""', "''"):
            entry = f"{rel}: no real source:"
            if p.stem in _BASELINE_LIT_NOSOURCE_STEMS:
                lit_baseline.append(entry)
            else:
                lit_findings.append(entry)

    # ---- G3 (gate): wikilink integrity (NEW unresolved only)
    unresolved_findings = []
    for p, text in texts.items():
        for target, line_no in extract_wikilinks(text):
            if target in basenames or target in WHITELIST_UNRESOLVED:
                continue
            if is_image_embed(target):
                continue
            unresolved_findings.append(
                f"{p.relative_to(ROOT)}:{line_no}: unresolved [[{target}]]")

    # ---- R-I1..R-I4 (report): the weekly increments
    graph = _trunk_graph(texts)
    nodes = graph["nodes"]
    reg = graph["reg"]

    i1_unregistered = [n for n in nodes if not reg[n]]
    i1_multi = {n.stem: [r.stem for r in sorted(reg[n], key=lambda x: x.stem)]
                for n in nodes if len(reg[n]) > 1}
    i1_lines = [f"未登记: {len(i1_unregistered)}  (queue — see rawindex L0)"]
    for stem, raws in sorted(i1_multi.items())[:8]:
        i1_lines.append(f"  多重登记: {stem} -> {raws}")

    area = graph["area"]
    i2_lines = []
    cross = intra = noarea = 0
    for L in graph["linksn"]:
        members = [q for q in graph["out"][L] if q in area]
        areas = set().union(*[area[q] for q in members]) if members else set()
        if len(areas) >= 2:
            cross += 1
        elif areas:
            intra += 1
            i2_lines.append(f"  同区域(违规): {L.stem} ({len(members)} 成员)")
        else:
            noarea += 1
    i2_lines.insert(0, f"跨界 {cross} | 同区域 {intra}(违规) | 无区域 {noarea}(提示)")

    zero = [n for n in nodes if not graph["out"][n]]
    i3_lines = [f"零出链: {len(zero)}/{len(nodes)} ({len(zero) * 100 // max(1, len(nodes))}%)"
                " — 捕获规则增量,不阻断 (B5)"]

    i4_lines = []  # I4: doctrine & Raw excluded from binding neighbors —
    # enforced structurally by the trunk-graph builder (zones Raw/Index/Links
    # never counted as binding neighbors); violations are impossible by
    # construction. Report the exclusion counts.
    i4_lines.append(f"绑定邻居排除 doctrine({len(graph['doctrine'])}) 与 Raw({len(graph['raws'])}) — 结构性排除,无违规")

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


def cmd_check(args) -> int:
    problems = 0
    print("# vault check — two-tier (D20): hard gates exit 1; I1–I4 report-level\n")
    for tier, title, findings in _collect_check():
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
    _clear_notes_cache()
    return 1 if problems else 0


# ---------------------------------------------------------------- trunk graph


def _trunk_graph(texts: dict) -> dict:
    """Build the two-tree graph shared by check/rawindex/status.

    out[n]      -> set of notes n links to (resolved)
    reg[n]      -> {RawIndex} registrations (Raw -> Node edges)
    area[n]     -> {Index} semantic areas (Index -> Node edges)
    nodes/raws/idxs/linksn/doctrine -> zone member lists
    """
    texts = texts or _load_notes()
    stems = {}
    for p in texts:
        stems.setdefault(p.stem, p)
    aliases = _alias_map(texts)

    def resolve(name):
        s = name.split("|")[0].split("#")[0].strip().split("/")[-1].strip()
        return stems.get(s) or aliases.get(s)

    out = {}
    for p, t in texts.items():
        links = set()
        for m in re.finditer(r"\[\[([^\]\n]+)\]\]", t):
            q = resolve(m.group(1))
            if q and q != p:
                links.add(q)
        out[p] = links

    zone = _zone
    nodes = [p for p in texts if zone(p) and zone(p).endswith("_fold")]
    raws = [p for p in texts if zone(p) == "Raw"]
    idxs = [p for p in texts if zone(p) == "Index"]
    linksn = [p for p in texts if zone(p) == "Links"]
    doctrine = [p for p in texts
                if p.relative_to(ROOT).parts[0] == "doctrine"]

    reg = collections.defaultdict(set)      # node -> {raw}
    for r in raws:
        for q in out[r]:
            if zone(q) and zone(q).endswith("_fold"):
                reg[q].add(r)
    area = collections.defaultdict(set)      # note -> {index}
    for i in idxs:
        for q in out[i]:
            area[q].add(i)

    return dict(out=out, reg=reg, area=area, nodes=nodes, raws=raws,
                idxs=idxs, linksn=linksn, doctrine=doctrine, stems=stems)


# ---------------------------------------------------------------- rawindex


def cmd_rawindex(args) -> int:
    """Trunk operations: queue + L0 proposals; --clusters / --check / --sync / --around."""
    texts = _load_notes()
    g = _trunk_graph(texts)
    out, reg = g["out"], g["reg"]
    nodes, raws = g["nodes"], g["raws"]

    # neighbor map over ALL notes (undirected)
    nbr = collections.defaultdict(set)
    for p, qs in out.items():
        for q in qs:
            nbr[p].add(q)
            nbr[q].add(p)

    registered = [n for n in nodes if reg[n]]
    queue = [n for n in nodes if not reg[n]]
    print(f"nodes {len(nodes)} | Raw Index {len(raws)} | Index {len(g['idxs'])} "
          f"| Links {len(g['linksn'])}")
    print(f"registered {len(registered)} | queue {len(queue)}")

    # ---------------- --check: I1-I3 (report-level, same numbers as check)
    if args.check:
        multi = {n.stem: [r.stem for r in sorted(reg[n], key=lambda x: x.stem)]
                 for n in nodes if len(reg[n]) > 1}
        print("\n## I1 每个 Node 恰好登记在一个 Raw Index")
        print(f"  未登记: {len(queue)}   多重登记: {len(multi)}")
        for stem, rs in sorted(multi.items())[:5]:
            print(f"    {stem}: {rs}")
        print("\n## I2 Links 必须横跨 >=2 个 Index 区域")
        area = g["area"]
        intra, cross, noarea = [], [], []
        for L in g["linksn"]:
            mem = [q for q in out[L] if q in area]
            ar = set().union(*[area[q] for q in mem]) if mem else set()
            (cross if len(ar) >= 2 else (intra if ar else noarea)).append((L, len(mem), len(ar)))
        print(f"  跨界 {len(cross)} | 同区域 {len(intra)}(违规) | 无区域 {len(noarea)}(提示)")
        for L, m, x in intra[:6]:
            print(f"    同区域: {L.stem} ({m} 成员, {x} 区域)")
        print("\n## I3 Node 必须 >=1 条出链（捕获规则）")
        zero = [n for n in nodes if not out[n]]
        print(f"  零出链: {len(zero)}/{len(nodes)}  ({len(zero)*100//max(1,len(nodes))}%)")
        print("\n## 材料 出链=已拆 (D21)")
        materials = [p for p in texts
                     if str(p.relative_to(ROOT)).startswith("archives/material/")
                     and p.suffix == ".md"]
        unsplit = [p for p in materials if not out[p]]
        print(f"  未拆材料: {len(unsplit)}/{len(materials)}  (零出链 = 未拆)")
        for p in unsplit[:8]:
            print(f"    {p.relative_to(ROOT)}")

    # ---------------- --sync: keep the trunk root's member list current
    if args.sync:
        _rawindex_sync(g)

    # ---------------- --around: one node's neighborhood
    if args.around:
        return _rawindex_around(args.around, g, nbr)

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
            r, n = sc.most_common(1)[0]
            props.append((n / len(nb), n, len(nb), v, r))
    props.sort(reverse=True)
    for s, n, tot, v, r in props[:args.top]:
        print(f"  {s:.0%} ({n}/{tot})  {v.stem}  ->  {r.stem}")
    if props:
        conf = sum(1 for p in props if p[0] >= 0.9)
        print(f"\n  ≥90% 置信的提议: {conf} 条 — 登记边是结构动作, AI 可直接追加 (D22); "
              "其余照人机分工: 共性/命名你定 (D16)")

    if args.clusters:
        Q = set(queue)
        dadj = collections.defaultdict(set)
        for v in Q:
            for q in out[v]:
                if q in Q:
                    dadj[v].add(q)
                    dadj[q].add(v)
        seen, comps = set(), []
        for n in dadj:
            if n in seen:
                continue
            st, c = [n], set()
            while st:
                x = st.pop()
                if x in c:
                    continue
                c.add(x)
                st += list(dadj[x])
            seen |= c
            comps.append(c)
        comps.sort(key=len, reverse=True)
        print(f"\n## L1 直接互链粗簇: {len(comps)} 个, 覆盖 {len(seen)}/{len(Q)}")
        for c in comps[:6]:
            print(f"  ({len(c)}) " + " / ".join(sorted(x.stem for x in c)[:6]))

        z2u = collections.defaultdict(set)
        for v in Q:
            for z in nbr[v]:
                z2u[z].add(v)
        w = collections.defaultdict(float)
        ev = collections.defaultdict(collections.Counter)
        for z, us in z2u.items():
            us = sorted(us)
            if len(us) < 2:
                continue
            inc = 1.0 / math.log(max(3, len(nbr[z]) + 1))
            for x, y in combinations(us, 2):
                w[(x, y)] += inc
                ev[(x, y)][z.stem] += 1
        vals = sorted(w.values())
        th = vals[int(len(vals) * 0.97)] if vals else 0
        adj2 = collections.defaultdict(set)
        for (x, y), ww in w.items():
            if ww >= th:
                adj2[x].add(y)
                adj2[y].add(x)
        seen2, cs = set(), []
        for n in adj2:
            if n in seen2:
                continue
            st, c = [n], set()
            while st:
                x = st.pop()
                if x in c:
                    continue
                c.add(x)
                st += list(adj2[x])
            seen2 |= c
            cs.append(c)
        cs.sort(key=len, reverse=True)
        print(f"\n## L2 共享邻居细分 θ=P97={th:.2f}: {len(cs)} 簇, 最大 {len(cs[0]) if cs else 0}")
        for c in cs[:5]:
            sh = collections.Counter()
            for x, y in combinations(sorted(c), 2):
                sh.update(nbr[x] & nbr[y])
            print(f"  ({len(c)}) " + " / ".join(sorted(x.stem for x in c)[:5]))
            print(f"      绑定证据: {[s.stem for s, _ in sh.most_common(3)]}")
        print(f"\n## L3 孤点: {len(Q) - len(seen | seen2)}")
        print("\n## 粗主干归组 (D10-P3): AI 把簇归组进粗 Raw Index (一个含几个簇),")
        print("   细结构(簇+共性)进 Index — 绝不每簇一个 Raw Index。归组方案 AI 提,命名你定。")

    _clear_notes_cache()
    return 0


def _rawindex_sync(g) -> int:
    """B6: maintain the trunk root's member list (registration edges).

    Structural action per D22 — AI may append directly. The root's
    `## Core Concepts` section lists one [[Node]] line per registered member
    grouped under each child Raw Index; existing prose is left alone.
    """
    root_note = None
    for r in g["raws"]:
        if r.stem == TRUNK_ROOT_STEM:
            root_note = r
            break
    if root_note is None:
        print(f"rawindex --sync: trunk root `{TRUNK_ROOT_STEM}.md` not found in library/Raw/")
        return 1

    # Child Raw Indexes = raws other than the root; members registered there.
    children = sorted((r for r in g["raws"] if r is not root_note),
                      key=lambda p: p.stem)
    lines = []
    for r in children:
        members = sorted((n for n in g["nodes"] if r in g["reg"][n]),
                         key=lambda p: p.stem)
        lines.append(f"- [[{r.stem}]] ({len(members)})")
    body = "\n".join(lines)

    text = root_note.read_text(encoding="utf-8")
    marker = "## Core Concepts"
    if marker in text:
        head, _, tail = text.partition(marker)
        # drop everything from the marker to the next ## section (or EOF)
        rest = tail.split("\n## ", 1)
        after = "\n## " + rest[1] if len(rest) > 1 else ""
        new = head + marker + "\n\n" + body + "\n" + after
    else:
        new = text.rstrip("\n") + "\n\n" + marker + "\n\n" + body + "\n"
    root_note.write_text(new, encoding="utf-8")
    print(f"rawindex --sync: {TRUNK_ROOT_STEM} — {len(children)} child Raw Indexes registered")
    for ln in lines[:10]:
        print(f"  {ln}")
    if len(lines) > 10:
        print(f"  … ({len(lines) - 10} more)")
    return 0


def _rawindex_around(name: str, g, nbr) -> int:
    """One node's neighborhood: registrations, areas, links, neighbors."""
    stems = g["stems"]
    target = stems.get(name)
    if target is None:
        low = name.lower()
        cands = [s for s in stems if low in s.lower()][:10]
        print(f"rawindex --around: `{name}` not found.")
        if cands:
            print("  did you mean: " + " / ".join(cands))
        return 1
    print(f"## {target.stem}")
    print(f"  path: {target.relative_to(ROOT)}")
    if target in g["reg"]:
        print(f"  登记: {[r.stem for r in g['reg'][target]]}")
    else:
        print("  登记: (queue — 未登记)")
    if target in g["area"]:
        print(f"  区域: {[i.stem for i in g['area'][target]]}")
    outs = g["out"].get(target, set())
    print(f"  出链 {len(outs)}: {[q.stem for q in sorted(outs, key=lambda p: p.stem)][:12]}")
    ins = [p for p, qs in g["out"].items() if target in qs]
    print(f"  入链 {len(ins)}: {[p.stem for p in sorted(ins, key=lambda p: p.stem)][:12]}")
    nb = nbr.get(target, set())
    print(f"  邻居 {len(nb)} (绑定证据候选: "
          f"{[p.stem for p in sorted(nb, key=lambda p: p.stem)][:8]})")
    return 0


# ---------------------------------------------------------------- triage


def _collect_triage():
    """Gather placement-debt findings per category. Shared by `triage` and `status`.

    v5: todo aging (B1) + suspected half-done (A1) added; promote/stale-tag
    categories retired (no more status tags).
    """
    now = time.time()
    texts = _load_notes()
    notes = sorted(texts.keys())
    findings = {"root": [], "todo_stale": [], "halfdone": [], "unhooked": [],
                "genre": [], "dead_todo": []}

    # 1. root files beyond allowed set
    for p in sorted(ROOT.glob("*.md")):
        if p.name not in ROOT_ALLOWED:
            findings["root"].append(f"file me: {p.name} (root is the entry queue)")

    # 2. todo aging (B1): todo-note entries untouched > 90 days
    for p in sorted((ROOT / "a_sticker" / "todos").glob("*.md")):
        age_days = (now - p.stat().st_mtime) / 86400
        if age_days > TODO_STALE_DAYS:
            findings["todo_stale"].append(
                f"todo 老化: {p.name} — {int(age_days)} 天未动 → 报告并清理 (B1)")

    # 3. suspected half-done (A1): created <= 7d + zero outbound + no todo hook
    todo_targets = set()
    for p in sorted((ROOT / "a_sticker" / "todos").rglob("*.md")):
        for t, _ in extract_wikilinks(texts.get(p, "")):
            todo_targets.add(t)
    root_queue = {p for p in notes
                  if len(p.relative_to(ROOT).parts) == 1
                  and p.name not in ROOT_ALLOWED}
    # A1 scope: own-voice candidates only (library notes + root queue);
    # archives are reference material, a_sticker/or is AI-raw, doctrine is system.
    # Age = git first-commit time (creation), NOT mtime — mv/migration resets mtime.
    for p in notes:
        rel = p.relative_to(ROOT)
        in_scope = str(rel).startswith("library/") and _zone(p) and _zone(p).endswith("_fold")
        in_scope = in_scope or p in root_queue
        if not in_scope:
            continue
        created = _git_first_seen(p)
        if created is None:
            continue
        age_days = (now - created) / 86400
        if age_days > HALFDONE_WINDOW_DAYS:
            continue
        has_out = any(True for _ in extract_wikilinks(texts[p]))
        if not has_out and p.stem not in todo_targets:
            findings["halfdone"].append(
                f"疑似半成品: {rel} — git 创建 {int(age_days)} 天前, 零出链, 无 todo 挂钩 (A1)")

    # 4. unhooked notes in root queue without todo entry (S5 anti-loss)
    for p in sorted(root_queue):
        if p.stem not in todo_targets:
            findings["unhooked"].append(
                f"unhooked: {p.name} — root 队列且无 todo 挂钩 (S5)")

    # 5. genre placement: name says Raw/Index/Links but not in its home
    for p in notes:
        rel = p.relative_to(ROOT)
        if not str(rel).startswith("library/") or len(rel.parts) < 3:
            continue
        gname = _genre(p)
        home = {"raw": "Raw", "index": "Index", "links": "Links"}.get(gname)
        sub = rel.parts[1]
        if home and sub != home:
            findings["genre"].append(f"体裁错位: {rel} ({gname} 应在 library/{home}/)")
        if gname == "node" and not sub.endswith("_fold"):
            findings["genre"].append(f"体裁错位: {rel} (node 应在 <fold>)")

    # 6. dead todo links
    basenames = {p.stem for p in notes}
    basenames |= {p.stem for p in (ROOT / "zzz_output").rglob("*.md")}
    basenames |= set(_alias_map(texts))
    for p in sorted((ROOT / "a_sticker/todos").glob("*.md")):
        text = texts[p]
        lines = text.splitlines()
        for target, line_no in extract_wikilinks(text):
            if target in basenames or "Index of Todos" in str(p.name):
                continue
            if re.search(r"-\s*\[x\]", lines[line_no - 1], re.IGNORECASE):
                findings["dead_todo"].append(
                    f"dead todo reference: {p.name}:{line_no}: [[{target}]]")

    return findings


def cmd_triage(args) -> int:
    findings = _collect_triage()
    print("# mtime heuristic — treat as prompt, not verdict\n")
    for category in ("root", "todo_stale", "halfdone", "unhooked", "genre", "dead_todo"):
        items = findings[category]
        print(f"# {category}: {len(items)}")
        for line in items:
            print(line)
        print()
    _clear_notes_cache()
    return 0


# ---------------------------------------------------------------- status


def _git_porcelain():
    """git status --porcelain lines, or None when git/repo is unavailable."""
    try:
        proc = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain"],
                              capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    return [ln for ln in proc.stdout.splitlines() if ln.strip()]


def _git_last_commit(paths: list) -> float:
    """mtime of the last commit touching any of `paths`, else 0."""
    for p in paths:
        try:
            proc = subprocess.run(
                ["git", "-C", str(ROOT), "log", "-1", "--format=%ct", "--", str(p)],
                capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.SubprocessError):
            continue
        if proc.returncode == 0 and proc.stdout.strip():
            return float(proc.stdout.strip())
    return 0.0


def _rhythm_line() -> list:
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
        t = _git_last_commit(paths)
        for p in paths:
            if p.exists():
                t = max(t, p.stat().st_mtime)
        if not t:
            return "从未"
        d = int((now - t) / 86400)
        return f"{d} 天前" if d > 0 else "今天"

    todos_dir = ROOT / "a_sticker" / "todos"
    links_dir = ROOT / "library" / "Links"
    raw_dir = ROOT / "library" / "Raw"
    zzz_dir = ROOT / "zzz_output"
    return [
        f"上次整理: {days_since([todos_dir])}",
        f"上次聚簇: {days_since([raw_dir])}",
        f"上次问箱: {days_since([links_dir])}",
        f"上次产出: {days_since([zzz_dir])}",
    ]


def cmd_status(args) -> int:
    """Session-entry state report: rhythm + git + check summary + triage counts + next moves."""
    print("# vault status — session entry report (read-only)\n")

    # (0) rhythm line (B3+B7)
    print("## 节律 (B3+B7 — 停摆可见 = 停摆可治)")
    for line in _rhythm_line():
        print(f"- {line}")
    print()

    # (a) git state
    porcelain = _git_porcelain()
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
    for tier, title, findings in _collect_check():
        state = "OK" if not findings else f"{len(findings)} findings"
        print(f"- [{tier}] {title}: {state}")

    # (c) triage counts
    triage = _collect_triage()
    print("\n## triage (counts)")
    print(f"- root files: {len(triage['root'])}")
    print(f"- todo 老化 (> {TODO_STALE_DAYS} 天): {len(triage['todo_stale'])}")
    print(f"- 疑似半成品 (≤{HALFDONE_WINDOW_DAYS} 天 + 零出链 + 零挂钩): {len(triage['halfdone'])}")
    print(f"- unhooked root queue: {len(triage['unhooked'])}")
    print(f"- 体裁错位: {len(triage['genre'])}")
    print(f"- dead todo references: {len(triage['dead_todo'])}")

    # (d) trunk summary
    g = _trunk_graph(_load_notes())
    print("\n## 主干 (trunk)")
    print(f"- nodes {len(g['nodes'])} | Raw Index {len(g['raws'])} | "
          f"Index {len(g['idxs'])} | Links {len(g['linksn'])}")
    unreg = sum(1 for n in g["nodes"] if not g["reg"][n])
    print(f"- queue (未登记): {unreg} — `vault.py rawindex` gives L0 归队提议")
    zero = sum(1 for n in g["nodes"] if not g["out"][n])
    print(f"- 零出链: {zero}/{len(g['nodes'])} — I3 报告级增量 (B5)")

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
        moves.append(f"todo GC: {len(triage['todo_stale'])} 个 todo >{TODO_STALE_DAYS} 天未动 — "
                     "review / resolve / archive (B1)")
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
    _clear_notes_cache()
    return 0


# ---------------------------------------------------------------- main


def main() -> int:
    parser = argparse.ArgumentParser(description="Vault operating procedures (v5)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="two-tier invariant report: hard gates exit 1, I1–I4 report-level")
    sub.add_parser("triage", help="placement-debt report: root, todo aging, suspected half-done (read-only)")
    sub.add_parser("status", help="session entry: rhythm line + git + check + triage + trunk + next moves (read-only)")

    p_raw = sub.add_parser("rawindex", help="trunk operations: queue + L0 归队提议")
    p_raw.add_argument("--clusters", action="store_true", help="L1/L2 clusters + binding evidence + grouping advice")
    p_raw.add_argument("--check", action="store_true", help="I1–I3 + material 未拆 report")
    p_raw.add_argument("--sync", action="store_true",
                       help="B6: maintain trunk root member list (structural, D22)")
    p_raw.add_argument("--around", metavar="NAME", help="one node's neighborhood")
    p_raw.add_argument("--top", type=int, default=10, help="L0 proposals to show (default 10)")

    args = parser.parse_args()
    if args.command == "check":
        return cmd_check(args)
    if args.command == "triage":
        return cmd_triage(args)
    if args.command == "status":
        return cmd_status(args)
    return cmd_rawindex(args)


if __name__ == "__main__":
    sys.exit(main())
