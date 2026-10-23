# 执行方案 v5

> v4 验证了「迁移可执行」，未回答「住得下去吗」；v5 并入 CRITIQUE.md 的 14 条审查结论（已裁决修法一次到位）。
> 标注 `[已实测]` / `[已设计未测]` / `[待批]`；数字口径 `[复验 2026-10-06]`。

---

## 0. 决策台账（对话中定下的每一条，这是方案的根）

| # | 决策 | 你的原话 / 依据 |
|---|---|---|
| D1 | **去掉类型化边** `goal::` / `object::` / `bridge::` | "本身很难维护" |
| D2 | **去掉成熟度** `status/*` | "本身很难维护" |
| D3 | **状态只存一处 = todo 树**；`mailbox/` 退役 | D2 的推论：三份状态必然漂移 |
| D4 | **`concept` → `node`**；`principle`/`technique`/`method` **砍掉** | "太模糊了，没有办法明确区分，很难实践" |
| D5 | **Links = 点之间的非主要联系 / 跨界联系**；**"links 是理解的产物"** | 你的定义 |
| D6 | **Index = 区域，Links = 跨区域的边（≥2 个 Index 区域）** | D5 的可检查化 |
| D7 | **模板归零** | "最好不要依赖模板" |
| D8 | **Raw Index = 主干**：一直存在，人创建、AI/人共管，**防止 node 失散** | 你的方案 |
| D9 | **Index = 涌现出来的、真正语义化的平行树** | 你的话 |
| D10 | 主干三条性质：**登记≠分类** / **唯一归属** / **粗粒度由 AI 归组簇维持：一个粗 Raw Index 包含几个簇** | 为保证主干是"主干"；CRITIQUE A2 裁决 |
| D20 | **不变量两级制**：硬门（root 排空 / material 出处 / 新悬空 wikilink）可阻断，I1–I4 报告级给增量 | CRITIQUE A5 裁决 |
| D21 | **出链 = 已拆**：材料被拆过 = 它有指向所拆 Node 的出链 | CRITIQUE B2 裁决 |
| D22 | **登记边（Raw Index → Node）是结构动作，AI 可直接追加；Node↔Node 与 Index→Node 仍须 owner 批准** | CRITIQUE A7 裁决 |
| D11 | **`K_fold` 回归单一用途**，系统文档移到别处 | "k_fold 要回复单一用途" |
| D12 | **`doctrine/` 顶层**；系统文档合并为两份 | D11 的落点 |
| D13 | **doctrine 参与链接图，但不做枢纽** | "参与" |
| D14 | `rawindex` 命令：L0 归队 / L1 粗簇 / L2 细分 / L3 孤点 + **绑定证据** | 讨论中成型 |
| D15 | **L0 不能自举 → 顺序必须是「先聚类，后登记」** | `[已实测]` 82% 无锚点 |
| D16 | 每簇**必须有一句你写的共性**，否则不进 Index | 研究笔记 §三.3：没有共性陈述的聚类是目录 |
| D17 | **输出回路仍未解决** | "我现在没有办法有效输出" |
| D18 | `archives/` 拆 `material/` + `work/` | 你的"外部 vs 我的"之分 |
| D19 | `a_sticker/other/` 的提案按批准/否决分流 | F5 |

---

## 1. 理念（7 条）

1. **人只做两件事**：写下自己的一个点，和把它连进旧网（写一句 why）。
2. **状态只存一处**——只在 todo 树。
3. **人维护的会变之物才删；变化由 AI 承载的可以留**（复杂度守恒的推论）：`status/*` 每次推进人改 → 删；`topic/*` 常量 → 删；主干成员集虽变但 AI 承载 → 留。
4. **结构涌现，不预设**：Index 是输出，不是脚手架。
5. **树是生成树，不是真相**——但现在有**两棵**（见 §2）。
6. **复杂度守恒**：省下的负担必须有承载体（AI / 工具 / 惯例）。
7. **理解的产物是联系**（D5）。

---

## 2. 两棵树（这是新体系的核心）

```
Raw Index  主干   完整 / 唯一归属 / 登记    → 防 node 失散     [D8, D10]
Index      语义树 部分 / 多重归属 / 区域    → 入口与稳定       [D9, D6]
Links      语义边 横跨 ≥2 个 Index 区域     → 理解的产物       [D5, D6]
Node       点     默认体裁
```

| | 边 | 含义 | 能否用于语义聚类 |
|---|---|---|---|
| 主干 | `Raw Index → Node` | **登记**（"你在这儿"）；登记边为结构动作，AI 可直接追加（D22） | **不能**（C2 规则） |
| 语义树 | `Index → Node` | **理解**（"这些是一回事"） | 能 |
| 节点间 | `Node ↔ Node` | 你的判断 | 能（主力） |

**判据两级制**（D20，写进 `check`）：

| 级别 | 判据 | 失败动作 |
|---|---|---|
| **硬门** | root 排空；`archives/material/` 每篇有 `source:`；wikilink 新增悬空 | exit code 1，阻断提交 |
| **报告级** | I1 唯一归属 / I2 Links 跨域（**同区域 = 违规，无区域 = 提示**，随 Index 生长自动消解）/ I3 Node ≥1 出链 / I4 doctrine 与 Raw 不做绑定邻居 | 每周增量数字，不阻断 |

跨领域卡的唯一归属是登记不是判决，可改可争议；**第二归属由 Index 承载**（A6，延伸 D10-P1）。

---

## 3. 结构

```
README.md          入口（最小记忆集）
AGENTS.md          AI 硬规则
doctrine/          Vault Design.md + Vault Workflow.md      [D11, D12]
library/
  <A–Z>_fold/      Node（默认体裁）
  Links/           Links
  Index/           Index（语义树）
  Raw/             Raw Index（主干，永久）                   [D8]
archives/
  material/        外部材料
  work/            我的档案（含 AI 报告）                     [D18]
a_sticker/         todos / or / new_terms / other
zzz_output/        终端产出
tools/             脚本
.agent/skills/     AI 技能
```

**体裁判据：名字 > 路径 > tag。** tag 只用于提示漂移，绝不决定去向。`[已实测]` 40 篇 tag 漂移、12 篇 Node 住错 `Index/`。

**字段**：删 `tags` / `created` / `data-date` / `date`；**保留 `aliases`（136 篇，wikilink 解析依赖）与 `source`（103 篇，含多行列表）**。`[已实测]`
**模板归零**：Node = 纯 markdown，无 frontmatter、无固定小节。`[D7]`

---

## 4. 工作流（3 动词 + 1 循环）

| 动作 | 触发 | 做什么 | 检查 |
|---|---|---|---|
| **捕获** | 有想法 / 读到东西 | 写 Node → **当场链 ≥1 篇 + 一句 why** → 未完成挂 todo | I3 |
| **整理** | 每周 | `vault.py triage` → 归档 + 清 root | root 空 |
| **聚簇** | 每周（**新工作流的核心**） | `vault.py rawindex --clusters` → 写共性 → 建 Index/登记主干 | I1、I2 |
| **问箱** | 每周 / 卡壳 | 随机笔记 + backlink → 补链接，产出直接落为 Links 卡 | — |

**节律可见性**：`status` 顶部显示：上次整理 / 上次聚簇 / 上次问箱 距今 N 天（git log + mtime 推导，零手工记录）。

**节律**：学完即捕获 / 每周整理 + 聚簇 + 问箱 / 每月 check。

### 4.1 聚簇的六轮收敛与粗主干归组 `[已实测]`

流程（A2 裁决后）：**聚类（递归切分）→ AI 把簇归组进粗 Raw Index（一个含几个簇）→ 簇内共性写进 Index → 重跑 L0**。
`--clusters` 输出格式相应改为「簇 → 建议归入的粗 Raw Index」。

| 轮 | 新增簇 | 覆盖节点 | 下轮可自动归属 | 剩余 |
|---|---|---|---|---|
| 1 | **34** | 166 | 179 | 329 |
| 2 | 19 | 100 | 41 | 188 |
| 3–6 | 15 | 67 | 13 | **108** |

**674 条队列 → 6 轮 → 108 条。** 第一轮吃掉 25%，之后边际递减。
**这是 D8"主干要人工维护"这个担忧的答案：它是有界的。** 簇数 68 不再等于 Raw Index 数——粗 Raw Index 由 AI 归组维持（D10-P3）。

### 4.2 人机分工（D16）

| 产物 | 谁 |
|---|---|
| 队列 + 归队提议 + 簇 + **绑定证据（共同邻居）** | 工具 |
| 共性**草稿**（只准基于绑定证据写） | AI |
| **共性定稿 + 命名** | **你** |

规则：**每簇必须有一句你写的共性，否则不进 Index。**

---

## 5. 场景（10 个）

| # | 场景 | 关键动作 |
|---|---|---|
| S1 | 读到外部材料 | 进 `material/`，写 `source:`；**不写卡**。拆过它的判据 = 该材料笔记有指向所拆 Node 的出链（D21）；rawindex 报告零出链材料 = 未拆 |
| S2 | 学一个点 | 建 Node，当场链 ≥1 篇 + why。**AI 必给 3 个候选链接（带 why），你选一个**——把当场链接从自律变一键 |
| S3 | 发现跨界联系 | 建 `Links of X`，并置 ≥2 点，不写新知识 |
| S4 | 系统化主题 | **不建骨架**；写点 → 聚簇 → 写 Index |
| S5 | 中断快存 | 原地不动 + 挂 todo + 续写说明（5–10 词） |
| S6 | 定期整理 | `triage` → 归档 root / 补零出链；**todo 条目 >90 天未动 → 报告并清理**；近 7 天创建且零出链零挂钩 → **疑似半成品单列** |
| S7 | 入口 | `status` → 编号选项 |
| S8 | 决策调研类 | 产出进 `archives/work/`，AI 可代笔，你审 |
| S9 | 问箱 | 随机笔记 + backlink → 补链接；**产出直接落为 Links 卡，不另记账** |
| S10 | AI 报告挂载 | 进 `work/` + 登记；可提取的点走 S2 |

---

## 6. 迁移 `[已实测，内容零损失]`

```
keep 753 / move 286 / delete 8 / conflicts 0
missing 0 / extra 0 / body-altered 0
wikilinks 2483 -> 2476    unresolved 248 -> 248   ← 链接零破坏
```

| 去向 | 数量 |
|---|---|
| `archives/material/`（保留子目录） | 122 |
| `archives/work/` | 41 |
| `library/Raw/`（含主干的根 `Raw Index of Everything`） | 19 |
| `library/<fold>/`（根散卡、`Index/` 里 12 篇 Node、归档区 13 篇语言碎片） | ~90 |
| `library/Index/` `library/Links/` | 2 + 3 |
| `doctrine/` | 3 |
| 删除 | 8（仅 template） |

**8 条校验：7 PASS**；唯一失败是**预存**的大小写冲突（见 §8）。

---

## 7. Runbook

```
0. ~~人工：解决 Instantaneous velocity / Instantaneous Velocity 大小写冲突~~ [已完成 2026-10-06：合并入 Instantaneous Velocity]
1. git commit -a -m "chore: pre-migration snapshot"        # 唯一回滚点
2. 迁移：[已实测] 02_plan → 04_migrate (dry-run) → --apply → 05_validate 8 条全 PASS
3. 写 doctrine 两份：Vault Design.md（理念+结构+两棵树）/ Vault Workflow.md（3动词+10场景）
4. 重写 README.md（最小记忆集 3 条）/ AGENTS.md（硬规则）/ 2 个 SKILL
5. 改 tools/vault.py：
     - 删 graph / promote / register-*
     - 加 rawindex（L0–L3 + 递归切分 + 绑定证据 + --check/--clusters/--around）
     - check：lit 判定改按 archives/material/ 路径；白名单改按名字索引；加 I1–I4
     - **check 两级化（D20）**：硬门（root 排空 / material 出处 / 新悬空 wikilink）exit 1 阻断；I1–I4 报告级 stdout 给增量
     - **`rawindex --sync`（B6）**：自动维护主干根 `Raw Index of Everything` 的成员列表
     - **triage todo 老化报告（B1）**：todo 条目 >90 天未动 → 报告；近 7 天创建 + 零出链 + 零挂钩 → 疑似半成品单列
     - **`status` 节律行（B3+B7）**：上次整理 / 上次聚簇 / 上次问箱 / 上次产出 距今 N 天（git log + mtime 推导；「上次产出」源 = zzz_output/）
6. 改 tools/trend_radar.py：4 处 tag 输出 + archives/work/ 路径
7. python3 tools/vault.py check && python3 tools/vault.py rawindex --clusters
8. git status 核对 → commit
```

**注意**：第 2 步已实测；**第 3–6 步只有设计，没跑过**。

---

## 8. 仍未解决（不假装）

| # | 项 | 状态 |
|---|---|---|
| 1 | **输出回路**（D17，B7） | **已裁决（2026-10-06）**：产出 = 手动创建于 `zzz_output/`（人的专属，零判据字段）；每周问箱后 AI 提名最成熟 Links 卡供成文决策（不落 todo、不记账）；`status` 节律行加「上次产出」（git log + mtime 推导）。详见 `archives/work/B7-output-loop-expansion.md` |
| 2 | **B5：捕获规则清零需数周** | 零出链 392/741（52%）`[复验 2026-10-06]`；靠 I3 报告级增量观察，不设硬门 |
| 3 | ~~Instantaneous velocity 大小写冲突~~ | **已裁决（2026-10-06）：合并**——保留 `Instantaneous Velocity`（evergreen、2 入链），删小写版，入链已改写，check 通过 |
| 4 | 674 篇未登记 | 6 轮可清到 108 |
| 5 | 33 篇正文内联 hashtag | 未清理；`#include` 是 C 代码不能误删 |
| 6 | 记忆底座（间隔重复） | 未落地 |

---

## 9. 脚本清单

| 脚本 | 作用 | 状态 |
|---|---|---|
| `01_inventory.py` | 只读盘点 | 已跑 |
| `02_plan.py` | 生成迁移清单 | 已跑 |
| `03_genre_audit.py` | 体裁三方审计 | 已跑 |
| `04_migrate.py` | 执行迁移（默认 dry-run） | 已跑（副本） |
| `05_validate.py` | 8 条二值校验 | 已跑 |
| `06_rawindex.py` | L0–L3 + 递归切分 + I1–I3 | 已跑 |
