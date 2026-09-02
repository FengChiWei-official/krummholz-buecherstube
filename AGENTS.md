# Agent Rules for This Vault

Read this first, then the two source-of-truth files it points to. Do not improvise doctrine.

## Source of truth

- `README.md` — zones, dirs, tags, promotion rule.
- `library/K_fold/Knowledge Base Operating Rules.md` — when to write a card, how to structure one, Index vs Links doctrine.

## Hard rules

1. **Wikilinks resolve by note name, not path.** Moving a file never breaks a link; renaming one requires updating every `[[Old Name]]` inbound link. Grep before renaming.
2. **Zones by state:** drafts → `mailbox/`, stable own-voice knowledge → `library/`, external/copied material → `archives/`. The vault root stays `README.md`-only.
3. **Doctrine:** Index note = big-topic navigation (`Index of ...`, tag `attr/map`, cross-topic ones in `library/Index/`). Links note = single-concept multi-angle interpretation (tag `attr/links`, stable ones in `library/Links/`). There is no "Map"/"View" vocabulary anymore.
4. **Templates** live in `template/`. New lit notes carry a real `source:` — never leave `source:` empty except in `template/lit-temp.md`.
5. **Don't touch** `zzz_output/` (owner's finished work) or `.obsidian/`.
6. One note, one idea. Prefer short definitions; link instead of inlining.
7. No commits or pushes unless the owner asks. Deletions and renames need the owner's sign-off.

## Tags (closed set)

`type/permanent`, `type/lit`; `status/in-progress|evergreen|archive`; `attr/map`, `attr/links`, `attr/principle`, `attr/concept`, `attr/technique`, `attr/method`.
