#!/usr/bin/env python3
"""Vault operating procedures: invariant check, placement triage, promotion,
session-entry status.

Usage:
    python3 tools/vault.py check
    python3 tools/vault.py triage
    python3 tools/vault.py status
    python3 tools/vault.py promote NAME [--dry-run] [--force]

Stdlib only. Vault root = parent of tools/. Works from any cwd.
"""

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- constants

TYPE_TAGS = {"type/permanent", "type/lit"}
STATUS_TAGS = {"status/in-progress", "status/evergreen", "status/archive"}
ATTR_TAGS = {"attr/map", "attr/links", "attr/principle",
             "attr/concept", "attr/technique", "attr/method"}

VALID_TAGS = TYPE_TAGS | STATUS_TAGS | ATTR_TAGS

# Root files that are allowed to live outside the three zones.
ROOT_ALLOWED = {"README.md", "AGENTS.md"}

# Pre-existing unresolved wikilinks. The 17 cleanup-verified placeholders plus
# the 2026-09 baseline snapshot of intentional dangling hooks (owner doctrine:
# dangling links are allowed as new-note hooks; check flags only NEW unresolved).
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

# Legacy lit notes that already lacked a real source at the 2026-09 baseline.
# check reports these informationally; NEW un-sourced lit notes still fail hard.
_BASELINE_LIT_NOSOURCE = {
    'a_sticker/or/对制度的一点思考.md',
    'a_sticker/or/职业规划-ai版.md',
    'a_sticker/or/风险评估.md',
    'archives/reading/algorithm/raw index of Number-theoretic.md',
    'archives/reading/kaggle_biomass/GUIDE.md',
    'a_sticker/new_terms/terms sheet.md',
    'a_sticker/or/Can we Learn about Semantic Space.md',
    'a_sticker/or/Hypernetwork.md',
    'archives/CiS 03.md',
    'archives/Latin Root -Nomial.md',
    'archives/Prefix Poly-.md',
    'archives/Project vs. Protrude vs. Stand out.md',
    'archives/Prominent.md',
    'archives/Recognizance of Hook Function.md',
    'archives/Self-generated ANN.md',
    'archives/Surplus Society.md',
    'archives/Term Polynomial.md',
    'archives/Turn to the definition of differentiability.md',
    'archives/Word Family of Define.md',
    'archives/algorithms/01 Knapsack DP Classes.md',
    'archives/algorithms/2D Cost Knapsack Template.md',
    'archives/algorithms/Algorithm Decision Tree.md',
    'archives/algorithms/CSP 42.md',
    'archives/algorithms/CSP Difficulty 1.md',
    'archives/algorithms/CSP Difficulty 3.md',
    'archives/algorithms/CSP Math.md',
    'archives/algorithms/CSP Simulation.md',
    'archives/algorithms/CSP-2020-06.md',
    'archives/algorithms/CSP202006C. Markdown 渲染器.md',
    'archives/algorithms/CSP202104.md',
    'archives/algorithms/Equivalence Class Proof.md',
    'archives/algorithms/How do you Implement Unbounded Knapsack DP.md',
    'archives/algorithms/Implement of Regular Expression Matching.md',
    'archives/algorithms/数量级判断.md',
    'archives/engineering/Clash.md',
    'archives/engineering/How to tech Backend.md',
    'archives/engineering/Tip ml4w kitty fish config error oh-my-posh.md',
    'archives/finding the projection of the line onto the plane.md',
    'archives/latin/Fix -ance -ence.md',
    'archives/projects/Gynecological AI.md',
    'archives/projects/Gynecological Agent Backend Todo.md',
    'archives/projects/Gynecological Experiment Design.md',
    'archives/projects/How do you handle a cartesian movement equation for a_theta.md',
    'archives/projects/How to Implement a Openclaw for yourself.md',
    'archives/projects/TODO polar coordinate.md',
    'archives/projects/Term Asynchronicity.md',
    'archives/projects/Two Pointers TODO.md',
    'archives/projects/t2 Robot and coffee.md',
    'archives/projects/延毕条件.md',
    'archives/reading-notes/Lyrics 13番目の彼女.md',
    'archives/reading-notes/Raw Vocabularies Sheet.md',
    'archives/reading-notes/YM-S1-E1 Open Government.md',
    'archives/reading-notes/YM-S1-E2 The Official Visit.md',
    'archives/reading-notes/YM-S1-E5 The Writing on the Wall.md',
    'archives/reading-notes/YM-S1-E6 The Right to Know.md',
    'archives/reading-notes/命运石之门 序章.md',
    'archives/reading-notes/看过的番剧.md',
    'archives/tricks/MPD Installing.md',
    'archives/tricks/Trick Can not Find ISO of Windows 11.md',
    'archives/tricks/Trick Clash verge rev bin Kernel IO error.md',
    'archives/tricks/Trick Install Windows via Libvirt.md',
    'archives/tricks/Trick Neo vim for vs code.md',
    'archives/tricks/Trick Solve confliction between swaync and KDE on D-bus.md',
    'archives/tricks/Trick UMU set up.md',
    'archives/tricks/Trick Windows ISO Fall back.md',
    'archives/tricks/Trick fix can not open virt-manager.md',
    'archives/tricks/Trick for VirtIO FS in windows.md',
    'archives/tricks/Trick for install virtio nic driver.md',
    'archives/tricks/Trick for installing all virtio driver.md',
    'archives/tricks/Trick install Win Fsp.md',
    'archives/tricks/Trick keep hyprland and wayland plasma.md',
    'archives/tricks/Trick mount ntfs.md',
    'archives/tricks/Trick qemu.md',
    'archives/tricks/Trick rotate-before-login-with-sddm.md',
    'archives/tricks/script toggle_workspace_conf.md',
    'archives/番剧 机动战士Z高达.md',
    'archives/聊天.md',
    'library/B_fold/BFS Templates.md',
    'library/C_fold/C++ algorithm start up.md',
    'library/D_fold/DFS Template.md',
    'library/D_fold/DP problems todo.md',
    'library/F_fold/fix -ory -atory.md',
    'library/G_fold/Gynecological AI.md',
    'library/G_fold/Gynecological Experiment Design.md',
    'library/I_fold/Improved-DP (Greedy).md',
    'library/I_fold/Instance of Fraction Hook Function.md',
    'library/I_fold/Instance of Function defined via Limitation.md',
    'library/L_fold/Latin 动词现在时词干 的派生.md',
    'library/L_fold/Latin 变位中的主题元音.md',
    'library/L_fold/Latin 名词派生.md',
    'library/L_fold/Legacy View of Algorithm.md',
    'library/N_fold/Next Greater Elements.md',
    'library/P_fold/Power-Exponential-like Limitation Examples.md',
    'library/P_fold/Prep Notwithstanding.md',
    'library/P_fold/Proof of Properties of Powers of Group Elements.md',
    'library/P_fold/Proof of Reversed Trigonometric Inequality.md',
    'library/P_fold/Proving the Given Function is Bounded.md',
    'library/R_fold/Reference Sheet of Series.md',
    'library/R_fold/Rock and Roll Road Map.md',
    'library/R_fold/roots and fixes sheet.md',
    'library/S_fold/States Update Form.md',
    'library/T_fold/Template of Fixed Window.md',
    'library/T_fold/Template of Sliding Window.md',
    'library/T_fold/Term Hyponym.md',
    'library/T_fold/Traversal Index to Traversal Object.md',
    'library/Template of BFS with Cycles.md',
    'archives/Raw math idea.md',
}

SKIP_DIRS = {".git", ".obsidian", "zzz_output", ".agent"}

# ---------------------------------------------------------------- helpers


def iter_notes(root: Path = ROOT):
    """Yield every *.md under root, skipping showcase/config dirs."""
    for path in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def parse_frontmatter(text: str) -> dict:
    """Parse the first --- block into a dict. Values stay strings; tags become a list."""
    fm = {}
    if not text.startswith("---"):
        return fm
    lines = text.splitlines()
    # find closing ---
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
                fm[key] = []          # bare "key:" -> list items follow
        elif line.startswith("  - ") and key is not None:
            fm.setdefault(key, [])
            if isinstance(fm[key], list):
                fm[key].append(line[4:].strip().strip("'\""))
    return fm


def get_tags(fm: dict) -> list:
    tags = fm.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]
    return [t for t in tags if t]


_WIKILINK_RE = re.compile(r"(!?)\[\[([^\]\n]+?)(\|[^\]\n]*)?\]\]")


def extract_wikilinks(text: str):
    """Yield (target, line_no) for every [[...]] in text (embeds included).

    Skips inline code spans (`...`) — command literals like `- [ ] [[NAME]]`
    are syntax examples, not links. Fenced code blocks are skipped by the
    caller stripping them first when needed for invariant checks.
    """
    for line_no, line in enumerate(text.splitlines(), start=1):
        line = re.sub(r"`[^`]*`", "", line)
        for match in _WIKILINK_RE.finditer(line):
            target = match.group(2)
            # strip heading/anchor, then path prefix up to last /
            target = target.split("#")[0]
            target = target.split("/")[-1]
            target = target.strip()
            if target:
                yield target, line_no


def is_image_embed(target: str) -> bool:
    return target.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg"))


def report(title: str, findings: list) -> bool:
    print(f"## {title}")
    if findings:
        for item in findings:
            print(f"  {item}")
    else:
        print("  OK — no violations")
    print()
    return bool(findings)


# ---------------------------------------------------------------- check


def _collect_check():
    """Gather all check findings. Shared by `check` and `status`.

    Returns an ordered list of (title, findings, hard): hard sections count
    toward check's PROBLEMS total; informational ones never do.
    """
    notes = sorted(iter_notes())
    texts = {p: p.read_text(encoding="utf-8", errors="replace") for p in notes}
    basenames = {p.stem for p in notes}
    basenames |= {p.stem for p in (ROOT / "zzz_output").rglob("*.md")}

    # 1. root drained
    root_findings = [f"{p.name}: file me (root is the entry queue)"
                     for p in ROOT.glob("*.md") if p.name not in ROOT_ALLOWED]

    # 2. lit notes carry a real source
    # template/lit-temp.md keeps `source:` empty by design (AGENTS.md rule 4).
    # Legacy lit notes with genuinely un-derivable sources are a known baseline
    # (owner sign-off pending on sourcing/retagging) — reported, not failing.
    lit_findings = []
    lit_baseline = []
    for p, text in texts.items():
        if p.is_relative_to(ROOT / "template"):
            continue
        fm = parse_frontmatter(text)
        if "type/lit" in get_tags(fm):
            source = fm.get("source", "")
            if not source or str(source).strip() in ("", '""', "''"):
                entry = f"{p.relative_to(ROOT)}: type/lit without real source:"
                if str(p.relative_to(ROOT)) in _BASELINE_LIT_NOSOURCE:
                    lit_baseline.append(entry)
                else:
                    lit_findings.append(entry)

    # 3. tag vocabulary
    tag_findings = []
    for p, text in texts.items():
        if p.is_relative_to(ROOT / "template"):
            continue
        fm = parse_frontmatter(text)
        for tag in get_tags(fm):
            if tag.startswith("topic/"):
                # open vocabulary — prefix check only (AGENTS.md Tags section)
                if not tag[len("topic/"):]:
                    tag_findings.append(f"{p.relative_to(ROOT)}: empty topic tag 'topic/'")
            elif tag.startswith(("type/", "status/", "attr/")) and tag not in VALID_TAGS:
                tag_findings.append(f"{p.relative_to(ROOT)}: invalid tag '{tag}'")
            elif tag == "todo" and not str(p).startswith(str(ROOT / "a_sticker/todos")):
                tag_findings.append(f"{p.relative_to(ROOT)}: bare 'todo' tag outside a_sticker/todos/")

    # 4. wikilink integrity
    unresolved_findings = []
    for p, text in texts.items():
        for target, line_no in extract_wikilinks(text):
            if target in basenames or target in WHITELIST_UNRESOLVED:
                continue
            if is_image_embed(target):
                continue
            unresolved_findings.append(
                f"{p.relative_to(ROOT)}:{line_no}: unresolved [[{target}]]")

    # 5. orphans (zero inbound AND zero outbound)
    outbound = {}
    inbound = {}
    for p, text in texts.items():
        links = {t for t, _ in extract_wikilinks(text)}
        outbound[p] = links
        for t in links:
            inbound.setdefault(t, set()).add(p)
    orphan_findings = []
    for p in notes:
        rel = p.relative_to(ROOT)
        if not str(rel).startswith(("mailbox/", "library/")):
            continue
        if str(rel).startswith(("library/Index/", "library/Links/")):
            continue
        fm = parse_frontmatter(texts[p])
        if "attr/map" in get_tags(fm):
            continue
        if not outbound[p] and not inbound.get(p.stem):
            orphan_findings.append(f"{rel}: no inbound and no outbound wikilinks")

    return [
        ("Root drained", root_findings, True),
        ("Lit notes have real source", lit_findings, True),
        ("Lit without source — informational (2026-09 baseline; owner sign-off pending)",
         lit_baseline, False),
        ("Tag vocabulary", tag_findings, True),
        ("Wikilink integrity (NEW unresolved only; whitelist = known placeholders)",
         unresolved_findings, True),
        ("Orphans — informational (invisible-to-association risk; link them when touched)",
         orphan_findings, False),
    ]


def cmd_check(args) -> int:
    problems = 0
    for title, findings, hard in _collect_check():
        if hard:
            problems += report(title, findings)
        else:
            report(title, findings)
    print("CLEAN — all invariants hold" if problems == 0 else f"PROBLEMS: {problems}")
    return 1 if problems else 0


# ---------------------------------------------------------------- triage


def _collect_triage():
    """Gather placement-debt findings per category. Shared by `triage` and `status`."""
    now = time.time()
    notes = sorted(iter_notes())
    findings = {"root": [], "promote": [], "stale": [], "untagged": [], "unhooked": [], "dead_todo": []}

    # 1. root files beyond allowed set
    for p in sorted(ROOT.glob("*.md")):
        if p.name not in ROOT_ALLOWED:
            findings["root"].append(f"file me: {p.name} (root is the entry queue)")

    # 2. mailbox evergreen = stalled promotions
    for p in sorted((ROOT / "mailbox").glob("*.md")):
        fm = parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        if "status/evergreen" in get_tags(fm):
            findings["promote"].append(
                f"promote candidate: {p.stem} (evergreen tag only — content may not be stable)")
    for p in notes:
        rel = str(p.relative_to(ROOT))
        if not rel.startswith("library/"):
            continue
        fm = parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        if "status/in-progress" in get_tags(fm):
            age_days = (now - p.stat().st_mtime) / 86400
            if age_days > 90:
                findings["stale"].append(f"stale in-progress: {rel} ({int(age_days)} days old)")
    # 3.5 mailbox in-progress notes without any todo entry (S5 anti-loss rule).
    # Any wikilink to the note from any file in a_sticker/todos/ counts as
    # hooked (todo item or Index of Todos registration).
    todo_targets = set()
    for p in sorted((ROOT / "a_sticker" / "todos").glob("*.md")):
        for t, _ in extract_wikilinks(p.read_text(encoding="utf-8", errors="replace")):
            todo_targets.add(t)
    for p in sorted((ROOT / "mailbox").glob("*.md")):
        fm = parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        if "status/in-progress" in get_tags(fm) and p.stem not in todo_targets:
            findings["unhooked"].append(
                f"unhooked in-progress: mailbox/{p.name} — no todo entry (Spec §S5)")

    # 4. untagged notes (no type/* tag). By design untagged: root infra files,
    # todo notes (bare `todo` tag), templates.
    for p in notes:
        rel_path = str(p.relative_to(ROOT))
        if rel_path in ("AGENTS.md", "README.md"):
            continue
        if rel_path.startswith(("a_sticker/todos/", "template/")):
            continue
        fm = parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        if not any(t.startswith("type/") for t in get_tags(fm)):
            findings["untagged"].append(f"untagged: {rel_path}")

    # 5. dead todo links
    basenames = {p.stem for p in notes}
    basenames |= {p.stem for p in (ROOT / "zzz_output").rglob("*.md")}
    for p in sorted((ROOT / "a_sticker/todos").glob("*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        for target, line_no in extract_wikilinks(text):
            if target in basenames or "Index of Todos" in str(p.name):
                continue
            # unchecked items are future-note hooks (vault doctrine) — fine;
            # a checked item pointing at a missing note is dead.
            if "- [x]" in lines[line_no - 1]:
                findings["dead_todo"].append(
                    f"dead todo reference: {p.name}:{line_no}: [[{target}]]")

    return findings


def cmd_triage(args) -> int:
    findings = _collect_triage()
    print("# mtime heuristic — treat as prompt, not verdict\n")
    for category in ("root", "promote", "stale", "untagged", "unhooked", "dead_todo"):
        for line in findings[category]:
            print(line)
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


def cmd_status(args) -> int:
    """Session-entry state report: git + check + triage + next moves.

    Read-only, always exits 0. This IS the entry state machine: repo state,
    not memory, decides what is possible.
    """
    print("# vault status — session entry report (read-only)\n")

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
        for ln in porcelain:
            print(f"  {ln.strip()}")

    # (b) check sections, summary only
    print("\n## check (summary)")
    for title, findings, hard in _collect_check():
        state = "OK" if not findings else f"{len(findings)} findings"
        if not hard and findings:
            state += " (informational)"
        print(f"- {title}: {state}")

    # (c) triage key findings, counts only
    triage = _collect_triage()
    print("\n## triage (counts)")
    print(f"- root files: {len(triage['root'])}")
    print(f"- promote candidates (evergreen tag only — verify content first): {len(triage['promote'])}")
    print(f"- stale in-progress (> 90 days): {len(triage['stale'])}")
    print(f"- untagged: {len(triage['untagged'])}")
    print(f"- unhooked in-progress (no todo entry): {len(triage['unhooked'])}")
    print(f"- dead todo references: {len(triage['dead_todo'])}")

    # (d) uncommitted zzz_output changes — git-state only, content never read
    zzz_changes = [ln.strip() for ln in (porcelain or []) if "zzz_output/" in ln]
    print("\n## zzz_output (owner's terminal output — git-state only)")
    if zzz_changes:
        print(f"unpublished-output changes: {len(zzz_changes)} files")
        for ln in zzz_changes:
            print(f"  {ln}")
    else:
        print("no uncommitted changes")

    # next moves — fixed decision table, plain ifs
    print("\n## next moves")
    moves = []
    if porcelain:
        moves.append("commit or tidy first (run `python3 tools/vault.py status` after)")
    if triage["root"]:
        moves.append("file me: run triage, decide zone, move")
    if triage["promote"]:
        moves.append(f"promote candidates: {len(triage['promote'])} (signal, not verdict — "
                     "check content) — run `python3 tools/vault.py promote NAME --dry-run`")
    if triage["stale"]:
        moves.append(f"{len(triage['stale'])} notes idle > 90 days — review or archive")
    if triage["untagged"]:
        moves.append(f"untagged: {len(triage['untagged'])} — tidy: "
                     "run `python3 tools/vault.py triage`, add `type/*` tags")
    if triage["unhooked"]:
        moves.append(f"{len(triage['unhooked'])} unhooked in-progress notes — "
                     "todo-hook per Spec §S5 (dynamic todo creation)")
    if zzz_changes:
        moves.append(f"unpublished-output changes: {len(zzz_changes)} files — "
                     "finish/publish via Spec §S4")
    if not moves:
        moves.append("vault clean — new capture, idea polish (Spec §S1), "
                     "or ingestion (Spec §S3) are available")
    for i, move in enumerate(moves, 1):
        print(f"{i}. {move}")
    return 0


# ---------------------------------------------------------------- promote


def _destination_for(name: str, fm: dict) -> Path:
    if "attr/map" in get_tags(fm) and (name.startswith("Index of") or name.startswith("Raw Index")):
        return ROOT / "library/Index" / f"{name}.md"
    if "attr/links" in get_tags(fm):
        return ROOT / "library/Links" / f"{name}.md"
    # letter fold: first ASCII letter in the name
    for ch in name:
        if "a" <= ch <= "z" or "A" <= ch <= "Z":
            return ROOT / f"library/{ch.upper()}_fold" / f"{name}.md"
    # existing vault conventions: digit-leading -> 0_fold, CJK -> 中_fold
    for ch in name:
        if ch.isdigit():
            return ROOT / "library/0_fold" / f"{name}.md"
    for ch in name:
        if ord(ch) > 0x2E80:  # CJK range
            return ROOT / "library/中_fold" / f"{name}.md"
    return ROOT / "library/_misc" / f"{name}.md"


def cmd_promote(args) -> int:
    name = args.name
    name = name.removeprefix("mailbox/")
    if name.endswith(".md"):
        name = name[:-3]
    matches = list((ROOT / "mailbox").glob(f"{name}.md"))
    if not matches:
        print(f"error: mailbox/{name}.md not found")
        return 1
    if len(matches) > 1:
        print(f"error: ambiguous name, matches: {[str(m) for m in matches]}")
        return 1

    src = matches[0]
    text = src.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(text)
    tags = get_tags(fm)
    errors = []

    if "status/evergreen" not in tags and not args.force:
        errors.append("not stable; finish first or pass --force")

    for tag in tags:
        if tag.startswith(("type/", "status/", "attr/")) and tag not in VALID_TAGS:
            errors.append(f"tag typo: '{tag}' not in closed vocabulary")

    if "type/lit" in tags:
        print("refused: type/lit notes belong in archives/, not library/")
        print(f"suggest: git mv '{src.relative_to(ROOT)}' archives/")
        return 1

    if errors:
        for e in errors:
            print(f"error: {e}")
        print("nothing moved")
        return 1

    dst = _destination_for(name, fm)
    if dst.exists():
        print(f"error: destination already exists: {dst.relative_to(ROOT)}")
        return 1

    print(f"plan: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
    if args.dry_run:
        print("dry-run: nothing moved")
        return 0

    dst.parent.mkdir(parents=True, exist_ok=True)
    src.rename(dst)
    print(f"moved: {dst.relative_to(ROOT)}")
    print("reminder: run `python3 tools/vault.py check` before committing")
    return 0


# ---------------------------------------------------------------- main


def main() -> int:
    parser = argparse.ArgumentParser(description="Vault operating procedures")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="invariant report (read-only)")
    sub.add_parser("triage", help="placement-debt report (read-only)")
    sub.add_parser("status", help="session-entry state report: git + check + triage + next moves (read-only)")

    p_promote = sub.add_parser("promote", help="move mailbox -> library with graduation rules")
    p_promote.add_argument("name", help="note name (mailbox/ prefix and .md optional)")
    p_promote.add_argument("--dry-run", action="store_true", help="print plan, move nothing")
    p_promote.add_argument("--force", action="store_true",
                           help="bypass the status check (never the lit rule)")

    args = parser.parse_args()
    if args.command == "check":
        return cmd_check(args)
    if args.command == "triage":
        return cmd_triage(args)
    if args.command == "status":
        return cmd_status(args)
    return cmd_promote(args)


if __name__ == "__main__":
    sys.exit(main())
