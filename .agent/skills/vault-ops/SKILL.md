---
name: vault-ops
description: "Krummholz vault operating procedures: note placement, trunk registration (rawindex), todo-hooking, health checks (two-tier invariants), cluster grouping, rhythm monitoring. Use when working in this Obsidian vault — filing, moving, renaming, triaging, or diagnosing vault structure."
---

# vault-ops

Operating procedures for the Krummholz Bücherstube vault. Never improvise doctrine; follow the load order below.

## Load order

Read in this order before acting:

1. `AGENTS.md`
2. `README.md`
3. `doctrine/Vault Design.md`
4. `doctrine/Vault Workflow.md`

These four files are the truth. This skill restates them operationally.

## Session entry (state machine)

At the start of every session — cold or warm — run `python3 tools/vault.py status`. It prints the **rhythm line** (上次整理 / 上次聚簇 / 上次问箱 / 上次产出 — days since, derived from git log + mtime, zero manual records). A stalled number (e.g. 聚簇 > 14 days) is a standing warning, same failure class as the trend-radar 9-day stall. Report state in plain language, present next-moves as numbered options; owner decides, you execute. Repo state, not memory, decides what is possible.

### Cold start

Fresh clone is fully operational: procedures in this skill, tools in `tools/`, doctrine in `doctrine/`. No state outside git. `.obsidian/` is gitignored (per-machine conveniences only).

### Resuming half-done work

Dirty tree / untracked files = likely mid-work. Cross-check against the todo tree: grep for `- [ ] [[NAME]]` hooks. Found → resume from the continuation note. Not found → ask the owner; a note with zero signals (no links, no todo hook, no registration) cannot be attributed by doctrine — never guess.

### Tool signals vs content

`check`/`triage`/`status` findings are signals, not verdicts. A "疑似半成品" flag is a time-windowed heuristic (created ≤7d + zero outbound links + no todo hook); content wins over the signal — report contradictions, don't force actions.

## Hard mechanics

- Wikilinks resolve by **note name, not path**. Renaming: `grep -rn '\[\[Old Name'` first, update every form (incl. `|alias`, path-style), `git mv`, then `check`.
- Root is the entry queue. Allowed root files: `README.md`, `AGENTS.md`. Everything else gets drained by `triage`.
- Zones: `archives/material/` (external, `source:` mandatory — hard gate), `archives/work/` (owner archives / AI reports), `library/` (own-voice), root (queue).
- Genre by name: `Raw Index*` → `library/Raw/`; `Index of*` → `library/Index/`; `Links of*` → `library/Links/`; else `<letter>_fold`.
- **No tags, no frontmatter** beyond `aliases:` / `source:`. Notes are plain markdown.
- State lives only in the todo tree: unfinished work carries `- [ ] [[NAME]] — continuation note (5–10 words)` in the owning todo. Resolve the owning todo dynamically from topic/name; create `a_sticker/todos/<Topic> Todo.md` and register in `Index of Todos.md` if none fits. A todo entry without a continuation note is forbidden.
- **Registration edges (Raw Index → Node) are structural actions — you may append them directly** (e.g. `rawindex --sync`, L0 归队 with ≥90% confidence, coarse-index grouping). `Node↔Node` and `Index→Node` new links need owner approval — links change meaning. Structure fixes (renames, re-homing, dangling repair) you do directly.
- Never touch `zzz_output/` contents; never write own-voice prose (skeleton/questions/checks only; AI prose goes to `a_sticker/or/`).
- Deletions/renames: owner sign-off first.

## The trunk workflow (rawindex)

The weekly core loop — 聚簇 (cluster) → 归组 (group) → 登记 (register):

1. `python3 tools/vault.py rawindex` — the registration queue (未登记 Nodes) + L0 affiliation proposals (queue notes whose neighbors' registrations vote ≥90% for one Raw Index).
2. `python3 tools/vault.py rawindex --clusters` — L1 coarse components (direct interlinks), L2 fine clusters (shared-neighbor θ=P97, with binding evidence = common neighbors), L3 isolated points.
3. **Group clusters into coarse Raw Indexes** (D10-P3): one coarse Raw Index holds several clusters — AI proposes the grouping, owner confirms names. Never create one Raw Index per cluster (68 clusters ≠ 68 files).
4. Registration is append-only bookkeeping: you add `[[Node]]` lines to the Raw Index (structural, direct). Cluster共性 (commonality) goes into the Index note as a draft for owner sign-off — one sentence per cluster, owner's words, or the cluster does not enter the Index (D16).
5. `python3 tools/vault.py rawindex --check` — I1–I3 report-level increments (未登记 / 多重登记 / Links 区域 / 零出链).
6. `python3 tools/vault.py rawindex --sync` — dry-run: prints the intended `library/Raw/Raw Index of Everything.md` member list without touching the file (L13 write safety). Add `--apply` to land it (structural, direct).

Convergence is bounded (measured: 674 queue → 6 rounds → 108; first round eats 25%).

## Common problems → exact procedures

### Session start / unsure what to do

1. `python3 tools/vault.py status` → rhythm line + numbered options.
2. Execute owner's choice per [[Vault Workflow]] scenarios.

### New note in root

1. `python3 tools/vault.py triage` — standing debt.
2. Decide zone by state; move; genre by name (see Hard mechanics).
3. If unfinished → todo-hook (S5).

### Note has zero outbound links (I3 / 捕获规则)

At capture time S2 applies: **give 3 candidate links with a why-line each; owner picks one; you insert it.** Old zero-link inventory is not batch-fixed — I3 gives weekly increments, no hard gate (B5 honesty item).

### Suspected half-done work (A1)

`triage` lists 疑似半成品: created ≤7 days + zero outbound links + no todo hook. Report to owner; hook or finish — never bulk-guess.

### Todo aging (B1)

`triage` reports todo entries untouched >90 days. Weekly cleanup: review, resolve, or archive into `a_sticker/todos/archived/` (manual GC already happens there — the report makes it systematic).

### Where is this material's extraction state? (D21)

`rawindex --check` reports zero-outlink material = 未拆. A material note with outbound links to Nodes has been拆过. No status fields — the links are the state.

### Note feels lost / can't find related

1. Backlinks (Obsidian).
2. `grep -rn '[[NAME'` across the vault.
3. `python3 tools/vault.py rawindex --around NAME`.

### Renaming

1. `grep -rn '\[\[Old Name'`.
2. Update every form; `git mv`; `python3 tools/vault.py check`.

### Health audit

- `python3 tools/vault.py check` — hard gates (exit code) + report-level increments.
- `python3 tools/vault.py triage` — placement debt + todo aging + suspected half-done.
- `python3 tools/vault.py status` — all of the above + rhythm line.

## When unsure

Ask the owner — never guess attribution for signal-less notes. The default for drafts is the root queue (reversible) over library (commitment).
