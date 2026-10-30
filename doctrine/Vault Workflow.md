# Vault Workflow

> 版本：v6（2026-10-30）。

## Definition

三个动词 + 一个循环。人只做两件事：写下自己的一个点，把它连进旧网（写一句 why）。其余全部由工具与 AI 承载。

## 节律

学完即捕获 / 每周整理 + 聚簇 + 问箱 / 每月 check。

`status` 顶部节律行：**上次整理 / 上次聚簇 / 上次问箱 / 上次产出：距今 N 天**（从 git log 与文件 mtime 推导，零手工记录）。停摆可见 = 停摆可治（trend-radar 曾停摆 9 天无人察觉——这条就是它的教训）。

## 三个动词

| 动作 | 触发 | 做什么 | 检查 |
|---|---|---|---|
| **捕获** | 有想法 / 读到东西 | 写 Node → **当场链 ≥1 篇 + 一句 why** → 未完成挂 todo | I3 |
| **整理** | 每周 | `vault.py triage` → 归档 + 清 root + todo 老化清理 | root 空 |
| **聚簇** | 每周（核心） | `vault.py rawindex --clusters` → AI 归组进粗 Raw Index → 写共性 → 建 Index | I1、I2 |
| **问箱** | 每周 / 卡壳 | 随机笔记 + backlink → 补链接，产出直接落为 Links 卡 | — |

### 聚簇流程（A2 裁决）

**聚类（递归切分）→ AI 把簇归组进粗 Raw Index（一个含几个簇）→ 簇内共性写进 Index → 重跑 L0**。

人机分工：

| 产物 | 谁 |
|---|---|
| 队列 + 归队提议 + 簇 + 绑定证据（共同邻居） | 工具 |
| 归组方案（簇 → 粗 Raw Index）+ 共性**草稿**（只准基于绑定证据写） | AI |
| **共性定稿 + 命名** | **你** |

规则：每簇必须有一句你写的共性，否则不进 Index。登记边（Raw Index → Node）AI 可直接追加（D22）；Index → Node 须你批准。

## 场景（10 个）

| # | 场景 | 关键动作 |
|---|---|---|
| S1 | 读到外部材料 | 进 `material/`，写 `source:`；**不写卡**。拆过判据 = 该材料有指向所拆 Node 的出链（D21）；rawindex 报告零出链材料 = 未拆 |
| S2 | 学一个点 | 建 Node，当场链 ≥1 篇 + why。**AI 必给 3 个候选链接（带 why），你选一个**——把当场链接从自律变一键 |
| S3 | 发现跨界联系 | 建 `Links of X`，并置 ≥2 点，不写新知识 |
| S4 | 系统化主题 | **不建骨架**；写点 → 聚簇 → 写 Index |
| S5 | 中断快存 | 原地不动 + 挂 todo + 续写说明（5–10 词） |
| S6 | 定期整理 | `triage` → 归档 root / 补零出链；**todo 条目超过老化阈值未动 → 报告并清理**；时间窗内创建且零出链零挂钩 → 疑似半成品单列（阈值见 `tools/vault.toml`） |
| S7 | 入口 | `status` → 节律行 + 编号选项 |
| S8 | 决策调研类 | 产出进 `archives/work/`，AI 可代笔，你审 |
| S9 | 问箱 | 随机笔记 + backlink → 补链接；**产出直接落为 Links 卡，不另记账**；问箱后 AI 提名最成熟 Links 卡供成文决策 |
| S10 | AI 报告挂载 | 进 `work/` + 登记；可提取的点走 S2 |

## 产出（B7 已裁决）

产出是**人的专属**：手动在 `zzz_output/` 创建的文件即产出。零判据字段、零内容检查。AI 的角色上限：每周问箱后提名候选 Links 卡、验证链接。写作永远是你。

`zzz_output/Root.md` 是主树入口：tree entry `Root.md` → `Raw Index of Root` → topic indexes。

## AI 边界

**AI 是磨刀石，不是代笔。** 问题、结构、链接、检查——正文永远是人写。AI 生成的散文属于 `a_sticker/or/`，作为原材料等待消化，绝不直接进 `library/`。`zzz_output/` 内容 AI 永不代笔、永不编辑（git 状态可查、链接可验）。

链接的批准权（S2 继承）：**Node↔Node 与 Index→Node 的新链接须 owner 批准**（链接改变笔记意义）；登记边（Raw Index → Node）是结构动作，AI 直接做；结构修复（改名、归位、悬空修复）AI 直接做。

## 心法（窍门显性化）

这一节收拢散落在 `archives/work/PLAN.md`、`计组融贯性诊断.md` 与技能里的窍门——新人不必自己拼。

1. **聚簇收敛有界**：实测 674 条队列 → 6 轮 → 108，首轮吃掉 25%。**队列大不必怕**；每周一轮，别想一次清空。
2. **绑定证据 = 共同邻居**，阈值 θ 取高分位（`cluster_theta_percentile`）。簇是数据推出来的，不是猜的——所以「为什么这两篇在一起」永远能指回证据。
3. **粒度闸门**：整体层只收四类——**层 / 合同 / 根张力 / 不变量**；算法与参数细节一律挡在门外，归章内下钻（见 `archives/work/计组融贯性诊断.md`）。
4. **两级制**：硬门只有 3 条（root 排空 / material 出处 / 新增悬空 wikilink）；其余全是报告级增量。**门常红 = 门失效**——旧体系就死在这里。
5. **信号 ≠ 裁决**：工具输出是信号，内容优先。`triage` 自称「prompt, not verdict」；`suggest` 只给候选，链接由你选。
6. **悬空链接是钩子**，不是错误。它标记「这张卡该存在」；`check` 只拦**新增**的（baseline 白名单在 `tools/vault.toml` 的 `whitelist_unresolved`）。
7. **登记边 ≠ 分类**：Raw Index 说「它在这」，不说「它是什么」。归属可改可争议，第二归属由 Index 承载。
8. **半成品只靠时间窗识别**：时间窗内创建 + 零出链 + 零挂钩（A1）。三条同时成立才报——这是启发式，不是判决。

### 约定（写在文档里，不自动化）

- **D16**：簇的共性句子与新 Raw Index 的名字**由你写**；AI 只提归组方案。共性句必须基于绑定证据。
- **D10-P3**：一个粗 Raw Index 装**几个**簇；细结构（簇 + 共性）进 Index。绝不每簇一个 Raw Index。
- **`-MOC` 是 index 体裁**：名字以 `-MOC` 结尾的笔记与 `Index of*` 同属 `library/Index/`。
- **todos 登记是体裁例外**：`a_sticker/todos/Index of Todos.md` 是 todo 树的登记册，不套 library 的体裁规则。
- **`triage` 的六个类别**：`root` / `todo_stale` / `halfdone` / `unhooked`（root 队列无 todo 挂钩，S5 防丢）/ `genre`（体裁错位）/ `dead_todo`（`- [x]` 指向不存在的名字）。前三类写在 S1–S10 里，后三类是工具新增，等价重要。
- **`rawindex --top` 默认 10**（`rawindex_top` in `tools/vault.toml`）：L0 提议只列前 N 条，别一次看 500 条。
- **todo 老化只看顶层文件 mtime**，`a_sticker/todos/archived/` 豁免。
- **`--sync` 默认 dry-run**：确认输出后再加 `--apply`。

## Related

- [[Vault Design]]
- [[Agent Contract]]
- [[Index of Todos]]
