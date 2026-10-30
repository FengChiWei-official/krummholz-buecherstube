# Changelog

## v6.0.0 (unreleased)

In-place overhaul of the vault tooling and doctrine, phased P0–P9 (plan slug
`vault-overhaul-plan`, proposal `a_sticker/or/vault-overhaul-plan.md`).

- **P0** — baseline frozen at tag `v6-start` (`tools/migrations/baseline-v6.md`).
- **P1** — trend radar stops persisting raw candidate lists: the pool lives only
  in the day's `/tmp` snapshot; `MERGE_RAW_CAP`, raw links and the automatic
  `Index of Todos` registration are gone; `TR-leaderboards.state.json` is
  gitignored.
- **P2** — `tools/` becomes a package: `tools/vaultkit/{config,parse,model,rules,cli}.py`
  with `tools/vault.toml` as the single home for zones, genres, thresholds and
  baselines; `tools/vault.py` is a thin entry point; one parser, one graph per
  process; pytest suite + fixtures + GitHub Actions CI.
- **P3** — performance and honest failure: one batched git pass, graph built
  once, explicit missing-config errors, `rawindex --sync` dry-run by default,
  `TR_SNAPSHOT_DIR`.
- **P4** — rule registry shared by `check` and `rawindex --check`; I1 split into
  I1a/I1b/I1c; I4 zone exclusion enforced; G3 scan scope stated.
- **P5** — trunk semantics tree → DAG: registration is an edge (multi-parent
  legal), cycles are the invariant.
- **P6** — learning mechanisms I5–I8 + the 计组 scaffold (owner fills prose).
- **P7** — servicization: `doctrine/Agent Contract.md`, `--json`, `help <topic>`,
  `random`, `suggest`, template ruling, skill dedup, 心法, decision ledger.
- **P8** — content cleanup: source backfill + I9, `Raw Index of Root`, obsolete
  proposal banners, retired-tag removal, history folder, registration campaign.
- **P9** — finalize.
