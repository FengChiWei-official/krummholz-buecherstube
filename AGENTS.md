# Agent Rules for This Vault

Read this first, then the source-of-truth files it points to. Do not improvise doctrine.

## Source of truth

- `README.md` — zones, two trees, minimal memory set.
- `doctrine/Vault Design.md` — why the system works, the two trees, two-tier invariants.
- `doctrine/Vault Workflow.md` — 3 verbs + 1 loop, scenarios S1–S10, AI boundary.
- `.agent/skills/vault-ops/SKILL.md` — operational procedures (load order, common problems → exact steps).

## Hard rules

1. **Wikilinks resolve by note name, not path.** Moving a file never breaks a link; renaming one requires updating every `[[Old Name]]` inbound link. Grep before renaming.
2. **Zones by state:** external material → `archives/material/`, own archives → `archives/work/`, stable own-voice knowledge → `library/`, drafts → root (entry queue, drained by `triage`). Root is the entry queue: new captures land there (Obsidian default) and are drained by `triage`; only `README.md` and `AGENTS.md` stay permanently.
3. **Two trees (doctrine):** Raw Index = trunk (complete, unique registration, coarse: one coarse Raw Index holds several clusters, AI-grouped); Index = emergent semantic tree; Links = edges across ≥2 Index areas; Node = default genre in `<A–Z>_fold/`. Registration edge (Raw Index → Node) is a structural action, AI may append directly; `Node↔Node` and `Index→Node` links change meaning — owner approval required.
4. **No templates, no status frontmatter.** Notes are plain markdown. Fields kept: `aliases` (wikilink resolution), `source` (mandatory for `archives/material/` — hard gate). Genre by name: `Raw Index*` → `library/Raw/`, `Index of*` → `library/Index/`, `Links of*` → `library/Links/`, else fold.
5. **State lives only in the todo tree** (`a_sticker/todos/`). Unfinished work must have a `- [ ] [[NAME]]` hook + 5–10 word continuation note. `status/*`, `topic/*`, `attr/*` tags are retired — do not reintroduce them.
6. **Don't touch** `zzz_output/` contents (owner's terminal output — human-only; links and git-state may be checked/diagnosed) or `.obsidian/`. `zzz_output/Root.md` is the main-tree entry (主树): `Root.md` → `Raw Index of Root` → topic indexes.
7. One note, one idea. Prefer short definitions; link instead of inlining. AI never writes own-voice body prose; AI-generated prose belongs in `a_sticker/or/`.
8. No commits or pushes unless the owner asks. Deletions and renames need the owner's sign-off.
9. Run `python3 tools/vault.py check` before committing structural changes; before any rename/move, `grep -rn '\[\[Old Name'` first. Skill `vault-ops` at `.agent/skills/vault-ops/SKILL.md` has full procedures.

## Invariants (two-tier)

- **Hard gates** (exit 1, block commit): root drained; every `archives/material/` note has real `source:`; no NEW unresolved wikilinks (baseline whitelist in `tools/whitelist_unresolved.txt`).
- **Report-level I1–I4** (weekly increments, never block): I1 unique Raw Index registration / I2 Links cross-area (same-area = violation, no-area = hint) / I3 Node ≥1 outbound link / I4 doctrine & Raw excluded from binding neighbors.
