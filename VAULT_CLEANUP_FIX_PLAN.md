# Vault Cleanup & Taxonomy Restructure Plan

**Vault**: `/home/mia/Documents/obsidian/krummholz-buecherstube` (all paths below relative to it)
**Working tree state**: git `main @ 0a3c78a`, one unstaged deletion (`AGENTS.md`, intentionally deleted — do NOT recreate).

## Context

The vault is a modified Zettelkasten organized by note state (`archives/` external → `mailbox/` drafts → `library/` stable). The owner wants: (1) the vault cleaned per its own rules, (2) the view/map doctrine replaced — **Map==Index** (big-topic architecture/navigation) and former "views" renamed to **Links** (single-concept / cross-topic multi-angle synthesis), with structure `library/Index/` + `library/Links/` replacing `library/_index_/`, (3) README fixed to describe reality (4 broken links, undocumented dirs `zzz_output/`, `a_sticker/`, `template/`, missing `attr/technique`/`attr/method` in taxonomy). Owner decisions (this conversation): stale `source: 《卡片盒笔记法》 by Sönke Ahrens` template-artifact lines removed **everywhere** (172+ files); rename scope = typos + archives/tricks prefix normalization; 人生规划.md + 人生规划2.md merged into one mailbox note.

Obsidian wikilinks resolve by note **name**, so directory moves never break links; only **renames** require inbound-link updates. Every rename below lists verified inbound links; re-grep at execution before each rename to catch any missed.

No git commit — leave changes in the working tree.

---

## Step 1 — Fix git conflict-marker file (independent)

**`library/A_fold/Alignment between Ordered Data Beats Mapping.md`** currently contains stash-conflict markers fusing two notes. The stashed side's content (aliases `Count chars (a-z) efficiency`, `Frequency Array`) already exists verbatim in `library/B_fold/Bucketing Chars.md` — nothing is lost by discarding it.

Edit the file to exactly:
```markdown
---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/technique
---

## Definition

## E.g.
[[CSP202006B. 稀疏向量]]

---
## **Related**

[[Using Hashing to Verify Bucket Array Equality]]
```
(Removes `<<<<<<<< Updated upstream...` / `========` / aliases / `>>>>>>>> Stashed changes...` lines 7–12; body preserved as-is.)

## Step 2 — Create new structure, restructure `library/_index_/` (78 files)

Create `library/Index/` and `library/Links/`. Move every `_index_/` file per the disposition below. **Naming rules**: `View of X`→`Links of X`; `View X`/`Views X`→`Links of X` (strip leading View(s), prepend `Links of`); `Map of X`→`Index of X`; `Raw Map`→`Raw Index` (keep the `Raw` prefix — it marks unrefined maps). Delete `library/_index_/` when empty.

**→ `library/Index/`** (no rename unless noted; retag where noted):
`history-of-attention.md`, `How do PC system work.md`, `Structure of Computer Network.md`, `Index of Abstract Algebra.md`, `Index of Algorithm.md`, `Index of Binary Tree.md`, `Index of Calculus.md`, `Index of Deutsch Grammar.md`, `Index of Identity Transform.md`, `Index of Limit Strategy.md`, `Index of Linear Algebra.md`, `Index of Math Expressions Pattern.md`, `Index of Math.md`, `Index of Operating System.md`, `Index of Scaling and Normalization.md`, `Index of Structural Exploitation.md`, `Index of Useful Functions.md`, `Index of Vector Calculus & Geometry of Curves.md` *(retag `attr/views`→`attr/map`)*, `Raw Index of Root.md`, `大模型微调完整指南-MOC.md` *(retag `type/moc`→`type/permanent`; keep `cs/llm`, `ml/fine-tuning`, `attr/map`, `status/evergreen`)*, `Table Method for Integration by Parts.md`, `Table of Basic Integrals.md`, `Table of Integrals.md`, `Table of Trigonometric Function Integrals.md`, `Table of 双元 Integrals.md`, `Table of 反三角和双元.md`, `Table of ADTs.md` *(retag lit residue → `type/permanent`, `status/in-progress`, `topic/learning`, `attr/concept`)*.

Renamed while moving (old → new):
- `Index Common types of kinematics basic problems.md` → `Index of Common Types of Kinematics Basic Problems.md` *(retag `attr/principle`→`attr/map`)*
- `Index Linux Virtual Machine.md` → `Index of Linux Virtual Machine.md`
- `Index of Core Concept of OS.md` *(retag principle→map)*
- `Index of History of  Operating System.md` → `Index of History of Operating System.md` *(fix double space; retag principle→map)*
- `Index of Process.md` *(retag principle→map)*
- `Index of Range Sum Query - like Problem.md` *(retag principle→map)*
- `Map of Concepts of Data.md` → `Index of Concepts of Data.md`
- `Map of Data Structure.md` → `Index of Data Structure.md` *(also fix lit-residue frontmatter → `type/permanent`, `status/in-progress`, `topic/learning`, `attr/map`)*
- `Map of Knowledge.md` → `Index of Knowledge.md`
- `Map of Music.md` → `Index of Music.md`
- `Map of Relationship.md` → `Index of Relationship.md`
- `Map of my Presets.md` → `Index of my Presets.md`
- `Raw Map for Integral Toolkits.md` → `Raw Index for Integral Toolkits.md`
- `Raw Map Function Properties Toolkit.md` → `Raw Index Function Properties Toolkit.md`
- `Raw Map Function Structure Toolkit.md` → `Raw Index Function Structure Toolkit.md`
- `Raw Map Function Toolkits.md` → `Raw Index Function Toolkits.md`
- `Raw Map Variation Substitution Toolkit.md` → `Raw Index Variation Substitution Toolkit.md`
- `Raw Map of Coding.md` → `Raw Index of Coding.md`
- `Raw map of Songs.md` → `Raw Index of Songs.md`
- `Raw Map of Tricks in Math.md` → `Raw Index of Tricks in Math.md` *(retag `attr/views`→`attr/map`)*

**→ `library/Links/`** (all renamed `View(s)…`→`Links of …`; tag `attr/views`→`attr/links`; retag `attr/principle`→`attr/links` where noted):
- `View of Addtive Group of Integer.md` → `Links of Additive Group of Integer.md` *(typo fix + principle→links)*
- `View of Cyclic Subgroup or Group.md` → `Links of Cyclic Subgroup or Group.md` *(principle→links)*
- `View of Group.md` → `Links of Group.md` *(principle→links)*
- `View of Vector-valued Function.md` → `Links of Vector-valued Function.md` *(principle→links)*
- `View of Parity Indentity.md` → `Links of Parity Identity.md` *(typo fix)*
- `View How to choice the Implement of Linear List.md` → `Links of How to Choose the Implementation of Linear List.md`
- `Views of Function Properties.md` → `Links of Function Properties.md`
- `View Properties of Trees.md` → `Links of Properties of Trees.md`
- `View Properties of Binary Trees.md` → `Links of Properties of Binary Trees.md`
- `View of All Important Function in Composition.md` → `Links of All Important Function in Composition.md`
- `View of Bit Manipulation.md` → `Links of Bit Manipulation.md`
- `View of Composition of a Function with a Monotonic Function.md` → `Links of Composition of a Function with a Monotonic Function.md`
- `View of Continuity.md` → `Links of Continuity.md`
- `View of Formula Sheet.md` → `Links of Formula Sheet.md`
- `View of General Coding Thoughts.md` → `Links of General Coding Thoughts.md`
- `View of Handle Inequalities with Absolute Expressions.md` → `Links of Handle Inequalities with Absolute Expressions.md`
- `View of Handling Points Discontinuity.md` → `Links of Handling Points Discontinuity.md`
- `View of Inverse Trigonometric Identity.md` → `Links of Inverse Trigonometric Identity.md`
- `View of Knapsack DP.md` → `Links of Knapsack DP.md`
- `View of LXS.md` → `Links of LXS.md`
- `View of Monotonicity in Transformations.md` → `Links of Monotonicity in Transformations.md`
- `View of Parity in Transformations.md` → `Links of Parity in Transformations.md`
- `View of Periodicity in Transformations.md` → `Links of Periodicity in Transformations.md`
- `View of Properties of Specific Transform.md` → `Links of Properties of Specific Transform.md`
- `View of Solve with Definition of Continuous.md` → `Links of Solve with Definition of Continuous.md`
- `View of Solving Limit of Sequence.md` → `Links of Solving Limit of Sequence.md`
- `View of Solving Limitation of Function.md` → `Links of Solving Limitation of Function.md`
- `View of Sum and Product.md` → `Links of Sum and Product.md`
- `View of Visited.md` → `Links of Visited.md`

**→ `library/T_fold/`**: `The relationship between the number of vertices and edges in a tree.md` (attr/concept card misfiled in the hub dir; no rename).

**Inbound-link updates for renames** (verified hits; re-grep each old name vault-wide at execution, replace `[[OLD` → `[[NEW` preserving `|alias` parts):
- `Map of Programming Language` ← `library/_index_/Map of Knowledge.md:13` (becomes `Index of Programming Language`, see Step 4)
- `Raw Map of Sequence Toolkits`, `Raw Map of Series Toolkits`, `Raw Map of Mathematical Heuristics` ← `Raw Map of Tricks in Math.md:21-22,33` (targets renamed in Step 4)
- `View of Addtive Group of Integer` ← `library/A_fold/Additive Group of Integers.md:17`, `Index of Abstract Algebra.md:111`
- `View of Parity Indentity` ← `Index of Identity Transform.md:29`, `Views of Function Properties.md:21`
- `View How to choice the Implement of Linear List` ← `library/L_fold/Linear List.md:26`, `Raw Map of Data Structure.md:15`
- `Views of Function Properties` ← `a_sticker/todos/Math Todo.md:17`, `library/P_fold/Properties of Functions.md:20`, `Index of Calculus.md:19`
- `Index of History of  Operating System` ← `Index of Operating System.md:23`
- `Sequential List v.s. Linked List` handled in Step 6.

## Step 3 — Global tag + text fixes

1. **Tag rename**: `attr/views` → `attr/links` in every remaining file vault-wide (verified 45 files carry it; after Step 2 the `_index_` ones are done — remaining: `library/A_fold/Algorithm tips.md`, `library/A_fold/AM-GM Inequality.md`, `library/B_fold/Build up Your Geometric Building.md`, `library/C_fold/Common Types of Limit Problems.md`, `library/D_fold/Different Types of State.md`, `library/F_fold/function and continuous and differential function.md`, `library/I_fold/Identities of Trigonometric Function.md`, `library/I_fold/Instinct of Special Functions.md`, `library/L_fold/Latin 动词过去分词词干的派生.md`, `library/Tree Mental Models.md`, `library/Types of BFS & DFS.md`, `archives/algorithms/CSP 真题.md`, `archives/engineering/Hyprland Workspace Config Templates.md`, `mailbox/Logarithmic Function Toolkit.md`, `mailbox/Partial Sum Sequence Toolkit.md`, `mailbox/Telescoping Sum Toolkits.md`, `template/views-temp.md`, `README.md`). These files stay where they are (topic-local links notes live beside their topic).
2. **Stale source removal**: delete every line matching `source: 《卡片盒笔记法》 by Sönke Ahrens` (172+ files). Exception: in `苛政猛於虎.md` (moved in Step 4) replace it with `source: 《礼记·檀弓下》` (the passage 孔子過泰山側 is from there). Also fix the corrupted variant in `archives/reading-notes/看过的番剧.md:6` (`sourceobsidian://open?vault=...: 《卡片盒笔记法》 by Sönke Ahrens`) — delete that whole line.
3. **template/lit-temp.md**: replace the hardcoded source line with `source: ` (empty placeholder; the hardcoded Ahrens value is what leaked into 172 files).
4. **template/views-temp.md** → rename file to `template/links-temp.md`, tag `attr/views`→`attr/links`.
5. **a_sticker/todos/Animation Todo.md**: retag frontmatter to `tags: [todo]` (it is a watchlist, not a lit note), remove the source line (covered by 2).
6. **a_sticker/todos/Hobby todo.md:10**: delete the empty checklist item `- [ ] [[]]`.
7. **library/T_fold/The Cyclic Decomposition Theorem...md**: fix alias typo `Addtive Subgroup of Integers is In shape of Za` → `Additive Subgroup of Integers is In shape of Za`, and the matching `[[...|Addtive Subgroup...]]` display text at line 16.

## Step 4 — Drain the vault root (13 notes)

All wikilinks are name-based; moves break nothing.

- **→ `mailbox/`** (7 in-progress concept stubs): `Abstract Data Type.md`, `Abstract Data Type in Programming Language.md`, `Algebraic Data Types.md`, `Enumeration Types.md`, `Product Types.md`, `Functional Programming Language.md`, `Lazy Evaluation.md`.
- **Alias dedup** (three files currently claim alias `ADT`): keep `aliases: [ADT]` only on `mailbox/Abstract Data Type.md` (the concept hub); remove the `aliases: - ADT` block from `mailbox/Abstract Data Type in Programming Language.md` and `library/A_fold/Abstract Data Type in Data Structure.md`.
- **→ `library/Index/`**: `Index of 文学.md`, `Index of 汉语言学.md`, and `Lit 古代汉语学习笔记.md` (verified: it is an `attr/map` evergreen hub linking 苛政猛於虎, not a lit duplicate as one scout claimed).
- **→ `archives/`** (top level): `苛政猛於虎.md` (`type/lit`, `status/archive`; set real source per Step 3.2).
- **Merge 人生规划**: read both `人生规划.md` and `人生规划2.md` fully. Keep `人生规划.md` as the base, move to `mailbox/人生规划.md`. Append the unique content of 人生规划2.md (the four-dimension self-diagnostic: 建造者 vs 探索者 / pain-tolerance / generalist vs specialist / safety assets, plus its action plan) as new `##` sections after the existing philosophy/practice content. Where both repeat the same theme (重力坝 metaphor, 考研-as-entry-ticket, realism-over-ideology), keep the fuller phrasing once. Frontmatter: `tags: [type/permanent, status/in-progress, topic/learning]`. Delete `人生规划2.md`. Update `library/L_fold/Life todo.md:12-13`: `[[人生规划]]` + `[[人生规划2]]` → single `[[人生规划]]` (note: Life todo.md itself moves in Step 5).

## Step 5 — Promote stable notes out of mailbox; dedupe; relocate strays

1. **Promote evergreen maps → `library/Index/`** (rename per Step 2 rules):
   - `mailbox/Raw Map of Mathematical Heuristics.md` → `library/Index/Raw Index of Mathematical Heuristics.md`
   - `mailbox/Raw Map of Sequence Toolkits.md` → `library/Index/Raw Index of Sequence Toolkits.md`
   - `mailbox/Raw Map of Series Toolkits.md` → `library/Index/Raw Index of Series Toolkits.md` (its self-reference `[[Raw Map of Sequence Toolkits]]:21` → `[[Raw Index of Sequence Toolkits]]`)
   - `mailbox/Map/Map of Programming Language.md` + `mailbox/Map/Map of Fuctional Programming.md` → both are near-empty evergreen map stubs of the same topic; merge into one `library/Index/Index of Programming Language.md` with frontmatter `tags: [type/permanent, status/evergreen, topic/learning, attr/map]` and body: `## Definition`, `## Core Concepts`, `## Key Methods`, `## Applications`, `## **Related**` (merge the two bodies; drop Map of Programming Language's self-link `[[Map of Programming Language]]:13`).
   - Update inbound: `library/Index/Index of Knowledge.md` (formerly Map of Knowledge) line 13 `[[Map of Programming Language]]` → `[[Index of Programming Language]]`.
2. **`mailbox/View/View of Haskell's Properties.md`** → rename+move to `mailbox/Links of Haskell's Properties.md`, retag `attr/concept`→`attr/links` (still a stub — stays in mailbox). Update inbound `[[View of Haskell's Properties]]` in: `archives/Programming Language Haskell.md:18`, `library/Tree Mental Models.md:25`, `library/L_fold/Learning Haskell.md:13`.
3. Delete now-empty dirs `mailbox/Map/`, `mailbox/View/`.
4. **`library/L_fold/Life todo.md`** → `a_sticker/todos/Life todo.md` (todos live with todos; inbound `[[Life todo]]` in `a_sticker/todos/Index of Todos.md:19` still resolves by name).
5. **`archives/algorithms/todo interval.md`** → `a_sticker/todos/todo interval.md` (same reason; no inbound links).
6. **Delete `library/H_fold/How to tech Backend.md`**: verified byte-duplicate of `archives/engineering/How to tech Backend.md` (only diff: `[[Class]]` vs `[[library/Class]]` path spelling — both resolve to the same name — plus trailing newline). Both are `type/lit`; keep the archives copy. No inbound links to either.
7. **Delete `a_sticker/or/Ebola virus' right.md`** (0 bytes, empty).

## Step 6 — Typo renames + tricks prefix normalization (with link updates)

Re-grep each old name before renaming; update every `[[OLD...` hit.

| Old path | New path | Verified inbound links |
|---|---|---|
| `library/L_fold/Linear Agebra.md` | `Linear Algebra.md` | `library/C_fold/CDM.md:27`, `library/I_fold/Image of Homomorphism.md:18`, `library/K_fold/Kernel of Homomorphism.md:14`, `library/Index/Index of Abstract Algebra.md:87` |
| `library/L_fold/Lagecy View of Algorithm.md` | `Legacy View of Algorithm.md` | `a_sticker/todos/translate todo.md:21`, `library/A_fold/Algorithm tips.md:12`, `library/Index/Index of Algorithm.md:13` |
| `library/M_fold/Mutiplicative function.md` | `Multiplicative function.md` | `library/E_fold/Euler's totient function.md:38`, `library/Index/Index of Abstract Algebra.md:98` |
| `library/G_fold/Grammer.md` | `Grammar.md` | `library/D_fold/Declension.md:11` (`[[Grammer\|Grammatical]]` → `[[Grammar\|Grammatical]]`) |
| `archives/Surplus Sociaty.md` | `Surplus Society.md` | none |
| `library/Sequential List v.s. Linked List.md` | `Sequential List vs. Linked List.md` | `library/Links/Links of How to Choose the Implementation of Linear List.md:11`; also fix double space in its body header `Sequential  v.s. Linked` → `Sequential vs. Linked` |
| `archives/Project v.s. Protrude v.s. Stand out.md` | `Project vs. Protrude vs. Stand out.md` | none |

**archives/tricks/ prefix normalization** (verified: no inbound links to any of these): rename each file whose name starts with `Tip`/`Tips`/`tirck`/`trick` (any case/separator) to `Trick <rest>`:
- `Tip-Install Windows via Libvirt.md` → `Trick Install Windows via Libvirt.md`
- `Tip Can not Find ISO of Windows 11.md` → `Trick Can not Find ISO of Windows 11.md`
- `Tip fix can not open virt-manager.md` → `Trick fix can not open virt-manager.md`
- `Tip for applying a proxy to the Docker daemon.md` → `Trick for applying a proxy to the Docker daemon.md`
- `Tips-Windows ISO Fall back.md` → `Trick Windows ISO Fall back.md`
- `Tip windows can not find disk or NIC.md` → `Trick windows can not find disk or NIC.md`
- `tirck for install virtio nic driver.md` → `Trick for install virtio nic driver.md`
- `trick for installing all virtio driver.md` → `Trick for installing all virtio driver.md`
- `trick install Win Fsp.md` → `Trick install Win Fsp.md`
- `trick qemu.md` → `Trick qemu.md`
- `trick-mount-ntfs.md` → `Trick mount ntfs.md`
- `trick- rotate-before-login-with-sddm.md` → `Trick rotate-before-login-with-sddm.md`
(Already-conformant `Trick ...` files untouched.)

## Step 7 — Rewrite README.md

Full replacement. Content spec (keep the existing tone — short, rule-like, English):

1. **Title + intro**: knowledge base organized by state, not folder tree; modified Zettelkasten stressing atomic cards, linking, and original own-voice output.
2. **Core Zones**: `mailbox/`, `library/`, `archives/`, root = temporary landing area (kept small, drained) — as today.
3. **Support dirs** (new section):
   - `library/Index/` — cross-topic Index notes (`Index of ...`); topic-local maps may stay beside their topic in the letter folds.
   - `library/Links/` — Links notes (formerly "views"): one concept from multiple angles, isomorphisms, cross-topic connections.
   - `library/<A–Z>_fold/` — letter-sharded stable cards.
   - `zzz_output/` — finished personal outputs / own-voice synthesis pieces (the vault's showcase; `zzz_` keeps it last in the sidebar).
   - `a_sticker/` — scratch: `todos/` task lists, `or/` AI-conversation captures, `new_terms/` vocab staging.
   - `template/` — card scaffolds (`concept/method/principle/technique/map/links/lit-temp.md`).
4. **Index vs Links doctrine** (replaces Map vs View): Index = big-topic architecture & navigation ("where things live"); Links = single-concept multi-angle interpretation ("how to understand"); Index solves navigation, Links solves interpretation. Map==Index — one word: Index.
5. **Where a note belongs / promotion rule** — keep current sections, s/view/Links/g, s/map note/Index note/g; map naming guidance: `Index of ...`.
6. **Recommended Tags**: `type/permanent`, `type/lit`; `status/in-progress|evergreen|archive`; `attr/map`, `attr/links`, `attr/principle`, `attr/concept`, `attr/technique`, `attr/method`; lit notes MUST carry a real `source:`.
7. **How to Use the Vault** — unchanged 5 steps.
8. **Related Files** (all links verified after restructure):
   - `[Knowledge Base Operating Rules](library/K_fold/Knowledge%20Base%20Operating%20Rules.md)`
   - `[Links of General Coding Thoughts](library/Links/Links%20of%20General%20Coding%20Thoughts.md)`
   - `[Index of Knowledge](library/Index/Index%20of%20Knowledge.md)`
   - Remove the phantom `Library Consolidation Work Log` link and the deleted `AGENTS.md` link.

## Step 8 — Update `library/K_fold/Knowledge Base Operating Rules.md`

Its "Map vs View" / "Where to Store Map and View" sections teach the old doctrine. Replace with Index-vs-Links doctrine matching README Step 7.4 (Index=big-topic navigation, `Index of ...`, cross-topic in `library/Index/`, topic-local beside topic; Links=single-concept multi-angle, in `library/Links/` when stable, mailbox while shaping). Keep the Definition / Core Split / When to Write a Card / How to Structure a Card / How to Promote / How to Use sections (s/map note/Index note/, s/view note/Links note/). Its `[[View of General Coding Thoughts]]`-style related links, if any, follow the renames.

## Step 9 — Verification

From vault root:

1. **Wikilink integrity** (end-to-end, the load-bearing check — every rename/move must resolve):
```bash
cd /home/mia/Documents/obsidian/krummholz-buecherstube
grep -rhoE '\[\[[^]|#]+' --include='*.md' . | sed 's/^\[\[//' | sort -u > /tmp/targets.txt
find . -name '*.md' -not -path './.git/*' -printf '%f\n' | sed 's/\.md$//' | sort -u > /tmp/names.txt
comm -23 /tmp/targets.txt /tmp/names.txt
```
Expected unresolved (pre-existing intentional placeholders — whitelist): `Functional`, `Pure`, `Statically typed`, `Partial Sum Sequence`, `Inequality`, `Consolidation`, `mailbox/trivial-analysis/Rational Function that is 1 to 1`, `mailbox/algo/Pre-condition Check`, `mailbox/trivial-data-structure/Map of Concepts of Data`, `mailbox/trivial-trigonometry/Trigonometric Functions`, `mailbox/trivial-trigonometry/Trigonometric Substitution`, `mailbox/trivial-physics/Acceleration`, `library/trivial-physics/Instantaneous Velocity`, `mailbox/algo/Alignment between Ordered Data Beats Mapping`, `mailbox/algo/Bucketing Chars`, `library/Class`, `Subset Traversal` (unresolved pre-cleanup). Fix any NEW unresolved link created by the renames by updating the referencing file. Optionally normalize the stale path-style links (`[[mailbox/trivial-.../X]]` → `[[X]]`) in `a_sticker/todos/translate todo.md:20-23`, `library/I_fold/Instinct of Special Functions.md:20`, `library/T_fold/Tangential Velocity.md:10`, `library/Index/Index of Structural Exploitation.md:33` — targets exist under short names.
2. **Zero-hit greps** (expect no output each):
```bash
grep -rn 'attr/views' --include='*.md' .
grep -rn '卡片盒笔记法.*Ahrens' --include='*.md' .    # template/lit-temp.md now has empty source
grep -rn 'trivial-thoughts' --include='*.md' .
grep -rn '_index_' --include='*.md' .
grep -rnE '\[\[(View of|Views of|Map of|Raw Map)' --include='*.md' .
grep -rn 'Addtive\|Indentity\|Lagecy\|Agebra\|Mutiplicative\|Grammer\|Fuctional\|Sociaty\|tirck' --include='*.md' .   # alias/display-text fixes from Step 3.7 may remain in display text only — file names must be clean
ls library/_index_ mailbox/Map mailbox/View 2>&1   # all three must be "No such file or directory"
```
3. **Root drained**: `ls *.md` in vault root returns only `README.md`.
4. **Git review**: `git status --short` — expect deletions (AGENTS.md, 人生规划2.md, How to tech Backend.md in H_fold, Ebola file), renames and modifications matching this plan, nothing else. Do NOT commit.

## Critical files & anchors

- `library/_index_/` — the entire 78-file hub being split into `Index/` + `Links/` (Step 2 disposition is exhaustive)
- `library/A_fold/Alignment between Ordered Data Beats Mapping.md:7-12` — conflict markers to strip (Step 1)
- `template/lit-temp.md:6` — hardcoded source line, root cause of the 172-file leak (Step 3.3)
- `README.md:106-111` — Related Files section, 4 broken links; whole file rewritten (Step 7)
- `library/K_fold/Knowledge Base Operating Rules.md` — doctrine source of truth, updated (Step 8)

## Assumptions & contingencies

- `library/Index/` + `library/Links/` (not vault-root `./Index ./Links`): the root must stay a drainable landing zone and the README already places cross-topic hubs in `library/`; owner said "make your own choice basing on my guideline".
- Links naming is mechanical `Links of <old View payload>`; Index naming consolidates `Map of`→`Index of` so one concept has one word (owner: "Map==Index… is confusing me now").
- Topic-local `attr/map`/`attr/links` notes in letter folds stay put (README: topic-local maps live beside their topic); only the hub `_index_` is restructured.
- Dangling-but-intentional wikilinks (`[[Functional]]`, `[[Pure]]`, `[[Consolidation]]`, etc.) are left as Obsidian unresolved placeholders — vault philosophy uses them as new-note hooks.
- `zzz_output/` contents untouched (owner-valued showcase).
- If a re-grep at execution finds inbound links to any renamed file beyond the listed ones, update those too (same `[[OLD`→`[[NEW` rule) — never leave a renamed note unlinked.
- If the 看过的番剧 frontmatter proves to have more corruption than line 6, delete only the corrupted source line and leave the rest untouched.
- No commits, no pushes; owner reviews `git status` themselves.
