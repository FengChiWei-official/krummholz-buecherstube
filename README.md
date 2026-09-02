# Knowledge Base

This vault is a modified Zettelkasten. It is organized by **state**, not by a folder tree: atomic cards, explicit links, and your own voice over collected material.

## Core Zones

- `mailbox/` — work in progress: drafts, experiments, notes still being shaped.
- `library/` — stable knowledge in your own voice: reusable ideas, principles, definitions, methods, indexes.
- `archives/` — external material kept for reference: quotations, transcripts, copied sources.
- Root — a temporary landing area. Keep it small; drain it into the three zones above.

## Support Dirs

- `library/Index/` — cross-topic Index notes (`Index of ...`). Topic-local indexes may stay beside their topic in the letter folds.
- `library/Links/` — Links notes: one concept from multiple angles — isomorphisms, cross-topic connections.
- `library/<A–Z>_fold/` — stable cards, sharded by first letter.
- `zzz_output/` — the vault's terminal output: finished own-voice works (essays, summaries, proposals, poems) that link viewpoints from `library/` — the proof of having learned. `Root.md` in it is the default tree entry (主树) into the knowledge network. The `zzz_` prefix keeps it last in the sidebar.
- `a_sticker/` — scratch: `todos/` task lists (`Index of Todos.md` is the todo-tree registry), `or/` AI-conversation captures, `new_terms/` vocab staging.
- `template/` — card scaffolds: `concept/method/principle/technique/map/links/lit-temp.md` + `Todo Template.md`.

## Tooling

- `python3 tools/vault.py check` — invariant report (root drained, lit sources, tag vocabulary, wikilink integrity, orphans). Run before committing structural changes.
- `python3 tools/vault.py triage` — placement-debt report (root files, stalled promotions, stale in-progress, untagged notes, dead todo references).
- `python3 tools/vault.py promote NAME` — graduate a mailbox note into library (validates status and tags; `--dry-run` prints the plan).
- `python3 tools/vault.py status` — session-entry state report (git + invariants + placement debt + next moves). Run this first in any session.


## Index vs Links

- An **Index note** is big-topic architecture: it tells you *where things live*.
- A **Links note** is single-concept synthesis: it tells you *how to understand* something from multiple angles.
- Index solves navigation. Links solves interpretation.
- Map == Index — one word: Index.

### Index Notes

- Tag `attr/map`; name them `Index of ...`.
- Cross-topic indexes live in `library/Index/`; topic-local ones live beside their topic.
- In-progress indexes stay in `mailbox/` until stable.

### Links Notes

- Tag `attr/links`.
- Write one when a concept needs multiple perspectives, examples, or distinctions.
- Shape them in `mailbox/`; promote to `library/Links/` when mature.

## How to Use the Vault

1. Capture the note quickly.
2. Decide whether it is external material, active drafting, or stable knowledge.
3. Put it in the right zone.
4. Add links to nearby notes.
5. Promote it only when the wording and meaning are stable.
6. For human↔AI collaboration scenarios (idea polishing, review, ingestion, output, todo, tags), follow [Collaboration Workflow Spec](library/K_fold/Collaboration%20Workflow%20Spec.md).
7. When a cluster is truly learned, publish to `zzz_output/` and link it into the main tree via the criteria in the Collaboration Workflow Spec (§S4).
8. Unsure what to do at any point? Run `python3 tools/vault.py status` (or ask the AI to) — it reports state and options.

## Where a Note Belongs

- `archives/` — copied from a source, mainly quotation or reference, not yet rewritten in your own words.
- `mailbox/` — still exploratory: TODOs, rough proofs, unstable structure you expect to change.
- `library/` — your own voice, reusable across contexts, stable enough to serve as a reference card.

Root files should not stay unmanaged. Move a root file into `mailbox/`, `library/`, or `archives/` by the rules above — or convert it into an Index note if it guides navigation.

### Working in mailbox/

- Rewrite rough notes into clearer cards; split large notes into smaller ones.
- Add missing links.
- Keep `status/in-progress` while refining.

### Working in library/

- One note, one idea.
- Prefer short, explicit definitions over narratives.
- Use Index notes to organize broad topics.
- Promote out of mailbox only what is ready.

## Recommended Tags

- `type/permanent` — stable personal notes.
- `type/lit` — source material. **A lit note MUST carry a real `source:`.**
- `status/in-progress` — drafts and notes still being shaped.
- `status/evergreen` — stable references, finished synthesis.
- `status/archive` — imported material.
- `attr/map` — navigation notes.
- `attr/links` — multi-angle explanation notes.
- `attr/principle`, `attr/concept` — ordinary knowledge cards.
- `attr/technique`, `attr/method` — hands-on technique and method cards.
- `topic/<name>` — open vocabulary, one per note (`topic/learning`, `topic/math`, `topic/cs`, …). Not a closed set; checked for prefix only.

## Promotion Rule

A note moves from `mailbox/` to `library/` when:

- its meaning is stable;
- it is reusable in more than one context;
- the wording is clean and short;
- it no longer depends on temporary debugging or active drafting.

## Related Files

- [Knowledge Base Operating Rules](library/K_fold/Knowledge%20Base%20Operating%20Rules.md)
- [Links of General Coding Thoughts](library/Links/Links%20of%20General%20Coding%20Thoughts.md)
- [Vault System Design](library/K_fold/Vault%20System%20Design.md)
- [Collaboration Workflow Spec](library/K_fold/Collaboration%20Workflow%20Spec.md)
- [Index of Knowledge](library/Index/Index%20of%20Knowledge.md)
