# Vault Design

## Definition

这个 vault 的管理问题从来不是自律问题，是结构问题：物理布局是固定层级，而知识到达是联想的、无序的。解法不是更多自律，而是把「状态」从文件夹里拿出来，交给两个不同的承载者。

一句话：**人只写点和链；结构由两棵树承载，一棵防失散，一棵管理解；纪律由工具承载。**

三层分工：

- **人 = 内容**。自己的话，自己的思想。没有任何东西可以替代它。终端产出在 `zzz_output/`。
- **Obsidian = 媒介**。backlink、未解析链接面板、搜索——联想引擎。
- **omp (AI) = 结构与纪律**。检查、聚簇、登记、供材。永远不是声音。

## 两棵树

```
Raw Index  主干   完整 / ≥1 登记边 / 登记   → 防 node 失散（DAG）
Index      语义树 部分 / 多重归属 / 区域    → 入口与稳定
Links      语义边 横跨 ≥2 个 Index 区域     → 理解的产物
Node       点     默认体裁（<A–Z>_fold）
```

| | 边 | 含义 | 能否用于语义聚类 |
|---|---|---|---|
| 主干 | `Raw Index → Node` | **登记**（"你在这儿"）；登记边为结构动作，AI 可直接追加 | **不能** |
| 语义树 | `Index → Node` | **理解**（"这些是一回事"） | 能 |
| 节点间 | `Node ↔ Node` | 你的判断 | 能（主力） |

关键 doctrine：

- **粗主干**（D10-P3）：粗粒度由 AI 归组簇维持——**一个粗 Raw Index 包含几个簇**；细结构（簇 + 共性）进 Index。主干不随簇数膨胀。
- **登记 ≠ 分类**：Raw Index 说「它在这」，不说「它是什么」。归属是登记不是判决，可改可争议；跨领域卡的**第二归属由 Index 承载**。
- **登记是边，不是父**（v6）：主干是 DAG 不是树。每个 Node **至少一条**登记边；同一 `(Raw Index, Node)` 对不得重复；一个 Node **可以**被多个 Raw Index 登记（多重登记合法）——唯一性在边，不在父。Node 的完整性判据是「有登记边」，不是「只有一个父」（I1a / I1b）。
- **环不变量**：`Raw Index → Raw Index` 子图必须无环（I1c）。主干允许一个 Raw Index 指向另一个（粗主干挂细主干），但不允许互相指回去。
- **登记边规则**（D22）：Raw Index → Node 的登记边是结构动作，AI 可直接追加；`Node ↔ Node` 与 `Index → Node` 改变笔记意义，须 owner 批准。
- **出链 = 已拆**（D21）：材料被拆过的标记 = 它有指向所拆 Node 的出链；零出链材料 = 未拆。零新增状态字段。
- **结构涌现，不预设**：Index 是聚簇的输出，不是脚手架。先有簇（带共性），再有 Index。
- **人维护的会变之物才删；变化由 AI 承载的可以留**：状态字段人改 → 删；主干成员集虽每轮变但 AI 承载 → 留。

## 判据两级制（D20）

| 级别 | 判据 | 失败动作 |
|---|---|---|
| **硬门** | root 排空；`archives/material/` 每篇有 `source:`；wikilink 新增悬空 | exit code 1，阻断提交 |
| **报告级** | I1a 未登记 / I1b 重复登记边 / I1c Raw Index 环 / I2 Links 跨域（同区域 = 违规，无区域 = 提示）/ I3 Node ≥1 出链 / I4 doctrine 与 Raw 不做绑定邻居 | 每周增量数字，不阻断 |

理由（CRITIQUE A5）：上线即 674 未登记、392 零出链——全部做成硬门 = 门常红 = 门失效。旧体系死于红灯常态。报告级给增量，让改善可见而不是让检查失败。

## 区域

```
README.md / AGENTS.md    入口与硬规则
doctrine/                 本设计 + [[Vault Workflow]]
library/
  <A–Z>_fold/             Node（默认体裁）
  Links/                   Links
  Index/                   Index（语义树）
  Raw/                     Raw Index（主干，永久）
archives/
  material/                外部材料（source: 必填，硬门）
  work/                    我的档案（AI 报告、调研、决策材料）
a_sticker/                 todos / or / new_terms / other
zzz_output/                终端产出（主树入口 Root.md）
tools/                     脚本
```

体裁判据：**名字 > 路径 > tag**。`Raw Index*` → Raw/；`Index of*` → Index/；`Links of*` → Links/；`-MOC` 与 `Index of*` 同属 Index/；其余 → fold。名字与路径冲突 = 搬家，不是改判。`a_sticker/todos/Index of Todos.md` 是 todo 树的登记册，不套 library 体裁规则。

## 字段

删：`tags` / `created` / `data-date` / `date`（全部退役——状态单点在 todo 树，体裁由名字+路径承载）。
留：`aliases`（wikilink 解析依赖）、`source`（material 的硬门）。
Node = 纯 markdown。**工具不依赖模板；模板是可选脚手架**（`template/`，6 个模板保留原样，含 `aliases:`）。「无固定小节」只约束**笔记**：笔记不要求填满模板的小节，而不是禁止模板存在固定小节。

## 为什么这套不会重演旧死因

旧体系三大死因与本设计的对位：

| 旧死因 | 复发路径 | 堵法 |
|---|---|---|
| 门常红 → 门失效 | I1–I4 若做硬门 | 两级制：硬门只 3 条；I1–I4 给增量 |
| 状态漂移 | todo 树无 GC | triage 报 todo 老化；零出链信号加时间窗（时间窗 + 零挂钩 = 疑似半成品）——阈值单点在 `tools/vault.toml` |
| 周期流程停摆无告警 | 聚簇/问箱停了没人知道 | `status` 顶部节律行：上次整理/聚簇/问箱/产出 距今 N 天（git log + mtime 推导，零手工记录） |

## 决策台账

形制沿用 v5（`archives/work/PLAN.md` §0）：一条决策一行，含编号、议题、裁决、落地含义。v5 用到 D22，v6 从 D30 起。

| # | 议题 | 裁决（owner，2026-10-30） | 落地含义 |
|---|---|---|---|
| D30 | 模板 | **保留**，模板保留 `aliases:` | 模板文件不动；doctrine 措辞改为「工具不依赖模板；模板是可选脚手架」；「无固定小节」收窄为只约束笔记；清 12 处残留提示行 |
| D31 | `Raw Index of Root` | **留着** | 新建 `library/Raw/Raw Index of Root.md` 并登记 topic indexes；`zzz_output/Root.md` 的链随即成立 |
| D32 | 49 篇无 `source:` 材料 | **补默认 source** | 默认值须诚实（`source: 未记录（2026-10-30 补齐）`）；同时新增报告级计数器 I9；baseline 豁免表整体可弃 |
| D33 | `a_sticker/other/` 四份提案 | **保留，逐份标注已过时部分** | 不删除；用显式区块标注哪些段落已被 v5 / v6 取代 |
| D34 | 类型化边 | **不要** | 维持 v5 D1；「约定小节」方案成为正式路线 |
| D35 | 记忆底座（间隔重复） | **做** | 只喂规则卡 + 核心概念卡；Obsidian 间隔重复插件，per-machine（`.obsidian/` 已 gitignore）；deck 须切按文件夹模式，否则与「无 tag」冲突 |
| D36 | 原始清单 `TR-raw-D-*.md` | **不再保存** | 候选池只活在当日 `/tmp` 快照；滚动 raw 合并删除；索引不再挂 raw 链 |
| D37 | 主干模型 | **树 → DAG** | 登记是边不是父：≥1 条登记边，同一 `(Raw Index, Node)` 对不得重复，多重登记合法，`Raw Index → Raw Index` 必须无环（I1a/I1b/I1c） |

## Related

- [[Vault Workflow]]
- [[Agent Contract]]
- [[Index of Todos]]
