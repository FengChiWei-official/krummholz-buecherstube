# Knowledge Base

Modified Zettelkasten，按**状态**组织，不按主题树。两棵树 + 原子卡 + 明确链接 + 自己的声音。
> 核心两条：写下自己的一个点，当场把它连进旧网（写一句 why）。其余全是机器的事。
> 验收标准：检索时能否回报惊奇。

## 最小记忆集（3 条，其余不用记）

1. 写笔记 = 纯 markdown（工具不依赖模板，`template/` 是可选脚手架），无 frontmatter 字段（除 `aliases`/`source`）。捕获时当场链 ≥1 篇旧笔记：`python3 tools/vault.py suggest "旧笔记名"` 给 3 个候选 + why，选一个即可。
2. 未完成的活挂 todo（`a_sticker/todos/`）；中断快存 = 原地不动 + 挂钩 + 续写说明（5–10 词）。
3. 不知道干什么 = `python3 tools/vault.py status`（节律行 + 编号选项，每条都带可复制命令）。

> 其余 ~84 条规则由工具与 [[Agent Contract]] 承载，不需要记忆：`vault.py help <topic>` 就地查（check / status / triage / rawindex / dag / links / random / suggest / docs-check）。

## 两棵树

- **主干 `library/Raw/`** — `Raw Index*`。完整、**≥1 条登记边**、登记（"你在这儿"）。防 node 失散。登记是边不是父：一个 Node 可被多个 Raw Index 登记，唯一性在边（DAG）；`Raw Index → Raw Index` 不许成环。粗粒度：一个粗 Raw Index 含几个簇，AI 归组维持。根 = `Raw Index of Everything`。
- **语义树 `library/Index/`** — `Index of*`。涌现的（聚簇输出，不是脚手架）、多重归属、区域。跨领域卡的第二归属由它承载。

边语义：**登记边（Raw → Node）是结构动作，AI 可直接追加；Node↔Node 与 Index→Node 改变意义，须你批准。**

## 区域

- `library/<A–Z>_fold/` — Node（默认体裁，按首字母分片；数字头与 CJK 各有自己的 fold，名字见 `tools/vault.toml [zones]`）。
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
- `python3 tools/vault.py rawindex [--clusters|--check|--sync [--apply]]` — 主干作业：归队提议 L0 / 簇 L1–L3（含绑定证据）/ 规则注册表 / 同步主干根成员（默认 dry-run）。
- `python3 tools/vault.py place NAME` — **一篇笔记在图里的位置**（只读）：登记边、归队提议（邻居投票 + 谁投的）、语义区域、出入链、先链哪几篇（含 why）、I1a/I3/I1c/D21 信号。别名可查；查不到 exit 1 + did-you-mean。
- `python3 tools/vault.py links-candidates TOPIC [--n 12]` — **建 Links 卡的成员候选**（只读）：名字/别名命中作种子，按 Index 区域分组成员，每人带证据（名字含 / 链到种子 / 同登记 / 同区域 / 共同邻居）。跨 <2 区域会明确说「还不算 Links 卡」；结构笔记（Raw/Index/Links/doctrine）作为中介被排除。
- `python3 tools/vault.py index-candidates RAW_INDEX [--n 8]` — **建 Index 的候选卡表**（只读）：把该 Raw Index 的成员按共同邻居（θ 同主干）成簇，输出 `| 簇 | 成员 | 共同证据 | 共性句候选（草稿） | 建议 Index 名 |`。成员里的 Links 卡会标注为天然种子；只有一个簇会明说「撑不起 Index」（D10-P3）。
- `python3 tools/vault.py retrieve TERM [--n 15]` — **整库检索**（只读）：按证据强度排序（名字 4 / 别名 3 / 登记于或区域名命中或正文命中 2 / 共同邻居 1），每条命中带理由、登记者、区域、角色，正文命中还带行号与原文。范围 = 载入的笔记（`zzz_output/`、`template/` 不参与，同 G3）。有命中 exit 0，无命中 exit 1。
- `python3 tools/vault.py rename OLD NEW [--apply]` — 改名 + 级联：把全库指向 `OLD` 的 wikilink 一次改完（`|alias` 与 `#标题` 原样保留，只改名字那一段）。同名冲突 / 路径分隔符 / root 契约文件 / `zzz_output/` 里的文件都会**拒绝**（exit 1）。默认 dry-run。
- `python3 tools/vault.py new NAME [--zone Z] [--source S] [--todo NOTE --into TODO_NOTE] [--apply]` — 按模板新建：分区由**状态**定（root 入口队列 / library / material / work / todos），体裁由**名字**定，脚手架从 `tools/vault.toml [templates]` 按体裁取（可选，D30）。`material` 缺 `source:` 会拒绝（G2 硬门）；落地后给 3 个候选链接（S2）。默认 dry-run。
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
