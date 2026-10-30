"""Rule registry: hard gates and report-level invariants.

Populated in P4 — `check` and `rawindex --check` will both render from here so a
rule exists once. Adding a rule = appending one `Rule`.
"""

from __future__ import annotations

from collections import namedtuple

# (id, tier, title, fn) — tier is "hard" (exit 1 on finding) or "report".
Rule = namedtuple("Rule", "id tier title fn")

RULES: list = []
