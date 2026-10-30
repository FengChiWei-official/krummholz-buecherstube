# Knowledge Base

Modified Zettelkasten，按**状态**组织，不按主题树。两棵树 + 原子卡 + 明确链接 + 自己的声音。
> 核心两条：写下自己的一个点，当场把它连进旧网（写一句 why）。其余全是机器的事。
> 验收标准：检索时能否回报惊奇。

## 最小记忆集（3 条，其余不用记）

1. 写笔记 = 纯 markdown（工具不依赖模板，`template/` 是可选脚手架），无 frontmatter 字段（除 `aliases`/`source`）。捕获时当场链 ≥1 篇旧笔记：`python3 tools/vault.py suggest "旧笔记名"` 给 3 个候选 + why，选一个即可。
2. 未完成的活挂 todo（`a_sticker/todos/`）；中断快存 = 原地不动 + 挂钩 + 续写说明（5–10 词）。
3. 不知道干什么 = `python3 tools/vault.py status`（节律行 + 编号选项，每条都带可复制命令）。

> 其余 ~84 条规则由工具与 [[Agent Contract]] 承载，不需要记忆：`vault.py help <topic>` 就地查（triage / rawindex / dag / links / random / suggest）。

## 两棵树

- **主干 `library/Raw/`** — `Raw Index*`。完整、**≥1 条登记边**、登记（"你在这儿"）。防 node 失散。登记是边不是父：一个 Node 可被多个 Raw Index 登记，唯一性在边（DAG）；`Raw Index → Raw Index` 不许成环。粗粒度：一个粗 Raw Index 含几个簇，AI 归组维持。根 = `Raw Index of Everything`。
- **语义树 `library/Index/`** — `Index of*`。涌现的（聚簇输出，不是脚手架）、多重归属、区域。跨领域卡的第二归属由它承载。

边语义：**登记边（Raw → Node）是结构动作，AI 可直接追加；Node↔Node 与 Index→Node 改变意义，须你批准。**

## 区域

- `library/<A–Z>_fold/` — Node（默认体裁，按首字母分片；数字头 `0_fold`，CJK `中_fold`）。
- `library/Links/` — `Links of*`：单概念多角度，横跨 ≥2 个 Index 区域。理解的产物。
- `archives/material/` — 外部材料。`source:` 必填（硬门）。拆过判据 = 有指向所拆 Node 的出链。
- `archives/work/` — 我的档案：AI 报告、调研、决策材料。
- `a_sticker/` — `todos/`（唯一状态存储 + 任务树，`Index of Todos.md` 登记）、`or/`（AI 对话捕获）、`new_terms/`、`other/`。
- `zzz_output/` — 终端产出（**人的专属**：手动创建即产出）。`Root.md` = 主树入口。
- `doctrine/` — 系统文档：[[Vault Design]]、[[Vault Workflow]]、[[Agent Contract]]、[[Vault Extension]]（维护者手册 + 文档同步面）、[[New Machine]]（新设备复现）。

Root = 入口队列（Obsidian 默认落点）：新捕获落在那里，triage 排空。永久 root 文件只有 `README.md` / `AGENTS.md`。

## 工具

所有子命令都接受 `--json`（机器可读）与 `--strict`（缺配置文件即 exit 2）；`help <topic>` 给就地说明。

- `python3 tools/vault.py status` — 会话入口：git + 检查摘要 + 整理债 + **节律行（上次整理/聚簇/问箱/产出）** + 编号选项（每条带可复制命令）。任何会话先跑它。
- `python3 tools/vault.py check` — 两级判据：**硬门 G1/G2/G3**（root 排空 / material 出处 / 新增悬空 wikilink）exit 1 阻断；**报告级**（I1a 未登记 / I1b 重复登记边 / I1c Raw Index 环 / I2 Links 跨域 / I3 出链 / I4 绑定邻居 / I5 Mapping / I6 实例化 / I7 时间轴 / I8 挂点覆盖率 / I9 未记录 source / D21 未拆材料）给增量。提交前跑。
- `python3 tools/vault.py docs-check [--against REV] [--gate]` — 文档同步面：按 `tools/vault.toml [docs_sync]`（＝ [[Vault Extension]] §同步面）diff 工作区，报出「碰了触发文件却没连带改」的连带文件。默认报告级，`--gate` exit 1。
- `python3 tools/vault.py triage` — 整理债：root 积压、todo 老化、疑似半成品（时间窗 + 零出链 + 零挂钩）、unhooked、体裁错位、dead todo——每个阈值只定义在 `tools/vault.toml`。
- `python3 tools/vault.py rawindex [--clusters|--check|--sync [--apply]|--around NAME]` — 主干作业：归队提议 L0 / 簇 L1–L3（含绑定证据）/ 规则注册表 / 同步主干根成员（默认 dry-run）/ 单点邻域。
- `python3 tools/vault.py random [--scope …] [--seed N]` / `suggest NAME [--n 3]` — 问箱材料（S9）与候选链接（S2），只给信号不写笔记。
- `python3 tools/trend_radar.py` — 每日情报（详见 `.agent/skills/trend-radar/`）。

阈值与路径的唯一定义处是 `tools/vault.toml`（改一处即全局生效）。

## 协作

场景协议（S1–S10）与 AI 边界见 [[Vault Workflow]]；AI 接手契约见 [[Agent Contract]]；系统原理见 [[Vault Design]]。维护者手册（怎么改系统、改一处要同步哪几处）见 [[Vault Extension]]；新设备复现见 [[New Machine]]。

## Related Files

- [Vault Design](doctrine/Vault%20Design.md)
- [Vault Workflow](doctrine/Vault%20Workflow.md)
- [Agent Contract](doctrine/Agent%20Contract.md)
- [Vault Extension](doctrine/Vault%20Extension.md)
- [New Machine](doctrine/New%20Machine.md)
- [Index of Todos](a_sticker/todos/Index%20of%20Todos.md)
- [Index of Knowledge](library/Index/Index%20of%20Knowledge.md)
