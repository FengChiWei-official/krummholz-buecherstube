# Agent Contract

> 版本：v6（2026-10-30）。

Self-contained handover contract for an AI (or a new human) with **zero history**.
If you read only this file plus run `python3 tools/vault.py status --json`, you can
take over correctly. Deeper why: [[Vault Design]]; operational procedures:
[[Vault Workflow]]; tool internals: `tools/vaultkit/`.

## 1. Entry commands

| command | use |
|---|---|
| `python3 tools/vault.py status` | session entry. Rhythm line + git + check summary + triage counts + trunk + numbered next moves (every move carries a copy-pasteable command) |
| `python3 tools/vault.py status --json` | the same as data — **this is the machine entry point**; every field below is in it |
| `python3 tools/vault.py help <topic>` | inline help: `triage` / `rawindex` / `dag` / `links` / `random` / `suggest` |
| `python3 tools/vault.py check` | two-tier invariant report; exit 1 only when a hard gate fails |
| `python3 tools/vault.py triage` | placement debt (root, todo aging, half-done, unhooked, genre, dead todo) |
| `python3 tools/vault.py rawindex [...]` | trunk operations: queue + L0 归队 / `--clusters` / `--check` / `--sync` / `--around NAME` |
| `python3 tools/vault.py random [--scope …] [--seed N]` | 问箱 material (S9): one note + its backlinks |
| `python3 tools/vault.py suggest NAME [--n 3]` | candidate links for a note, one why-line each (S2) |
| `python3 tools/trend_radar.py …` | daily intel flow (see `.agent/skills/trend-radar/SKILL.md`) |

Every subcommand accepts `--json` (one JSON document on stdout, nothing else) and
`--strict` (a missing config/list file becomes a fatal error instead of a warning).
`--vault` is not a flag: set `VAULT_ROOT` to point the tools at another vault.

### Exit codes

| code | meaning |
|---|---|
| 0 | ok — every report, and any `check` whose hard gates are green |
| 1 | a hard gate failed (`check`), or an unknown target (`rawindex --around`, `suggest`) |
| 2 | missing/unreadable config; a missing list file under `--strict`; unknown `help` topic |

## 2. Where state lives

**The todo tree is the only state store.** `a_sticker/todos/`, registered through
`Index of Todos.md`. Unfinished work = `- [ ] [[NAME]] — 5–10 word continuation note`.
There are no status fields, no `status/*` tags, no `topic/*` tags, no frontmatter
beyond `aliases:` and `source:`. Do not invent a second state store — a fact that is
not in a note is not in the system.

## 3. What you may do directly (structural actions)

- **Registration edges** (`Raw Index → Node`): append `[[Node]]` lines to a Raw
  Index. That is bookkeeping, not meaning (D22).
- **Structure repair**: rename/re-home a file to its doctrine-correct zone,
  fix a dangling link to a note that exists, drain the root queue into a zone.
- **Run the tools** and act on their signals: `rawindex` L0 proposals with
  confidence at or above `l0_confidence` (`tools/vault.toml`), `triage` categories,
  `rawindex --clusters` grouping proposals.
- **Scaffolds**: create a note's headings/empty tables, and `a_sticker/or/` drafts.
  Never the body prose of a `library/` note.

## 4. What needs owner approval

- **New `Node ↔ Node` and `Index → Node` links.** Links change meaning; the owner
  approves each one. (A `suggest` run is a proposal, not an edit.)
- **Deletions and renames** (the owner signs off; `git mv` keeps history).
- **Commits and pushes.** Never commit or push unless asked.
- **Cluster commonality sentences and new Raw Index names** (D16): the AI proposes
  the grouping, the owner writes the sentence and picks the name.
- **Any change to `.obsidian/`** — per-machine settings are the owner's.

## 5. What you must never do

- Write or edit anything in `zzz_output/` (owner's terminal output; git state and
  links may be *read*).
- Write own-voice body prose in `library/`. AI prose belongs in `a_sticker/or/`.
- Touch `.obsidian/`, add big binaries to the repo (T22: no large assets; the vault
  is text), or commit.
- Reintroduce retired tags or status fields.

## 6. How to verify yourself

| command | expected |
|---|---|
| `python3 tools/vault.py check` | hard gates (G1 root drained / G2 material `source:` / G3 NEW unresolved wikilinks) green → exit 0; report-level I1a/I1b/I1c, I2, I3, I4, I5–I8, D21 lines carry counts that should trend down, never block |
| `python3 tools/vault.py triage` | 6 category counts; every line is a *prompt*, not a verdict |
| `python3 tools/vault.py status` | rhythm line, git state, check summary, trunk counts, numbered moves |
| `python3 tools/vault.py rawindex --check` | the same rule registry as `check`, trunk-facing |
| `python3 tools/trend_radar.py verify` | the day's snapshot + report + index + leaderboards |

`check` before and after any structural change. `python3 -m pytest -q` runs the
tool's own suite (`tests/`), including a fixture vault.

### Facts the tools rely on (do not "fix" them)

- **G3 scan scope**: every `*.md` except the `skip_dirs` in `tools/vault.toml`
  (`.git`, `.obsidian`, `.agent`). Note *loading* additionally skips
  `zzz_output/` and `template/`, but names found there still resolve links.
  So a dangling link in a skipped dir is invisible — that is why an absent
  `Raw Index of Root` went unnoticed.
- **Rhythm line is a proxy, not a log**: 整理 = todos dir mtime / last commit,
  聚簇 = `library/Raw/`, 问箱 = `library/Links/`, 产出 = `zzz_output/`. On a fresh
  clone (no git history) the mtimes are checkout time, so it reads 今天.
- **Todo aging is file-level**: the mtime of each `a_sticker/todos/*.md` at the top
  level only — `a_sticker/todos/archived/` is exempt.
- **Empty notes bypass the half-done age window**: a zero-byte note has no link
  signal at all, so `triage` lists it regardless of creation time. A moved file has
  no first-commit entry either (git reports the move as a rename), so a moved note
  is never mistaken for a fresh one.
- **`rawindex --sync` is dry-run by default** (L13 write safety). Only `--apply` writes.
- **`tools/vault.toml` is the single home** for zones, genres, thresholds, paths and
  baselines. Never hardcode a threshold in code or docs.
- **Tasks that need a shell**: git archaeology (`git log --diff-filter=A …`),
  running the tools, `pytest`. A subagent without shell access cannot do them.
- **`omp` config writes are session-only** unless saved explicitly; treat any
  setting you change as temporary until the owner saves it.

## 7. Bootstrap checklist (zero context, in order)

1. `python3 tools/vault.py status --json` — read `trunk`, `triage`, `next_moves`,
   `exit_codes`.
2. Read this file (you are here), then [[Vault Design]] §两棵树 and
   [[Vault Workflow]] §心法 if you need the why.
3. `python3 tools/vault.py check` — confirm hard gates are green before touching
   anything. If a gate is red, fix that first and nothing else.
4. `python3 tools/vault.py help rawindex` — learn the trunk operations you are
   allowed to run unattended.
5. Take the first `next_moves` item whose command you can copy verbatim.
6. After any change: `check` again, then `git status` to show the owner what moved.
7. Report in the owner's terms: what moved, which gate/rule changed, what you did
   not touch. Never claim a verification you did not run.

## Related

- [[Vault Design]]
- [[Vault Workflow]]
