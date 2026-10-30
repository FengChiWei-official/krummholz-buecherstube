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

### New note (capture, S2/S5)

1. `python3 tools/vault.py new "<Name>"` — dry-run. Zone comes from **state** (root = the entry queue and the reversible default), genre from the **name**, scaffold from `tools/vault.toml [templates]` by genre (optional — D30, `--no-template` for plain markdown).
2. Unfinished work → hook it in the same call: `--todo "5–10 word continuation" --into "<owning todo note>"` (rule 5). A `--zone todos` note is registered in `Index of Todos.md` instead.
3. Owner confirms → add `--apply`. It then prints 3 candidate links (S2): pick one and write it into `## Related` with a why-line. The tool never links for you — links change meaning (Agent Contract §4).
4. `python3 tools/vault.py check`; `triage` lists whatever placement debt the new note created (root, unhooked, genre, zero-link).

It refuses rather than leaving the vault in a state its gates would flag: an existing name (ambiguity), a genre name outside its home zone (体裁错位), `--zone material` without `--source` (G2), `--todo` without `--into`.

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

Wikilinks resolve by note name, so a rename must cascade. The tool does it; the owner still signs off.

1. `python3 tools/vault.py rename "Old Name" "New Name"` — dry-run: prints the file pair, every inbound reference per file, and every refusal/warning. Nothing is written.
2. Read the warnings: a genre change (`node → raw` — the name decides the genre), a case-only twin, another note's `aliases:` already holding the new name, the old name in `whitelist_unresolved`, the old name inside the note's own `aliases:`.
3. Owner confirms → `python3 tools/vault.py rename "Old Name" "New Name" --apply`. It moves the file (`git mv` when available) and rewrites `[[Old]]`, `[[Old|alias]]`, `[[Old#Heading]]`, `![[Old]]`, `[[folder/Old]]`, `[[Old.md]]` — alias and heading untouched, fenced code and inline code spans skipped.
4. It re-scans and prints the remaining references; that number must be 0. Then `python3 tools/vault.py check`.

Refusals (exit 1): no such note, several files with that stem, a note already named NEW, a path separator in NEW, a root contract file (`README.md` / `AGENTS.md`), or a file inside `zzz_output/`. A `zzz_output/` file that merely *links* to OLD is reported as a warning and does not block: the tool never writes there, and G3 scans loaded notes only, so those links go stale silently — the owner fixes them by hand if they care.
Moving a file is NOT renaming: a move never breaks a link, so `git mv` alone is correct.

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
