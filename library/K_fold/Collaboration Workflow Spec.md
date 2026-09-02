---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/map
---

## Definition

**AI 是磨刀石,不是代笔。** AI sharpens — questions, structure, links, checks — the human writes in their own words. AI-assisted prose belongs in `a_sticker/or/` as raw material, never directly in `library/` as personal voice.

三层分工 (three layers):

- **人 (human)** = content. Own voice, own words. Nothing here substitutes for that.
- **Obsidian** = medium. Backlinks, unresolved-link pane, tag search — the association engine.
- **omp (AI)** = structure & discipline. Questions, skeletons, checks, link discovery, filing mechanics. Never the voice.

## S1 新想法打磨 (New idea → sharpened plan)

Trigger: 有新想法,想让 AI 先打磨再动笔。

Flow:

1. Owner tells omp the idea in one or two sentences.
2. omp asks 3–5 sharpening questions (核心概念是什么?边界在哪?碰到哪些已有笔记?) and runs `grep`/tag-search to list 3–5 potentially related existing notes.
3. omp proposes: note type (concept/links/technique), suggested filename, target zone, which index/Links note it should link into, and a skeleton of section headings only.
4. **Owner writes the body themselves in Obsidian, in their own words** — omp outputs at most skeleton headings, never body prose.
5. File lands in root/mailbox per normal capture; link to the notes from step 2 immediately.
6. If deferred, todo-hook.

AI boundary: skeleton + questions only. Owner-pasted AI-generated prose goes to `a_sticker/or/` as lit-ish raw material, to digest and rewrite later.

## S2 写完检查 (Post-writing review)

Trigger: 写完一篇,想让 AI 检查维护。

Flow:

1. Owner: "check X" (or omp runs after any writing session).
2. omp runs `python3 tools/vault.py check`.
3. omp reads the note and reports: tag correctness (closed set; is `attr/*` right for the content?), missing `source:` if lit, frontmatter shape vs the `template/` counterpart.
4. **Link discovery**: omp greps title-adjacent terms vault-wide and proposes 3–8 concrete new links with file:line — owner approves, omp inserts. Links change meaning, human approves; structure fixes omp applies directly.
5. omp moves the note root→mailbox if still in root (mechanical, allowed).
6. If `status/evergreen` and in mailbox → suggest `promote --dry-run`.

## S3 体系化知识摄入 (Systematic knowledge ingestion)

Trigger: 开始/继续一个课程式主题 (OS, Calculus, a book)。

Flow:

1. If new topic: omp creates `library/Index/Index of <Topic>.md` from `template/map-temp.md` + `Raw Index of <Topic>` stubs.
2. Owner studies and writes atomic cards per concept (own voice) into mailbox/root as usual.
3. Per-session: omp runs triage on the topic's new notes, files them to letter folds, links each into the Index note's Core Concepts.
4. **Cross-topic rule**: each promoted systematic note must gain ≥1 link outside its own topic — omp proposes candidates by tag/grep, owner approves.
5. Long-tail: unfinished syllabus items live as a checklist in `a_sticker/todos/<Topic> Todo.md` (template `Todo Template.md`), registered in `Index of Todos.md`.

When NOT to index: one-off course notes with no reuse intent stay as ordinary concept cards — no scaffolding.

## S4 Output 时点 (When to write into zzz_output/)

Trigger: 感觉一个主题集群成熟,想做自己的综合输出。

Criteria (all three, defaults not gates):

1. The topic's index/Links notes are `status/evergreen`.
2. ≥5 stable notes in the cluster.
3. Owner can state the thesis in one sentence without rereading. If not, the cluster isn't ripe — the failure mode is writing output to *understand*, which produces re-digested textbooks instead of own voice.
Output mount: back-link the new output from `Raw Index of Root` (or the closest topic `Index of`) so the main tree reaches it; outputs are the terminal state of the S3→S4 pipeline.

Flow:

1. omp assembles the cluster (index + backlinks) as a reading list.
2. **Owner writes the output themselves** — `zzz_output/` is by definition own-voice terminal output (the proof of having learned); AI never drafts it.
3. omp checks links resolve, adds the output backlink into the topic's Index note.
4. Tag `status/evergreen`. If the output introduces new synthesis worth keeping as cards, extract those as new library notes (AI suggests extraction points, owner writes them).

## S5 Todo 管理 (fast save, commit, hook without future-debt)

Trigger: 会话被打断 / 快速保存,不丢线索。

Flow:

1. Quick-save = just leave the note where it is (root ok — it's the entry queue).
2. omp inserts `- [ ] [[NAME]]` + a 5–10 word continuation note (e.g. `- [ ] [[NAME]] — 补完和 X 的对比`) into the owning topic todo; no owning todo → the inbox section of `a_sticker/todos/Index of Todos.md`, or a new topic todo per S3.
3. Commit message pattern `wip: NAME — what remains` (owner or omp writes it; omp may commit only when owner asks).
4. Future resume = open the todo; the `[[NAME]]` backlink + continuation note gives the exact re-entry point. No archaeology.

Rule: **a todo entry without a continuation note is forbidden** — the continuation note is what makes the future solvable (无从下手 prevention).

## S6 Tag 维护时点 (When to update tags)

Tags are not maintained continuously — three moments only:

1. At promotion (`promote` validates vocabulary).
2. At S2 review (omp checks attr correctness).
3. Tag taxonomy changes (rare, like the views→links migration): omp runs a vault-wide grep-rewrite as a planned change (exhaustive rename plan, link updates, verification), never ad hoc.


## S7 入口状态机 (Session-entry state machine)

Trigger: owner opens a session unsure what to do ("我有一个新东西" / "现在能干什么" / "上次没整理").

Flow:

1. omp runs `python3 tools/vault.py status` — repo state, not memory, is the source.
2. omp reports state plainly (dirty tree, root strays, stalled promotions, idle notes, unpublished outputs).
3. omp presents the status next-moves as numbered options, each with a one-line plan (e.g. "① 先整理:运行 triage 归档 N 篇 root 笔记,再提交;② 新想法可在主树 X 分支挂载,相关笔记:A、B、C").
4. Owner picks; omp executes per the matching scenario S1–S6.

AI boundary: options and plans only — state and actions are facts from tools; omp never invents state.


## Quick Cards

### 卡片 S1 — 打磨

1. Owner: 一两句话说出想法。
2. omp: 问 3–5 个打磨问题,列出 3–5 篇相关笔记。
3. omp: 给出类型/文件名/目标区/index 归属 + 只有标题的 skeleton。
4. Owner: 自己在 Obsidian 写正文。
5. 落地 root/mailbox,立即链接 step-2 笔记。
6. 延后 → 挂 todo。

### 卡片 S2 — 写完检查

1. Owner: "check X"。
2. omp: run `python3 tools/vault.py check`。
3. omp: 报告 tag/source/frontmatter 问题。
4. omp: 提出 3–8 个新链接 (file:line)。
5. Owner 批准 → omp 插入;结构问题 omp 直接修。
6. evergreen 在 mailbox → suggest `promote --dry-run`。

### 卡片 S3 — 体系化摄入

1. 新主题 → omp 建 `Index of <Topic>` + Raw Index stubs。
2. Owner: 逐概念写原子卡 (own voice)。
3. 每会话: omp triage → 归档到 letter folds → 挂进 Index。
4. omp 提议 ≥1 cross-topic 链接,owner 批准。
5. 未完成条目 → `<Topic> Todo.md`,注册进 `Index of Todos.md`。
6. 一次性课程笔记,无复用意图 → 不建 index。

### 卡片 S4 — Output

1. 查三条默认标准: index evergreen / ≥5 篇 / 一句话能说清 thesis。
2. omp: 组装 reading list (index + backlinks)。
3. Owner: 自己写 output (`zzz_output/`)。
4. omp: 验证链接,把 output 反向挂进 Index。
5. 反向挂载:把 output 挂进 `Raw Index of Root` 或最近的 topic Index(主树可达)。
6. 打 `status/evergreen`。
7. 新综合点 → AI 建议 extraction points,owner 写成新卡。

### 卡片 S5 — 快存挂 todo

1. 笔记原地不动 (root ok)。
2. omp: 在所属 topic todo 插入 `- [ ] [[NAME]] — 续写说明 (5–10 词)`。
3. 无所属 todo → `Index of Todos.md` inbox 或按 S3 新建。
4. Commit: `wip: NAME — what remains` (omp 仅在 owner 要求时提交)。
5. 恢复: 打开 todo,backlink + 续写说明即重入点。

### 卡片 S6 — Tag 维护

1. Promotion 时: `promote` 校验词汇表。
2. S2 review 时: omp 查 attr 正确性。
3. 分类变化时: omp 做计划性 grep-rewrite (改计划→改链接→验证),绝不 ad hoc。
4. Obsidian 内交互改名用 tag-wrangler 插件。
5. 批量真相以 `python3 tools/vault.py check` 为准。

### 卡片 S7 — 入口

1. omp: run `python3 tools/vault.py status`。
2. omp: 报告仓库状态(脏树/root 积压/待 promote/闲置笔记/未发布 output)。
3. omp: 给出编号选项+每项一句计划。
4. Owner 选择 → 按 S1–S6 执行。
5. 状态以工具输出为准,不凭记忆。

---
## **Related**

- [[Vault System Design]]
- [[Knowledge Base Operating Rules]]
- [[Index of Todos]]
