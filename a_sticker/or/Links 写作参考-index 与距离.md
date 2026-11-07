# Links 写作参考 — index / 距离 / 基准

> `a_sticker/or/` 里的**写作参考**（AI 散文）；成品 Links 卡请落 `library/Links/Links of X.md`。
> 配套：[[index 运算规范化-参考资料卡]]（名称 / 运算 / 工作流）。
> 今天转正/改正的节点簇（两类型 + 基准）：[[Index]]（类型：序号/位置）、[[Distance]]（类型：位移/长度）、[[Index Frame]]（基准）、[[0-index]] / [[1-index]]（基准两取值）——library，已登记 Raw Index of Algorithm。

## 1. 体裁规则（工具口径，别凭记忆）

- 命名 `Links of X`，前缀 `Links ` 决定 zone = `library/Links/`（`vault.py links` 帮助）。
- **I2**：Links 卡必须横跨 **≥2 个 Index 区域**；同区域 = 违规；无区域 = 提示（report 级，不阻断）。
- **D16**：**卡片名与共性句由你写**，且共性句必须落在工具打印的证据上。
- 证据分级（`tools/vault.toml [thresholds]`）：名字 `3` / 别名 `3` / 结构（同登记·链到被种子链）`2` / 正文命中 `2` / 共同邻居 `1`。**只共享区域不算证据。**
- 命令（只读）：`python3 tools/vault.py links-candidates "TOPIC"`；找不到种子就退到 `retrieve`。

## 2. 三步写法

1. 选**主题词**（越具体越好；过宽会得到 700+ 成员，见 §3「Index」）。
2. 跑 `links-candidates "TOPIC"` → 拿种子、区域覆盖、成员 why。
3. 写卡：一句洞见 + 成员表（每行一个 why）+ Related 指回本参考与素材卡。

## 2b. 怎么设计、怎么认识（先写的是工作流那张）

**设计三件事**：① 卡的是**概念**不是关键词；② 证据只认 `links-candidates` 打印的那几类（只共享区域不算证据）；③ **跨区**是硬条件（≥2 个 Index 区域，I2）；名与共性句按 **D16 归你**。

**这次的事实（工具实测，2026-11-06）**：

| 主题词 | 覆盖区域 | 结论 |
|---|---|---|
| Loop | 1 | 工作流的**自家卡全在 Index of Algorithm**，单靠「工作流」词**成不了** Links 卡 |
| Invariant | 1 | 同上 |
| Boundary | 1 | 同上（要换 `Bound` 才 12 区，但那是另一张卡：边界与有界性） |
| **Frame** | **2** | **唯一的桥**：算法（`Index Frame`/`0-index`/`1-index`…）× 几何（`Frenet-Serret Frame`/`Coordinate Frame`/`Arc Length Element`…） |
| Distance | 6 | 另一条可走的路（算法 × 几何 × OS），证据多为「同登记」= 结构 2 |

**认识（洞见）**：工作流的三条不变量——
1. **基准显式**（S0/S5）：每个 `±1` 都能指回一条声明过的 frame；
2. **算子分级**（S2/S4）：仿射/线性可自由组合，数制算子只能共轭出现 `f_φ = φ∘f₀∘φ⁻¹`；
3. **不变量只在差上**（S3/S6）：长度 = 差（rank 0）、点数 = 差 + 1（rank 1），返回值必须声明是哪一个。

而这三条恰好就是 **frame 的定义性内容：frame 不是被观测的对象，而是「读数赖以成立的那组约定」**。算法里的 0/1-based 与几何里的标架 / 参考系是同一角色的两种实例——这就是这张卡跨区共性句唯一能站住的地方。

## 3. 今天实测过的主题（可直接复用；数字是本次运行结果）

| TOPIC | 种子 | 覆盖区域 | 达标 | 备注 |
|---|---|---|---|---|
| Bound | 8（`Lower Bound`、`Upper Bound`、`Binary Search for Boundaries`、`Four Boundaries Traversal Matrix`、`Looper Boundary Conditions`、`Boundedness`…） | **12** | ✓ | 最稳的一张，算法 × 数学/极限 × 缩放归一化 |
| Index | 8（`0-index` `1-index` `Dynamic Programming Indexing` [[Index]]…） | 31 | ✓ 但过宽 | 752 成员，噪声主导，不建议直接用 |
| Distance | 3（`Arc Length`、`Hamming Weight & Distance`、`Storage Hierarchy as Distance`） | 6 | ✓ | 成员多来自「同登记」= 结构 2 |
| Coordinate | 8（`Coordinate Frame`、`Linear Coordinate Transformation`、`Polar Coordinate System`…） | 3 | ✓ | 几何侧强，可与 B 卡配合 |
| Indexing | 1（`Dynamic Programming Indexing`） | 1 | ✗ | 算法侧够，第二区缺 |
| Quotient | 1（`Quotient Group`） | 1 | ✗ | 抽代侧够，算法侧缺 |
| Boundary | 1（`Looper Boundary Conditions`） | 1 | ✗ | 换词用 `Bound` 立刻达标（见上行） |
| Mirror | 1（`858. Mirror Reflection`） | 1 | ✗ | 几乎空，需先建题卡 |

## 4. 推荐的 Links 卡（按可行性排序）

### 4.0 先写这张：index–distance 工作流 → 「Frame」桥（可粘贴草稿）

**为什么是它**：工作流的三条不变量全靠「先声明基准」撑着，而「基准」在库里天然跨区（`Frame` = 2 区）。所以这张卡 = 工作流的**第一步**（S0）作为概念，从算法与几何两侧看。

- 目标路径：`library/Links/Links of … .md`（**名你定**，D16）
- **名称候选**：`Links of Index Frame and Coordinate Frame`（工具原提案形）／`Links of Frame and Workflow`／`Links of Frame and Reference`
- **共性句候选**（都在打印证据上，任选或改写）：
  a. 基准不是被观测的东西，而是「读数赖以成立的那组约定」。
  b. 换基准不动不变量：算法换 0/1-based、几何换标架，靠的是同一条换算。
  c. 工作流的每一步都在维护一条基准声明——几何把它叫参考系。

**成员表（已完成区域与证据标注；噪声已圈出）**：

| 成员 | 区域 | 证据 | 备注 |
|---|---|---|---|
| `Index Frame` | （种子） | 名字含 `Frame` ★ | 算法侧核心（今天新建） |
| `0-index` / `1-index` | — | 链到种子 `Index Frame` | 基准的两个取值 |
| `Frenet-Serret Frame` | Index of Vector Calculus & Geometry of Curves | 名字含 ★ | 几何侧核心 |
| `Coordinate Frame` / `Polar Coordinate Frame` / `Frame of reference` | 名字命中 | 名字含 ★ | 参考系家族 |
| `Arc Length Element` / `Binormal Vector` / `Build up Your Geometric Building` | 几何 | 被种子链 · 链到种子 | 标架的成员与用例 |
| `Dynamic Programming Indexing` / `Lower Bound` / `Upper Bound` / `Template of Sliding Window` / `Template of Fixed Window` / `Looper Boundary Conditions` | Index of Algorithm | **同登记（结构 2）** | 证据偏弱：写句子时别把它们当强证据 |
| `Ethernet Frame` / ARP×3 / `Gin Framework` / `The OPD Problem-Solving Framework` | 网络·工程 | 名字含 | **噪声（同词不同物），建议剔除** |

**粘贴块**：

```markdown
## Definition
<共性句：基准是「读数赖以成立的那组约定」；算法与几何各给一例>

## Members
| 成员 | 区域 | why |
|---|---|---|
| [[Index Frame]] | — | 名字含 `Frame`（算法侧） |
| [[Frenet-Serret Frame]] | Index of Vector Calculus & Geometry of Curves | 名字含 `Frame`（几何侧） |
| [[0-index]] / [[1-index]] | — | 链到 [[Index Frame]] |

---
## **Related**
[[Links 写作参考-index 与距离]]
```

### A（最稳）——`Bound` 主题：边界与不变量
- 跨区证据：12 区，含 Index of Algorithm、Index of Limit Strategy、Index of Scaling and Normalization、Index of Structural Exploitation、Index of Useful Functions…
- 成员建议：算法侧 `Lower Bound` / `Upper Bound` / `Binary Search for Boundaries` / `Four Boundaries Traversal Matrix` / `Looper Boundary Conditions` / `Pre-condition Check` / `Bounded Knapsack DP`；数学侧 `Boundedness` / `Proving the Given Function is Bounded`（各自区域以 `place` 复核后再写进表）
- 洞见方向（由你落句）：*边界是「结构停止成立的那条线」——循环上界、积分端点、背包容量说的是同一件事*

### B（最有价值）——`Links of Frame and Gauge`：换基准 = 选代表元
- 抽代侧（Index of Abstract Algebra）：`Quotient Group` / `Normal Subgroup` / `Kernel of Homomorphism` / `Isomorphism`
- 几何侧（Index of Vector Calculus & Geometry of Curves）：`Coordinate Frame` / `Linear Coordinate Transformation` / `Polar Coordinate System`
- 算法侧（Index of Algorithm）：[[0-index]] / [[Index]] / `Dynamic Programming Indexing`
- 洞见方向：*换基准不改不变量，只改坐标；代码里的 `±1`、补码的代表元、商群的陪集是同一件事*（接你 11-05 的补码/商群线）

### C（待补一区）——`Links of Index and Distance`
- 现状：`links-candidates "Indexing"` 只覆盖 1 区；`"Index"` 又过宽。
- 补法：从 `Index of Concepts of Data` / `Index of Data Structure` 里挑数组侧成员（`Linear List` / `Sequential List` / `Storage Structure` / `Inserting Nodes into a Linked List`），或用主题词 `Offset` / `0-based` 再跑一次。
- 洞见方向：*位置与距离是两种量：换基准只动坐标不动差；库里所有 `±1` 都是这条换算的痕迹*（素材全在 [[index 运算规范化-参考资料卡]] §1–§2b）

## 5. 模板（复制即用）

```markdown
## Definition
<一句洞见；必须落在证据上，并点明它横跨哪两个区域>

## Members
| 成员 | 区域 | why（证据种类） |
|---|---|---|
| [[X]] | Index of … | 名字含 / 链到 / 同登记 / 共同邻居(具名) |

---
## **Related**
[[Links 写作参考-index 与距离]]
```

## 6. index/distance 节点簇（2026-11-06 改名后）

| 节点 | 落点 | 角色 |
|---|---|---|
| [[Index]] | `library/I_fold/` | **类型**：序号 / 位置（Pos）——原 `Function called Index` 改名而来 |
| [[Distance]] | `library/D_fold/` | **类型**：位移 / 长度（Vec），新建 |
| [[Index Frame]] | `library/I_fold/` | 概念：基准（frame）——原 `Links of different Indexes` 改名而来（本就不是 Links 卡：成员不跨区域） |
| [[0-index]] / [[1-index]] | `library/0_fold/` | 基准的两个取值 |

- 五张都登记于 Raw Index of Algorithm（L2 簇登记）；`Index` / `Distance` 互为对偶边。
- 已落笔：[[Index]] 的 Definition（保留你原句作基准实例 + 一句类型定义）、[[Index Frame]] 的一句定义、四条 why 链。
- 未落笔（**等你点头**）：[[Distance]] 的 Definition 正文；[[0-index]] / [[1-index]] 各自的定义句（现在只互链 + 指向 [[Index Frame]]）。
- 素材现成：[[index 运算规范化-参考资料卡]] §6 命名表、§7 运算签名可直接摘。

## 7. 待裁决

- [x] 先写哪张：**§4.0**（index–distance 工作流 → Frame 桥）；A（Bound，12 区）、B（代数 × 几何 × 算法）、C（Index × Distance，待补一区）排队在后。
- [ ] §4.0 的**名字与共性句你落**（D16）；落完我把成员表按区域复核、剔噪声、逐条 `place` 验证。
- [x] `Links of different Indexes` 已改名 `Index Frame` 并归位 `library/I_fold/`（不再是 Links 体裁）。
- [ ] [[Distance]] 与两个基准节点的定义正文要不要我填。
- [ ] §3 的实测表要不要固化成每次复跑的命令清单（省得下次重扫）。
