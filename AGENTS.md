# Agent Instructions

These are the operating rules for AI agents working in this vault.

## Directory Layout

- `root/` is only a temporary landing area.
- `mailbox/` holds active drafting, experiments, and unstable reasoning.
- `library/` holds stable personal knowledge and reusable reference cards.
- `archives/` holds imported source material and historical records.

### Directory Rules

- Scan `root/` and `mailbox/` first when organizing notes.
- Classify each note by state before moving it.
- Standardize naming before moving files.
- Preserve the note's meaning and existing links.
- Add or repair map/view links after moving.
- Do not leave duplicate copies unless the user explicitly wants a migration draft.

## Tag Taxonomy

### Status Tags

Status tags are AI-decided by default.
Do not rely on manual `status/...` editing when a note is being moved, promoted, or standardized.

- `status/in-progress` for drafts and working notes.
- `status/evergreen` for stable references and finished synthesis.
- `status/archive` for imported material.

### Type Tags

- `type/permanent` for stable personal notes.
- `type/lit` for source material.

### Attribute Tags

- `attr/map` for navigation notes.
- `attr/views` for multi-angle explanation notes.
- `attr/principle` for rule-like or method-like knowledge cards.
- `attr/concept` for definition-like concept cards.

## Decision Guide

- If the note is clearly stable, move it to `library/`.
- If the note is a navigation note, make it a map note.
- If the note is a multi-angle interpretation, make it a view note.
- If the note is still rough, keep it in `mailbox/`.
- If the note is imported material, keep it in `archives/`.

## Cleanup Priorities

- Fix obvious naming inconsistencies.
- Remove duplicated entry points.
- Add missing backlinks between related notes.
- Keep map notes broad but readable.
- Keep view notes focused on one topic.

## Notes

- The human-facing overview remains in `ZZZ_README.md`.
- The detailed knowledge-base operating rules remain in `library/trivial-thoughts/Knowledge Base Operating Rules.md`.
