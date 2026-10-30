---
name: vault-ops
description: "Krummholz vault operating procedures: note placement, trunk registration (rawindex), todo-hooking, health checks (two-tier invariants), cluster grouping, rhythm monitoring. Use when working in this Obsidian vault — filing, moving, renaming, triaging, or diagnosing vault structure."
---

# vault-ops

Operating procedures for the Krummholz Bücherstube vault. This skill holds **procedures only** — no doctrine, no constants. Doctrine lives in `doctrine/`; every threshold and path lives once, in `tools/vault.toml`.

## Load order

Read in this order before acting:

1. `AGENTS.md`
2. `README.md`
3. `doctrine/Agent Contract.md` — entry commands, what you may do directly, what needs owner approval, never-do list, self-verification, bootstrap checklist
4. `doctrine/Vault Design.md` — why the system works
5. `doctrine/Vault Workflow.md` — the 3 verbs + 1 loop, S1–S10, 心法
6. `doctrine/Vault Extension.md` — 改系统 / 改文档前读 §同步面（`doctrine/New Machine.md` 面向 owner 装配，不在 AI 载入序）

Inline help: `python3 tools/vault.py help <topic>` for `check` / `status` / `triage` / `rawindex` / `dag` / `links` / `random` / `suggest` / `docs-check`.

## Session entry

Run `python3 tools/vault.py status` first — rhythm line, git state, check summary, triage counts, trunk counts, numbered next moves (each with a copy-pasteable command). Owner decides, you execute. Repo state, not memory, decides what is possible.

- **Cold start**: a fresh clone is fully operational — procedures here, tools in `tools/`, doctrine in `doctrine/`, no state outside git. `.obsidian/` is gitignored (per-machine only).
- **Resuming**: a dirty tree means likely mid-work. Cross-check the todo tree (`grep -rn -- '- \[ \] \[\[NAME' a_sticker/todos/`). Found → resume from the continuation note. Not found → ask the owner; a note with zero signals cannot be attributed by doctrine, never guess.
- **Signals vs content**: every finding is a signal, not a verdict. Content wins; report contradictions instead of forcing actions.

## Procedures

### New note in root

1. `python3 tools/vault.py triage` — see the standing debt.
2. Decide the zone by state, move the file, let the name decide the genre (`check` reports 体裁错位).
3. Unfinished → todo-hook (S5): `- [ ] [[NAME]] — 5–10 word continuation note` in the owning todo under `a_sticker/todos/`.

### Note has zero outbound links (I3 / capture rule)

At capture time (S2): give 3 candidate links with a why-line each (`python3 tools/vault.py suggest NAME`), owner picks one, you insert it. The legacy zero-link inventory is never batch-fixed — I3 gives weekly increments only.

### Suspected half-done (A1)

`triage` lists them (created ≤ the half-done window + zero outbound links + no todo hook). Report; hook or finish — never bulk-guess.

### Todo aging (B1)

`triage` reports todo notes untouched longer than the stale window. Review, resolve, or archive into `a_sticker/todos/archived/` (exempt from the scan).

### Material extraction state (D21)

`rawindex --check` reports zero-outlink material = 未拆. A material note with outbound links to Nodes has been 拆过 — the links are the state, there is no status field.

### Note feels lost / can't find related

1. Backlinks (Obsidian).
2. `grep -rn -- '\[\[NAME' .`
3. `python3 tools/vault.py rawindex --around NAME`
4. `python3 tools/vault.py random --scope library` (问箱 material, S9)

### Renaming

1. `grep -rn -- '\[\[Old Name' .` — wikilinks resolve by note name, so every inbound form must be updated.
2. Update every form (incl. `|alias`, path-style), `git mv`, then `python3 tools/vault.py check`. Owner sign-off first.

### Trunk workflow (rawindex) — the weekly core loop

1. `python3 tools/vault.py rawindex` — registration queue + L0 归队 proposals.
2. `python3 tools/vault.py rawindex --clusters` — L1 coarse components, L2 shared-neighbor clusters with binding evidence, L3 isolated points.
3. **Group clusters into coarse Raw Indexes** (D10-P3): AI proposes the grouping, owner confirms names and writes the commonality sentence (D16). Never one Raw Index per cluster.
4. Register: append `[[Node]]` lines to the Raw Index (structural, direct). `Node↔Node` and `Index→Node` links need owner approval.
5. `python3 tools/vault.py rawindex --check` — the report-level rules again, trunk-facing.
6. `python3 tools/vault.py rawindex --sync` — dry-run; `--apply` writes the trunk root member list.

### Changing the system itself (rules, config, commands, doctrine)

1. Read `doctrine/Vault Extension.md` §同步面 — the trigger → co-owner table (ids `T1`–`T11`). Pick your row *before* editing.
2. Edit the code or doc.
3. `python3 tools/vault.py docs-check --against HEAD` — report-level; lists every triggered row whose co-owners did not move. `--gate` exits 1 (use it before committing).
4. `python3 tools/vault.py check` and `python3 -m pytest -q` — `tests/test_docs.py` holds the content checks that always gate (rule ids present and non-ghost, no id ranges, no threshold value copies, sync-map id parity, doctrine headers).
5. New doctrine file → also register it in the four places named by row T11.

### Health audit

```bash
python3 tools/vault.py check     # hard gates (exit code) + report-level increments
python3 tools/vault.py triage    # placement debt + todo aging + half-done
python3 tools/vault.py status    # all of the above + rhythm line
```

## When unsure

Ask the owner — never guess attribution for signal-less notes. The default for drafts is the root queue (reversible) over `library/` (commitment).
