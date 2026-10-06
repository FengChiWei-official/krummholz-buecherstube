# Knowledge Base

Modified Zettelkasten，按**状态**组织，不按主题树。两棵树 + 原子卡 + 明确链接 + 自己的声音。
> 核心两条：写下自己的一个点，当场把它连进旧网（写一句 why）。其余全是机器的事。
> 验收标准：检索时能否回报惊奇。

## 最小记忆集（3 条，其余不用记）

1. 写笔记 = 纯 markdown，无模板无 frontmatter。捕获时当场链 ≥1 篇旧笔记（AI 会给 3 个候选，选一个即可）。
2. 未完成的活挂 todo（`a_sticker/todos/`）；中断快存 = 原地不动 + 挂钩 + 续写说明（5–10 词）。
3. 不知道干什么 = `python3 tools/vault.py status`（节律行 + 编号选项）。

## 两棵树

- **主干 `library/Raw/`** — `Raw Index*`。完整、唯一归属、登记（"你在这儿"）。防 node 失散。粗粒度：一个粗 Raw Index 含几个簇，AI 归组维持。根 = `Raw Index of Everything`。
- **语义树 `library/Index/`** — `Index of*`。涌现的（聚簇输出，不是脚手架）、多重归属、区域。跨领域卡的第二归属由它承载。

边语义：**登记边（Raw → Node）是结构动作，AI 可直接追加；Node↔Node 与 Index→Node 改变意义，须你批准。**

## 区域

- `library/<A–Z>_fold/` — Node（默认体裁，按首字母分片；数字头 `0_fold`，CJK `中_fold`）。
- `library/Links/` — `Links of*`：单概念多角度，横跨 ≥2 个 Index 区域。理解的产物。
- `archives/material/` — 外部材料。`source:` 必填（硬门）。拆过判据 = 有指向所拆 Node 的出链。
- `archives/work/` — 我的档案：AI 报告、调研、决策材料。
- `a_sticker/` — `todos/`（唯一状态存储 + 任务树，`Index of Todos.md` 登记）、`or/`（AI 对话捕获）、`new_terms/`、`other/`。
- `zzz_output/` — 终端产出（**人的专属**：手动创建即产出）。`Root.md` = 主树入口。
- `doctrine/` — 系统文档：[[Vault Design]]、[[Vault Workflow]]。

Root = 入口队列（Obsidian 默认落点）：新捕获落在那里，triage 排空。永久 root 文件只有 `README.md` / `AGENTS.md`。

## 工具

- `python3 tools/vault.py status` — 会话入口：git + 检查摘要 + 整理债 + **节律行（上次整理/聚簇/问箱/产出）** + 编号选项。任何会话先跑它。
- `python3 tools/vault.py check` — 两级判据：**硬门**（root 排空 / material 出处 / 新增悬空 wikilink）exit 1 阻断；**报告级 I1–I4**（唯一归属 / Links 跨域 / 出链 / 绑定邻居）给增量。提交前跑。
- `python3 tools/vault.py triage` — 整理债：root 积压、todo >90 天老化、疑似半成品（近 7 天 + 零出链 + 零挂钩）。
- `python3 tools/vault.py rawindex [--clusters|--check|--sync|--around NAME]` — 主干作业：归队提议 L0 / 簇 L1–L3（含绑定证据）/ I1–I3 / 同步主干根成员 / 单点邻域。
- `python3 tools/trend_radar.py` — 每日情报（详见 `.agent/skills/trend-radar/`）。

## 协作

场景协议（S1–S10）与 AI 边界见 [[Vault Workflow]]。系统原理见 [[Vault Design]]。

## Related Files

- [Vault Design](doctrine/Vault%20Design.md)
- [Vault Workflow](doctrine/Vault%20Workflow.md)
- [Index of Todos](a_sticker/todos/Index%20of%20Todos.md)
- [Index of Knowledge](library/Index/Index%20of%20Knowledge.md)
