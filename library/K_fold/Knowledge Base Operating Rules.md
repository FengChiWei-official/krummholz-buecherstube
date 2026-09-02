---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/principle
---

## Definition

This vault works by separating state, not by forcing everything into a folder tree.

## Core Split

- [[mailbox]] stores work in progress, experiments, temporary workflows, and notes that still need shaping.
- [[library]] stores your own stable synthesis: reusable ideas, principles, definitions, and methods.
- [[archives]] stores external material or historical records that are kept for reference but are not part of your current understanding.

## Index vs Links

- An Index note organizes where to find related notes: big-topic architecture and navigation.
- A Links note organizes how to understand one concept from multiple angles.
- Index solves navigation; Links solves interpretation.
- Map == Index — one word: Index.

## Where to Store Index and Links Notes

- Large cross-topic Index notes should be placed in [[library/Index]].
- Topic-local Index notes can be placed next to their topic notes in [[library]].
- Prefer `Index of ...` naming for Index notes.
- In-progress Index or Links notes can stay in [[mailbox]] until stable.
- Stable Links notes should be promoted to [[library/Links]].

## When to Write a Card

Write a card when one of these is true:

- you can explain one idea in one sentence;
- you need a reusable method or template;
- you found a recurring pattern;
- you want to connect one idea to another.

If a note is still exploratory, keep it in [[mailbox]]. If it is already your own stable understanding, move it to [[library]].

## How to Structure a Card

- One card, one central idea.
- Prefer short, explicit definitions over long narratives.
- Add links for parent concepts, sibling concepts, and application scenes.
- Use an Index note (MOC) when a topic becomes large enough that direct browsing is no longer enough.

## How to Promote a Note

Move a note from [[mailbox]] to [[library]] when it has these traits:

- stable meaning;
- reusable across multiple contexts;
- clear wording in your own voice;
- no longer depends on active debugging or temporary context.

Keep it in [[mailbox]] when it still contains TODOs, experiments, debugging, or unfinished reasoning.

## How to Use the System

1. Capture first — root is the entry queue.
2. Link it to nearby ideas at capture time, not filing time.
3. Todo-hook unfinished work (`- [ ] [[NAME]]` in the owning todo).
4. Triage batched and cool (`python3 tools/vault.py triage`).
5. Promote only when stable (`python3 tools/vault.py promote NAME`).
6. Check before commit (`python3 tools/vault.py check`).

## Related

- [[Links of General Coding Thoughts]]
- [[Vault System Design]]
- [[middle-layer-thoughts]]
- [[standardizing-units]]