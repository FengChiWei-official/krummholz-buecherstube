---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: "本仓库实现 tools/vault.py graph(2026-09-17)+ 原文抽取:archives/Raw math idea.md、library/Index/*、mailbox/*"
---

# Graph of Math — 图在笔记里生长 (AI 提案)

> AI 提案。机制已落地(`tools/vault.py graph`),接线清单待 owner 批准;观点请消化后用自己的话写进你的卡片。

## Text

### 一、要解决的问题(owner 原话)

不是"画一张图"。是让**技巧、对象、共同目标、手段**之间的连接,在你读书做题的过程中**自己长出来**——而不是先搭好目录再往里填。

### 二、为什么"先搭目录"长不起来

现有 §S3 是 toc-first:先建 `Index of <Topic>` + Raw Index,再写卡,再往 Index 的 Core Concepts 里挂。代价是:**第一篇笔记就要决定它属于哪个目录**,而这个决定恰恰在你最不理解它的时候做出;目录一旦重排,所有归属作废。

证据就在库里:`Index of Math Procedures`、`Index of Math Details` 至今是空壳(`Definition` 空、`Core Concepts` 空);`[[Object -- Identify the form of the limit]]` 被两处 Index 挂着,却从没有这张卡——这是当前 `check` 仅存的 2 条 unresolved。**先搭的骨架停在原地,而碎片在长。**

### 三、图的结构(概念层,不依赖任何工具)

- **节点 = 笔记**(以及尚未成为笔记的名字)。**边 = 笔记正文里的一行**。
- 三种边,方向就是"为什么存在":

| 边 | 读作 | 例子 |
|---|---|---|
| `goal:: [[Aim]]` | 这张卡服务于什么目标 | 夹逼定理 → 上下界估计 |
| `object:: [[Shape]]` | 它作用在什么形状/结构上 | 夹逼定理 → 有界振荡结构 |
| `bridge:: [[Elsewhere]]` | 它与外部哪个想法同构 | 夹逼 ↔ 压缩映射 |

- **角色(技巧/手段/对象/目标)是相对的,不是卡的类型。**一张卡可以同时是"A 的手段"与"B 的目标":洛必达 = 求极限的手段,它自己的目标又是"消掉未定式"。**共同目标就是这样连起来的**——同一个目标节点被多条 `goal::` 打中,而它自己又向更高的目标发射。所以不需要给"目标"新标签:标签给卡的**身份**(`attr/technique` = 技巧、`attr/method` = 手段、`attr/concept` = 对象),边给它在**当前这条路线上的位置**。
- **目标节点不需要是笔记。**名字收到第一条边就存在。→ 不用建目录、不用登记、不会因为忘了建而断链(悬空名是钩子,不是错误)。
- **名字经 `aliases:` 解析。**你写"有界性"→`Boundedness`、"夹逼定理"/"迫敛定理"→`Squeeze Theorem`、"数学启发法"→`Raw Index of Mathematical Heuristics`。→ **用你思考时的词写边,库里保持一张卡一个名字**,同义节点自动合并,不产生重复目标。

### 四、生长规则(读书/做题时,成本 = 一行)

1. 在任何笔记里(卡片、例题本、`archives/` 的原文摘录、todo 条目)遇到"这东西是为了……",补一行 `goal:: [[…]] — why`。
2. 遇到"它作用在……形状上",补 `object:: [[…]] — why`。
3. 遇到"这和……是同一个想法",补 `bridge:: [[…]]`。
4. 不建目录、不登记、不重排。写完就完事。

判断一张手段卡是否"长好了":**有 aim + object 两条边**。
- 有 aim 无 object → 找得到,但不知道用在哪(抽象得无处下手)。
- 有 object 无 aim → 学懂了,却不知道为什么学(碎片)。
这两种正是你说的"复杂而被忽视"的两个方向,现在它们是可数的。

### 五、读图(需要时才读,不是维护动作)

```bash
python3 tools/vault.py graph                 # aims ← means(稀的先列)/ objects ← users + aims / 孔洞 / 悬空名 / 未接线草稿
python3 tools/vault.py graph --around 有界性   # 单个名字的邻域:作为目标谁指向它、作为对象谁在用、它自己指向谁(中文别名可直接查)
python3 tools/vault.py graph --unwired mailbox  # 只看某范围内没接线的草稿
```

`vault.py status` 每次会话已经带一段图摘要(next moves 里给编号选项)。**忽视因此变得可见,不靠自律。**

### 六、什么时候才写 Index 笔记(反 toc-first)

只有当某个目标节点已经积累够多 means、你想用自己的话写一段导航时,才写 `Index of ...`。那是**输出**,不是**前置**。内容可以从 `--around <目标>` 读出来,再改写成自己的话。

### 七、从你自己笔记里抽出的第一批节点(证据 = 行号)

目标(`archives/Raw math idea.md` §"Aim wise",line 91):

| 目标候选 | 原文行 | 已被别名覆盖? |
|---|---|---|
| 极限计算 | :133 | `Index of Limit Strategy`(已有卡) |
| 上下界估计 | :108 | `有界性` → `Boundedness` ✅ 别名已通 |
| 存在性证明 | :125 | — |
| 根存在性 | :103 | — |
| 构造方程 | :93 | `Identity to Equation` |
| 回到定义 | :98 | `Back-to-Basics Heuristic Definitions & Generalization` |

对象候选(形状):对偶结构 / 共轭式(:12–30,近邻 `Conjugate`、`Conjugate Radicals`)、三角函数分式(:17)、幂指式 $f(x)^{g(x)}$(:68 → `Power-Exponential Functions Transform`)、复杂根式对数代换(:70 → `Logarithmic Function Toolkit`)、数列和 $\sum_i^n f(i,n)$(:43)、变限积分(:214)——**形状这条轴目前几乎全是空的,是你最该长的一侧。**

手段/技巧候选(已有卡):`Hook Function`、`Conjugate` 族、`Equivalent Infinitesimals`、`Focus on the Dominant`(主部提取)、`L'Hospital Rule`、`Taylor Series`、`Mean Value theorem`、`Squeeze Theorem`、`Principle of Reduction`(化归)、`Case Analysis`、`Parity`(对称性)。

**归属待你定**:原文件把 `映射/同构`(:145)、`渐进分析`(:154)、`放缩`(:172) 放进 "Aim wise",但它们读起来是手段而非目标。doctrine 不猜——你定。

### 八、待批准的第一批接线(S2 式:你点头,我插入)

不用新建任何笔记,边的内容就是**你自己原文结构的转录**:

| 卡片 | 建议插入 | 证据 |
|---|---|---|
| `library/L_fold/Limitation.md` | `goal:: [[Index of Limit Strategy]]` | 该 Index §Overview Route 已列它 |
| `library/R_fold/Rational Limitation.md` 等 6 张路线卡 | `goal:: [[Index of Limit Strategy]]` | `Index of Limit Strategy` §Core Routes 逐一点名 |
| `library/D_fold/Definition-of-E-like Limitation.md`、`library/P_fold/Power-Exponential Functions Transform.md` | `goal:: [[Index of Limit Strategy]]` + `object:: [[幂指式]]`(对象卡待建,骨架我建) | `Raw Index of Limitation Toolkits`:13 把它当幂指类入口 |
| `library/C_fold/Conjugate.md`、`Conjugate Radicals.md`、`Hyperbolic Conjugate Radical.md` | `object:: [[对偶结构]]`(对象卡待建) | `Raw math idea.md`:12–30、`Index of Identity Transform` §Conjugate |
| `mailbox/Equivalent Infinitesimals.md`、`Focus on the Dominant.md`、`L'Hospital Rule.md`、`Standard Limits.md`、`Mean Value theorem.md`、`Principle of Reduction.md` | `goal:: [[Index of Limit Strategy]]` | `Raw Index of Limitation Toolkits` §Infinitesimals/§概论 原文逐步点名 |

需要你决定的还有一个名字:不等式簇(根目录 12 篇,今天新建)的目标节点叫什么——`Raw Index of Inequality Toolkits` 只列了手段(AM-GM、放缩、单调性、夹逼),目标(证不等式 / 估计上下界 / 证有界)目前无卡。

### 九、doctrine 增量提案(需批准)

1. `Collaboration Workflow Spec` §S3 改成 **graph-first**:先写卡+边,Index 是事后的输出而非前置骨架(与 §S4 的"集群成熟才写输出"本来就一致)。
2. `Vault System Design` 增一节「图的生长」:节点=笔记、边=正文一行、角色相对、目标名涌现、名字经 aliases 解析。
3. `template/*-temp.md` 的 `## Graph` 槽位已加(可回滚)。

### 十、试插结果(2026-09-17,owner 批准后已落地)

已插 3 张卡、3 条边(全部指向**已存在**的节点,未新建任何卡):

| 卡片 | 边 | 证据 |
|---|---|---|
| `library/D_fold/Definition-of-E-like Limitation.md` | `goal:: [[Index of Limit Strategy]]` | 该 Index §Exponential Route 已列它 |
| `library/P_fold/Power-Exponential Functions Transform.md` | `goal:: [[Index of Limit Strategy]]` | 同上 |
| `library/C_fold/Conjugate.md` | `goal:: [[Index of Identity Transform]]` | 该 Index §Core Patterns → Conjugate |

报告立刻读出:`Index of Limit Strategy` 有 2 means(共同目标的雏形);`Definition-of-E-like Limitation` 报"有 aim 无 object"——**对象轴的空缺被工具自己指出来了**,这正是下一轮要长的东西。

**S2 发现(待你定,我没有改)**:`Power-Exponential Functions Transform` 与 `Conjugate` 的 tag 是 `attr/concept`,但内容是"变换/模式"(手段),报告里因此显示为 `[object]`;`Conjugate` 的 Definition 目前也是空的。

**下一轮(queued)**:① 不等式簇的手段挂到 `Boundedness`(你已选它作目标节点);② 对象轴建卡(对偶结构 / 幂指式 / 分式有理函数 / 变限积分),之后这些卡才能补 `object::`。

## Graph

goal:: [[Raw Index of Tricks in Math]] — 本方案服务于它:让碎片按目标聚成可复用路线
object:: [[Index of Math Objects]] — 操作的是"对象"这条轴:题库形状的登记处
bridge:: [[树的定义与碎片自动聚合-研究]] — 同一问题的结构层定义(树 = 类型化聚合树)
bridge:: [[减负式联想学习]] — 复杂度守恒:人省下的结构负担必须有承载体,这里承载体就是 vault.py graph

## Sources

- 实现:`tools/vault.py` 的 graph 段(`iter_typed_edges` / `_alias_map` / `_collect_graph`);模板槽位 `template/*-temp.md`。
- 抽取来源:`archives/Raw math idea.md`(行号见上表)、`library/Index/Raw Index of Limitation Toolkits.md`、`Index of Limit Strategy.md`、`Index of Identity Transform.md`。

---
## **Related**

[[Raw Index of Tricks in Math]]
[[Index of Math]]
[[Index of Math Objects]]
[[Raw Index of Limitation Solving Toolkits]]
[[Raw math idea]]
[[树的定义与碎片自动聚合-研究]]
[[减负式联想学习]]
[[Vault System Design]]
[[Collaboration Workflow Spec]]
[[Math Todo]]