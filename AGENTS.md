# Agent Rules for This Vault

Read this first, then the source-of-truth files it points to. Do not improvise doctrine.

## Source of truth

- `README.md` — zones, two trees, minimal memory set.
- `doctrine/Agent Contract.md` — AI handover contract: entry commands, direct vs owner-approval actions, never-do list, self-verification, bootstrap checklist.
- `doctrine/Vault Design.md` — why the system works, the two trees, two-tier invariants.
- `doctrine/Vault Workflow.md` — 3 verbs + 1 loop, scenarios S1–S10, 心法, AI boundary.
- `doctrine/Vault Extension.md` — 维护者手册：不可破坏的特性、改法配方、**文档同步面**（改一处要同步哪几处）。
- `doctrine/New Machine.md` — 新设备复现清单：仓库里有 vs 每机各异、插件与设置、验收。
- `.agent/skills/vault-ops/SKILL.md` — operational procedures (load order, common problems → exact steps).
- `tools/vault.toml` — the single definition of zones, genres, thresholds and paths; `python3 tools/vault.py help <topic>` for inline help.

## Hard rules

1. **Wikilinks resolve by note name, not path.** Moving a file never breaks a link; renaming one requires updating every `[[Old Name]]` inbound link — `python3 tools/vault.py rename OLD NEW` does the cascade (dry-run; refuses a name collision, a path separator, a root contract file and a file inside `zzz_output/`). Grep before renaming by hand.
2. **Zones by state:** external material → `archives/material/`, own archives → `archives/work/`, stable own-voice knowledge → `library/`, drafts → root (entry queue, drained by `triage`). Root is the entry queue: new captures land there (Obsidian default) and are drained by `triage`; only `README.md` and `AGENTS.md` stay permanently. `python3 tools/vault.py new NAME --zone Z` creates a note this way (zone from state, genre from the name, `archives/material/` refuses without `--source`).
3. **Two trees (doctrine):** Raw Index = trunk (complete, ≥1 registration edge, coarse: one coarse Raw Index holds several clusters, AI-grouped); Index = emergent semantic tree; Links = edges across ≥2 Index areas; Node = default genre in `<A–Z>_fold/`. Registration is an edge, not a parent: the same `(Raw Index, Node)` pair may not repeat, a Node may carry several registration edges, and `Raw Index → Raw Index` must stay acyclic (I1a/I1b/I1c). Registration edge (Raw Index → Node) is a structural action, AI may append directly; `Node↔Node` and `Index→Node` links change meaning — owner approval required.
4. **No required templates, no status frontmatter.** Notes are plain markdown — the tools never depend on a template, and `template/` holds optional scaffolds only (notes are not required to fill any template section). Fields kept: `aliases` (wikilink resolution), `source` (mandatory for `archives/material/` — hard gate). Genre by name: `Raw Index*` → `library/Raw/`, `Index of*` → `library/Index/`, `Links of*` → `library/Links/`, else fold.
5. **State lives only in the todo tree** (`a_sticker/todos/`). Unfinished work must have a `- [ ] [[NAME]]` hook + 5–10 word continuation note. `status/*`, `topic/*`, `attr/*` tags are retired — do not reintroduce them.
6. **Don't touch** `zzz_output/` contents (owner's terminal output — human-only; links and git-state may be checked/diagnosed) or `.obsidian/`. `zzz_output/Root.md` is the main-tree entry (主树): `Root.md` → `Raw Index of Root` → topic indexes.
7. One note, one idea. Prefer short definitions; link instead of inlining. AI never writes own-voice body prose; AI-generated prose belongs in `a_sticker/or/`.
8. No commits or pushes unless the owner asks. Deletions and renames need the owner's sign-off.
9. Run `python3 tools/vault.py check` before committing structural changes; before any rename/move, `grep -rn -- '\[\[Old Name'` first. Procedures: `.agent/skills/vault-ops/SKILL.md`; handover contract: `doctrine/Agent Contract.md`; inline help: `python3 tools/vault.py help <topic>`.
10. **改文档或工具文案前**，先读 `doctrine/Vault Extension.md` §同步面——它列了「改一处要同步哪几处」；文档与 `check` 的报告级输出互相矛盾就是漂移。机器门：`python3 tools/vault.py docs-check --gate`（默认报告级；`tests/test_docs.py` 在 CI 里强制内容一致性）。

## Invariants (two-tier)

- **Hard gates** (exit 1, block commit): G1 root drained; G2 every `archives/material/` note has real `source:`; G3 no NEW unresolved wikilinks (baseline whitelist in `tools/whitelist_unresolved.txt`, currently 0 entries).
- **Report-level** (weekly increments, never block): I1a 未登记 / I1b 重复登记边 / I1c Raw Index 环 / I2 Links cross-area (same-area = violation, no-area = hint) / I3 Node ≥1 outbound link / I4 doctrine & Raw excluded from binding neighbors / I5 Mapping / I6 实例化 / I7 时间轴 / I8 挂点覆盖率 / I9 un-recorded material source / D21 未拆材料.
- Every rule is one entry in `tools/vaultkit/rules.py`; every threshold lives once in `tools/vault.toml`. Never hardcode either in a doc.
