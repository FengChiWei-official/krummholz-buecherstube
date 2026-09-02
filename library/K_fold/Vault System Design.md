---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/map
---

## Definition

This vault's management problem is not a discipline problem. It is a structural one: the physical layout is a *fixed* hierarchy, but knowledge arrival is *associative* and unordered. The fix is a second, algorithmic layer on top of the physical one.

The system in one line: **the folder tree stores state, the links store meaning, the tags store retrievability, the tools store discipline.** Manual management broke because it tried to make the folder tree do all four jobs.

Three layers, three jobs:

- **Human** = content. Own voice, own words. Nothing here substitutes for that.
- **Obsidian** = medium. Backlinks, unresolved-link pane, tag search, graph — the association engine.
- **omp (AI)** = structure and discipline. Checks, triage, link discovery, filing mechanics. Never the voice.

## Why Manual Management Breaks Down

Every note demands a placement decision at the worst moment: right after writing, when the idea is hot. Root accumulation is not a discipline failure — it is the default Obsidian landing spot (`app.json` sets no `newFileLocation`) plus a decision tax per note. At ~900 files, the marginal cost of "decide the folder + move + link + update todo + commit" per note exceeds the value of writing it down, so notes stall (observed: 18 mailbox strays, 338 in-progress in library). The fix is not more discipline; it is moving the placement decision from hot (per note) to cool (batched).

## Systematic vs Non-Systematic Knowledge

A curriculum (OS, Calculus, Abstract Algebra) arrives as a pre-shaped tree. The vault already answers this with `Index of ...` + `Raw Index` scaffolding; friction there is only that index templates and fill-in discipline are manual. The real gap: no *forced* connection between the systematic tree and the associative layer. Systematic notes end up linked only within their own topic, so cross-topic insight — the Zettelkasten payoff — never happens.

Rule: **every promoted systematic note must link at least one concept outside its own index, or stay in mailbox.**

## Anti-Loss Design

Scattered notes fail not by being wrong but by being *unfindable*. Anti-loss is structural:

- Every note carries `type`/`status`/`attr` tags — tags are the retrieval index, not decoration.
- Dangling `[[links]]` are allowed as hooks — they make absence visible in backlinks.
- The todo tree guarantees nothing is silently dropped — unfinished work must have a todo entry.
- `triage` output is the standing list of un-anchored notes.

## Retrieval by Association

Obsidian's backlinks + unresolved-link pane do 80% of retrieval. The vault adds: search by tag intersection (`attr/links` + topic), entering via the top-level indexes (`Index of Knowledge` → topic index → note), and Links notes as pre-computed multi-angle entry points.

Retrieval rule: **when writing a new note, link it to at least one existing note immediately — a note with zero inbound links is invisible to association.**

## The Algorithmic Layer

Physical = zones/folds (unchanged; they encode state). Algorithmic = the recurring procedures that keep the physical layer honest:

- `python3 tools/vault.py check` — invariants: root drained, lit notes have real `source:`, tag vocabulary, wikilink integrity, orphans (informational).
- `python3 tools/vault.py triage` — placement debt: root files, stalled promotions, stale in-progress (mtime heuristic — prompt, not verdict), untagged notes, dead checked todo references.
- `python3 tools/vault.py promote NAME` — the graduation ceremony: mailbox → library, validates status/tags, files by letter fold (`0_fold` for digit-leading, `中_fold` for CJK), refuses `type/lit`.
- Todo tree (`a_sticker/todos/Index of Todos.md`) — work debt.
- Git — history.

## Workflow (operating logic)

The corrected loop:

1. **Capture** — root is fine; it is the entry queue, not an error state.
2. **Link** — must happen at capture time, not filing time.
3. **Todo-hook** — unfinished work gets a `- [ ] [[NAME]]` entry.
4. **Triage** — batched, cool (`python3 tools/vault.py triage`).
5. **Promote** — when stable (`python3 tools/vault.py promote NAME`).
6. **Check** — before commit (`python3 tools/vault.py check`).

Filing moves from per-note hot decision to batched cool decision — that is why it becomes sustainable.

Scenario-by-scenario protocols: [[Collaboration Workflow Spec]].

---
## **Related**

- [[Knowledge Base Operating Rules]]
- [[Index of Todos]]
