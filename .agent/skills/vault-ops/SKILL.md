---
name: vault-ops
description: "Krummholz vault operating procedures: note placement, promotion, todo-hooking, health checks, retrieval by association. Use when working in this Obsidian vault — filing, moving, renaming, triaging, or diagnosing vault structure."
---

# vault-ops

Operating procedures for the Krummholz Bücherstube vault. Never improvise doctrine; follow the load order below.

## Load order

Read in this order before acting:

1. `AGENTS.md`
2. `README.md`
3. `library/K_fold/Knowledge Base Operating Rules.md`
4. `library/K_fold/Vault System Design.md`
5. `library/K_fold/Collaboration Workflow Spec.md`

These five files are the truth. This skill restates them operationally.

## Session entry (state machine)

At the start of every session — cold or warm — run `python3 tools/vault.py status`. Report the state to the owner in plain language, then present the next-moves options from its output with a short plan per option. The owner decides; you execute. Never skip this: repo state, not memory, decides what is possible.

### Cold start

A fresh clone/pull is fully operational: all procedures live in this skill, all tools in `tools/`, all doctrine in the four source-of-truth notes. No state outside git. First session on a new machine: run `status`, then normal session entry. Note: `.obsidian/` (plugin config, incl. tag-wrangler) is gitignored — Obsidian-side conveniences are per-machine; all agent-side behavior is repo-contained.

If the owner opens with a new item ('我有一个新东西'), fold S1 into the options: tidy first if state requires, then sharpening questions + main-tree mount proposal per Spec §S7/S1.

### Resuming half-done work

A dirty tree or untracked files usually mean the last session ended mid-work. Cross-check them against the todo tree (`a_sticker/todos/`): grep each dirty/untracked note name for `- [ ] [[NAME]]` hooks and inbound links. Found → resume from the continuation note (S5). Not found → they are unsaved new work: ask the owner which todo owns them, or offer S1.

### Ambiguity → ask, never guess

If a note carries no state signal (no tags, no links, no todo hook) and no rule determines its zone or type — as with a bare one-line capture — the correct move is to ask the owner. Doctrine cannot attribute what has no attributes; guessing violates "repo state, not memory".

### Tool signals vs content

`check`/`triage`/`status` findings are signals, not verdicts. A "promote candidate" only means the evergreen tag is present — content may be empty or unstable; verify before acting. The same holds for stale and untagged findings (mtime heuristics). When a signal contradicts the note's actual content, the content wins; report the contradiction instead of forcing an action.

## Hard mechanics

- Wikilinks resolve by **note name, not path**. Renaming requires updating every `[[Old Name]]` inbound link — grep `[[Old` first.
- Root is the entry queue (Obsidian default landing). Allowed root files: `README.md`, `AGENTS.md`. Everything else gets filed.
- Tags are a closed set: `type/{permanent,lit}`, `status/{in-progress,evergreen,archive}`, `attr/{map,links,principle,concept,technique,method}`, plus bare `todo` on todo notes only.
- Lit notes need a real `source:` — never leave it empty (except `template/lit-temp.md`).
- Never touch `zzz_output/` contents (owner's finished work) or `.obsidian/`. `zzz_output/` links and git-state may be checked/diagnosed (`vault.py status` reports them); content is never drafted or edited by AI.
- Never write own-voice body content for the owner — skeleton, questions, checks, and link-proposals only; AI-generated prose belongs in `a_sticker/or/` for the owner to digest.

## Common problems → exact procedures

### Session start / unsure what to do

1. `python3 tools/vault.py status`
2. Report state + present next-moves as options per §Session entry.
3. Execute the owner's choice per Spec §S1–S6.

### New note in root

1. Run `python3 tools/vault.py triage` to see standing placement debt.
2. Decide zone by state: `archives/` (external), `mailbox/` (drafting), `library/` (stable own-voice).
3. Move with edit tools; if already evergreen in mailbox, use `python3 tools/vault.py promote NAME`.

### Note feels lost / can't find related

Three retrieval routes, in order:

1. Backlinks (Obsidian).
2. `grep -rn '[[NAME'` across the vault.
3. Tag search (intersection).

If truly orphaned, link it into the nearest `Index of` hub.

### Systematic new topic

1. Create `library/Index/Index of <Topic>.md` from `template/map-temp.md`.
2. Create `Raw Index of <Topic>` stubs from the same template.
3. Todo-hook in the relevant todo note, or create `a_sticker/todos/<Topic> Todo.md` from `template/Todo Template.md` and add a link in `Index of Todos.md`.

### Unfinished work session

Insert `- [ ] [[NAME]]` in the owning todo note (never leave work unhooked).

### Renaming

1. `grep -rn '\[\[Old Name'` first.
2. Update all `[[Old` including `|alias` forms and path-style `[[dir/Old|...`.
3. `git mv`.
4. Run `python3 tools/vault.py check`.

### Suspected duplicate

Compare content; if dup, keep the better-placed one, move inbound links, delete.

### Health audit

- `python3 tools/vault.py check` — invariants.
- `python3 tools/vault.py triage` — placement debt.

## When unsure

The default is always mailbox (reversible) over library (commitment). A wrong folder costs a move; a wrong promotion costs doctrine drift.

## Collaboration scenarios

Scenario-by-scenario protocols live in `library/K_fold/Collaboration Workflow Spec.md` (also reachable as `[[Collaboration Workflow Spec]]`). Match the trigger, follow the protocol:

| Scenario | Trigger | omp role | Protocol |
|---|---|---|---|
| S1 idea polish | owner has a new idea | ask sharpening questions, propose skeleton + related notes; never write body | Spec §S1 |
| S2 post-writing review | owner finished a note | run check, verify tags/source, propose 3–8 new links (owner approves inserts) | Spec §S2 |
| S3 systematic ingestion | starting a curriculum topic | create Index + Raw Index stubs, triage per session, enforce ≥1 cross-topic link | Spec §S3 |
| S4 output timing | topic cluster feels mature | assemble reading list; owner writes output; omp checks links + backlink | Spec §S4 |
| S5 todo fast-save | session interrupted | insert `- [ ] [[NAME]]` + continuation note into owning todo | Spec §S5 |
| S6 tag maintenance | promotion / review / taxonomy change | validate at promote, check at review, planned grep-rewrite on taxonomy change | Spec §S6 |
| S7 session entry | owner unsure what to do / opens with a new thing | run `python3 tools/vault.py status`, report state, present numbered next-move options; owner picks, omp executes per S1–S6 | Spec §S7 |
