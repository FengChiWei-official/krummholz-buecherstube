# Changelog

## Unreleased (inside v6, after 6.0.0)

No version bump — `tools/vaultkit/__init__.py` still reports 6.0.0.

- **`docs-check [--against REV] [--gate]`** — the doc sync map
  (`doctrine/Vault Extension.md` §同步面, machine copy `tools/vault.toml
  [docs_sync]`) diffed against the working tree: names every triggered row's
  missing co-owner files. Report-level by default, `--gate` exits 1; CI runs it
  against the base commit.
- **`rename OLD NEW [--apply]`** — rename a note and cascade every inbound
  wikilink: `|alias` and `#Heading` kept, path prefixes and embeds handled,
  fenced code and inline code skipped, exact last-segment match only (renaming
  `Old` never touches `[[OldName]]`). Dry-run by default; refuses a collision, a
  path separator, a root contract file, a file inside `zzz_output/`.
- **`new NAME [--zone Z] [--template KEY] [--source S] [--todo NOTE --into T]`** —
  create a note from a scaffold: zone from state, genre from the name, template
  from `tools/vault.toml [templates]` (optional — D30), `--apply` prints 3
  candidate links (S2). Refuses a collision, a genre name outside its home zone,
  and `--zone material` without `--source` (G2).
- `check`'s scope line renders from config and now states what the code actually
  scans (loaded notes only — `zzz_output/` and `template/` were never scanned).
- `status`'s check summary renders from the rule registry; it had been reading a
  shadowed, stale second copy of the rule list.
- Doctrine: `doctrine/Vault Extension.md` (maintainer handbook + sync map),
  `doctrine/New Machine.md` (new-device runbook); ledger **D38** keeps `tests/`
  and `.pytest_cache/` out of the graph.
- Tests: 55 → 190.

## v6.0.0 (2026-10-30)

In-place overhaul of the vault tooling and doctrine, phased P0–P9 (plan slug
`vault-overhaul-plan`, proposal `a_sticker/or/vault-overhaul-plan.md`).
Measured before → after (details: `tools/migrations/baseline-v6.md`):

| metric | v5 | v6.0.0 |
|---|---|---|
| `vault.py status` wall time | 17.0 s | ~0.5 s |
| tests | 0 | 55 (pytest + fixture vault) |
| CI | none | `.github/workflows/ci.yml` |
| zones/genres/thresholds defined in code | 3 copies | 1 (`tools/vault.toml`) |
| material notes without `source:` | 49 | 0 (49 carry an honest `未记录` marker, counted by I9) |
| retired-tag files | 20 | 0 |
| registration queue | 500 | 392 |
| trunk model | tree | DAG (registration is an edge) |
| raw candidate lists in the repo | one file per day | none (`/tmp` snapshot only) |

- **P0** — baseline frozen at tag `v6-start` (`tools/migrations/baseline-v6.md`).
- **P1** — trend radar stops persisting raw candidate lists: the pool lives only
  in the day's `/tmp` snapshot; `MERGE_RAW_CAP`, raw links and the automatic
  `Index of Todos` registration are gone; `TR-leaderboards.state.json` is
  gitignored.
- **P2** — `tools/` becomes a package: `tools/vaultkit/{config,parse,model,rules,cli}.py`
  with `tools/vault.toml` as the single home for zones, genres, thresholds and
  baselines; `tools/vault.py` is a thin entry point; one parser, one graph per
  process; pytest suite + fixtures + GitHub Actions CI.
- **P3** — performance and honest failure: one batched git pass (was ~948
  subprocesses), graph built once, explicit missing-config errors, `rawindex
  --sync` dry-run by default, `TR_SNAPSHOT_DIR`.
- **P4** — rule registry shared by `check` and `rawindex --check`; I1 split into
  I1a 未登记 / I1b 重复登记边 / I1c Raw Index 环; I4's doctrine/Raw exclusion is
  real in the binding-neighbour graph; G3 states its scan scope; exit-code matrix
  in `--help`.
- **P5** — trunk semantics tree → DAG: a Node needs ≥1 registration edge, the
  same `(Raw Index, Node)` pair may not repeat, multi-parent is legal, and the
  `Raw Index → Raw Index` subgraph must stay acyclic.
- **P6** — learning mechanisms I5 (`## Mapping`) / I6 (`## 实例化`) /
  I7 (学科 `## 时间轴`) / I8 (挂点覆盖率) + the 计组 scaffold (empty tables and
  six invariant Node skeletons; owner fills the prose).
- **P7** — servicization: `doctrine/Agent Contract.md`, `--json` on every
  subcommand, `help <topic>`, `random`, `suggest`, the template ruling
  (「工具不依赖模板；模板是可选脚手架」), SKILL dedup with `--help` as the single
  source of constants, 心法, decision ledger D30–D37.
- **P8** — content cleanup: source backfill + I9, `Raw Index of Root`, obsolete
  proposal banners, retired-tag removal, `archives/work/history/`, the
  `Index of  Traditional CS` rename, and one owner-confirmed registration round
  (108 Nodes into 5 existing + 2 new Raw Indexes).
- **P9** — finalize: full pass, version markers, tag `v6.0.0`.

Known limitations (documented in `doctrine/Agent Contract.md`): the rhythm line
and todo aging are mtime proxies (a fresh clone reads 今天); a moved file has no
first-commit entry, so it is never mistaken for a fresh note; `zzz_output/Root.md`
still needs the owner's `[[Raw Index of Root]]` line.
