# Agent Rules for This Vault

Read this first, then the source-of-truth files it points to. Do not improvise doctrine.

## Source of truth

- `README.md` — zones, dirs, tags, promotion rule.
- `library/K_fold/Knowledge Base Operating Rules.md` — when to write a card, how to structure one, Index vs Links doctrine.
- `library/K_fold/Vault System Design.md` — why the system works, the algorithmic layer, the operating loop.
- `library/K_fold/Collaboration Workflow Spec.md` — human↔AI collaboration scenarios and role boundaries.
- `.agent/skills/vault-ops/SKILL.md` — operational procedures (load order, common problems → exact steps).

## Hard rules

1. **Wikilinks resolve by note name, not path.** Moving a file never breaks a link; renaming one requires updating every `[[Old Name]]` inbound link. Grep before renaming.
2. **Zones by state:** drafts → `mailbox/`, stable own-voice knowledge → `library/`, external/copied material → `archives/`. Root is the entry queue: new captures land there (Obsidian default) and are drained by `triage`; only `README.md` and `AGENTS.md` stay permanently.
3. **Doctrine:** Index note = big-topic navigation (`Index of ...`, tag `attr/map`, cross-topic ones in `library/Index/`). Links note = single-concept multi-angle interpretation (tag `attr/links`, stable ones in `library/Links/`). There is no "Map"/"View" vocabulary anymore.
4. **Templates** live in `template/`. New lit notes carry a real `source:` — never leave `source:` empty except in `template/lit-temp.md`.
5. **Don't touch** `zzz_output/` contents (owner's finished work) or `.obsidian/`. `zzz_output/` links and git-state may be checked/diagnosed; content is never drafted or edited by AI. `zzz_output/Root.md` is the main-tree entry (主树): tree entry `Root.md` → `Raw Index of Root` → topic indexes.
6. One note, one idea. Prefer short definitions; link instead of inlining.
7. No commits or pushes unless the owner asks. Deletions and renames need the owner's sign-off.
8. Run `python3 tools/vault.py check` before committing structural changes; before any rename/move, `grep -rn '\[\[Old Name'` first. Skill `vault-ops` at `.agent/skills/vault-ops/SKILL.md` has full procedures.

## Tags (closed set)

`type/permanent`, `type/lit`; `status/in-progress|evergreen|archive`; `attr/map`, `attr/links`, `attr/principle`, `attr/concept`, `attr/technique`, `attr/method`; plus bare `todo` on todo notes (`a_sticker/todos/` and todo-role notes) only. Additionally `topic/<name>` is an open vocabulary (free-form: `topic/learning`, `topic/math`, `topic/cs`, …) — exactly one `topic/*` tag per note recommended, checked for prefix only, not a closed set.

