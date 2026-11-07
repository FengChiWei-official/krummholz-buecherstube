# index 运算规范化 — 参考资料卡

> 位置：`a_sticker/or/`（AI 散文的合法家）。本卡是**待裁决的整理稿**，不是 library 正文；
> library 卡片的正文修订与 bug 修复都要 owner 点头。取证范围：`archives/material/algorithms/`（69 篇）+ `library/` 相关卡，直接跑 `vault.py retrieve` 复现。

## 0. 一句话

**位置（index）是点，距离（length / gap）是差。** 库里所有散落的 `+1` / `-1` 都不是「风格」，而是「位置 ↔ 距离」的换算痕迹（就是 k-index 里的 rank）；区间形态（半开 or 闭）与基准（0-based or 1-based）是 **frame**。规范化不是消灭 `±1`，而是：**把 frame 显式化 + 把换算集中成函数**。

## 1. 语料取证（逐字，file:line）

| 出处 | 原文片段 | 归类 |
|---|---|---|
| `library/L_fold/Looper Boundary Conditions.md:4-8` | `const int state_start = 32` … `for (int state = state_start; state < state_end; state++)` | 半开 frame（`<` 上界） |
| `library/L_fold/Looper Design Normal Form.md:5-12` | "**ENSURE** end_point be **static**, to satisfy [[Loop Invariant Principle]]" | 上界必须是**位置常量** |
| `archives/material/algorithms/59. Spiral Matrix II.md:72-77` | `for (; j < j + len; j++)` … "That broke [[Loop Invariant Principle]]. the end of the loop is running with the `state` `j`." | 用**会动的 state** 表达上界 → 不变式死；修法 `edge = j + len`（把距离预先冻成位置） |
| `archives/material/algorithms/59. Spiral Matrix II.md:33,40` | `int looper = n / 2 ; // + n % 2; //close-end so 1 based` / `int len = n - l - 1;` | 注释承认「闭 frame 的 1-based」；`len` = 距离，由位置算出 |
| `library/L_fold/Lower Bound.md:8-11` | `int r = nums.size(); while (l < r) { int m = l + (r-l)/2;` | 半开 + **距离式中点**（正确样板） |
| `library/U_fold/Upper Bound.md:11-24` | `while(l<r)` … `int m = l + (r-l)/2; // Attention! Out of Limit` … `if (nums[m] <= target) l = m+1; else r = m;` … `return l;` | 半开 `r` 不含；注释点出 `(l+r)/2` 的溢出 |
| `archives/material/algorithms/704. Binary Search.md:24-32` | `For Open Interal($[l, r]$)` … `so you use `while (left <= right)``；`For half-open Interal($[l,r]$)` … `so you use `while (left <= right)`` | **病灶**：两种 frame 用了同一句伪码，且记号写成同一个 `[l,r]` |
| `library/F_fold/Four Boundaries Traversal Matrix.md:9-17` | `int right = cols-1; int bottom = rows -1;` / `while (left<=right&&top<=bottom)` | 闭 frame（矩阵四条边要包含端点） |
| `library/T_fold/Template of Sliding Window.md:46-49` | `// window size is **r - l + 1**` / `ans = max(ans, r - l + 1);` | 闭 frame 的**派生量**：长度 = `r-l+1` |
| `library/T_fold/Template of Fixed Window.md:21,29` | `// 這裡 left 隱式為 r - p.size() + 1` / `ans.push_back(r - p.size() + 1);` | 「由距离求位置」的实锤：`+1` = 闭 frame 偏移 |
| `library/T_fold/Template of BFS with Cycles.md:8-9` | `// visited uses 1-based index!!!` / `vector<int> visited(n+1, 0);` | **frame 显式声明**（正确样板）；`n+1` = 点数 |
| `library/B_fold/BFS Templates.md:10` | `vector<int> vis(n+1, 0);` | 同 `n+1`，但**未声明** 1-based |
| `library/D_fold/Dual Sequence DP.md:6-14` | "Index of DP is current **prefix length** of each Sequence." / `A[0:i]`、`A[0:i-1]` | DP 下标 = **距离型**；切片记号是半开 |
| `library/D_fold/Dynamic Programming Indexing.md:10-14` | `int dp_a = a.size+1;` … `int current_b = b[j-1]; // handle 0-base index(centralized)` | 状态=距离、数组=位置，换算是 `[j-1]` |
| `archives/material/algorithms/121. to 123 and 128 Best Time to Buy and Sell Stock.md:62` | `const int cur = prices[i-1] // key point 2. i-1 to 0-based` | 换换算**写进注释**（可推广为规范） |
| `archives/material/algorithms/Implement of Regular Expression Matching.md:20-22,64` | `// 因此 dp 的大小需要是 (m+1) * (n+1)` / `char sChar = s[i - 1];` | 偏移数组 + `i-1` |
| `archives/material/algorithms/300. Longest Increasing Subsequence.md:68` | `$DP[i] = \max(1, \max_{j=1}^{i-1}(DP[j]+1, ...))$` | **1-based 公式压在 0-based 数组上**（j 从 1 起） |
| `archives/material/algorithms/2D Cost Knapsack Template.md:13-15` | `for (int i = m; i >= wm; i--)` … `dp[i][j] = max(dp[i][j], dp[i-wm][j-wn]+1);` | 容量下标 = 距离型；重量 = 位移 |
| `library/P_fold/Pre-condition Check.md:14-15` | `int limit = (int)text.size() - 3;` / `for (int i = 0; i <= limit; ++i)` | **距离式上界**（`size - 窗长`），替代 `i+len<=n` 的手写 `±1` |
| `library/M_fold/Monotonic Stack.md:26,32` | "- [ ] What kind of elements it is? -> **Index**" / "assign values to the answer array **by index** instead of using `push_back`" | 位置型写入 vs 顺序型写入 |
| `archives/material/algorithms/42. Trapping Rain Water.md:9` | "- [ ] What kind of elements it is? -> **Index**" | 同上（单调栈存位置） |
| `archives/material/algorithms/739. Daily Temperatures.md:8` | "you should assign values to the answer array **by index** instead of using `push_back`" | 同上 |
| `archives/material/algorithms/200. Number of Islands.md:21,27-29` | `vector<pair<int,int>> dirs = {{0,1},{1,0},{0,-1},{-1,0}};` / `int rs = g.size(); int cs = g[0].size();` | **位移向量** + 位置范围 |
| `archives/material/algorithms/33. Search in Rotated Sorted Array.md:9` | "you can tell which part a integer belongs to, by comparing with `nums[0]`" | 显式选**基准点**（原点） |
| `library/P_fold/Edgings in algo.md:11-13` | `### Index` / `1. Is it the 1-index or 0-index` | 问题**已提出、未回答** |
| `library/A_fold/Algorithm tips.md:54` | `(a - b) % mod` → `((a - b) % mod + mod) % mod` | 数制算子（`%`）另需防雷 |
| `library/B_fold/Binary Search.md:3-4` | "Specific binary search … return `bool`. General … returns `index`." | 返回值语义（缺 length / count 一档） |

## 2. index ↔ distance 的三条律

**律 1（长度律）**：距离是 frame 的派生量。
- 半开 `[l, r)`：`len = r - l`
- 闭 `[l, r]`：`len = r - l + 1`
两者恒差 1 位 —— **这个 1 就是 k-index 的 rank**；只有 `r - l`（距离）在换 frame 下不变，`r - l + 1`（点数）会变。

**律 2（换算律）**：`位置 = 起点 + 长度 - frame 偏移`。库里所有 `r - p.size() + 1`（Fixed Window）、`i - 1`（DP/股票）、`n + 1`（BFS 数组长度）都是这一条的特例，且**都出现在「距离→位置」或「位置→距离」的瞬间**。

**律 3（算子律）**：算子和 frame 的关系决定它能不能自由混用。
- **仿射**（平移、区间端点、中点、加权平均）与 frame 无关 → 可以自由换算，只要 frame 写明；
- **线性**（长度、gap、差值）只作用在距离上 → 不许作用在位置上；
- **数制算子**（`⌊·/2⌋`、`>>1`、`%`、`lowbit`、`i*W+j`、乘法）**必须与 frame 绑定** —— `m = l + (r-l)/2`（用距离）✅ vs `(l+r)/2`（用位置和，溢出且绑 frame）❌，`lowbit` 逼出 1-based，`%n` 逼出环形距离。

### 2b. 四类题族的 index 算子映射（按 2026-11-06 问的题型分）

| 题型族 | 库里的卡 / 题 | index 算子 | 类别 |
|---|---|---|---|
| 网格 BFS / DFS | [[Grid BFS and DFS]]（**空壳**）、[[DFS Template]]、[[Connectivity DFS]]、[[200. Number of Islands]]、[[牛客_小红走迷宫]]（空） | 邻居 = 位置 **+** 位移（`dirs` 四向）；边界 = 位置范围 `0<=x<rs`（不是长度）；`vis` 基准（`n+1`/1-based）要声明 | 仿射 + 线性 |
| 矩阵旋转 / 翻转 | [[Matrix-based Simulation Problem]]、[[Four Boundaries Traversal Matrix]]、[[59. Spiral Matrix II]] | `(i,j) → (j, n-1-i)` 等 = **二面体群 $D_4$** 的作用；`n-1-i` 是仿射（`-1` 是 rank 痕迹） | 仿射 |
| 螺旋 / Z 字形 / 蛇形 | 同上 + 498（无卡） | 四边界 `top/bottom/left/right` = **闭 frame**；`len = n - l - 1` 是位置↔距离换算 | 仿射 + 换算律 |
| 维度压缩 / 重塑 | [[Matrix-based Simulation Problem]] §4、74 / 566（无卡） | `index = r*n + c` = **数制算子**（n 进制商余）→ 必须绑 frame | 数制 |
| 反转 / 回文 | [[Algorithm Decision Tree]] A2 支、[[Two Points Algorithm]]、[[Reversibility]]、344/151/9（无卡） | `i ↔ n-1-i` 对称 = 仿射；跨度 `n-1` = 距离 | 仿射 |
| 图论（非网格） | [[BFS Implement Principle]]、[[Connectivity DFS]]、[[Disjoint Set Union]]、[[841. Keys and Rooms]] | 顶点编号基准（题面给 1-based 还是 0-based）**一处声明**；`adj[u]` 是位置，层数/距离是距离 | 帧声明 + 仿射 |

判据用法：**同族内的旋转/翻转/对称都是仿射算子，可以安全地与 frame 换算混用**；真正要小心的只有三类——① 维度压缩的 `r*n+c`；② 一切 `%`/`lowbit`/`÷2`；③ `n+1` 或 1-based 数组的基准声明。这与 §3 的 N1/N5 是同一件事。

## 3. 规范（待裁决，7 条）

- **N1｜frame 必须显式**：每处窗口/二分/遍历写明 `[l, r)`（默认，半开）或 `[l, r]`（闭）；长度一律用律 1 推，**禁止在更新行手写 `+1`**。
- **N2｜±1 只允许出现在两处**：① 收缩/丢弃边界（`l = m+1`、`r = m`）；② 一个具名换算函数（如 `pos_from_len(start, len, frame)`）。其余 `±1` 视为可疑。
- **N3｜循环上界必须是位置常量**：`edge = start + len` 冻结，禁止 `j < j + len`（`59` 的实锤）。这条只是把既有 `Looper Design Normal Form` 用 index/distance 语言重述。
- **N4｜DP 下标是距离型，数组下标是位置型，换算写成 `[i-1]` 就地注明**（`Dual Sequence DP`、`Dynamic Programming Indexing`、`121` 已这么做 → 升为规范）。`300 LIS` 那种「1-based 公式压 0-based 数组」必须二选一：要么状态也 0-based，要么数组开 `n+1`。
- **N5｜数制算子绑 frame**：`÷2 / % / lowbit / ×` 四处只准出现在声明了基准的地方；`n+1` 与 1-based 数组**一处声明**（模板：`visited uses 1-based index!!!`）。
- **N6｜返回值三态**：`index`（位置）/ `length`（距离）/ `count`（= length + 1，点数）。签名或注释写明（`Binary Search` 已区分 bool/index，缺 length/count）。
- **N7｜写前四问**：① 这变量是位置还是距离？② 当前 frame 半开还是闭？③ 这个 `±1` 是哪条换算来的？④ 这个算子绑了哪个 frame？

## 4. 病灶与缺口（file:line，未修）

1. `archives/material/algorithms/704. Binary Search.md:24-32` —— 两种 frame 给了同一句 `while (left <= right)`；记号 `Open Interval($[l,r]$)` 与 `half-open($[l,r]$)` 用了同一括号。
2. `library/D_fold/Dynamic Programming Indexing.md:10,24-29` —— `a.size+1`（缺 `()`）、`for (int i = 1; j < dp_a; i++)`（循环变量写错）、`int current_a = a[j-1]`（应为 `i-1`）。
3. `library/T_fold/Template of BFS with Cycles.md:31` —— `queue.push(start);`（`q` 写成了类型名）；且 `graph` 的索引基准未声明。
4. `library/L_fold/Lower Bound.md:16` —— `if (v_m < cur)` 后无分支，模板主体截断。
5. `library/P_fold/Prefix Sum.md`、`library/F_fold/Fenwick Tree.md`、`library/S_fold/Segment Tree.md`、`library/S_fold/Sparse Table.md` —— **空壳**：偏移数组与数制算子最该落规范的四张卡没有正文。
6. `library/P_fold/Edgings in algo.md:11-13` —— 1/0-index 的问题挂着没有答案（本卡 §3 就是候选答案）。
7. `library/F_fold/Four Boundaries Traversal Matrix.md` 与 `library/T_fold/Template of Sliding Window.md` 用闭 frame，`library/L_fold/Looper Boundary Conditions.md`/`Lower Bound`/`Upper Bound` 用半开 —— 两套并存**不是错**，但都没声明，属 N1 缺口。

## 5. 与既有 Normal Form 卡的接法

既有词汇已经够用，缺的是「一张把 index/distance 串起来的 Normal Form」：

- [[Loop Invariant Principle]]（while 条件一致）+ [[Looper Boundary Conditions]]（半开 `[start, end)`）+ [[Looper Design Normal Form]]（上界静态）→ **N1/N3 是它们的 index 语言版**；
- [[States Update Form]]（状态在哪更新，队列在 PUSH 更新）→ 与 **N2** 同一纪律；
- [[Pre-condition Check]]（距离式上界前置检查）→ **N7①③ 的样板**；
- [[Monotonic Stack]] 检查表（元素是 Index / 按 index 写入答案）→ **N6**；
- [[Dual Sequence DP]] / [[Dynamic Programming Indexing]] → **N4**；
- [[Binary Search for Boundaries]] + [[Lower Bound]] / [[Upper Bound]] → **N1+N5 的样板**（距离式中点已正确）；
- [[Edgings in algo]] 的 "1-index or 0-index?" → 由 **N1+N5** 回答。

### 5b. 与 index/distance 节点簇的关系（2026-11-06 晚，名字已改正）

两类型 + 基准：

| 节点 | 落点 | 角色 |
|---|---|---|
| [[Index]] | `library/I_fold/` | **类型**：序号 / 位置（Pos 侧） |
| [[Distance]] | `library/D_fold/` | **类型**：位移 / 长度（Vec 侧） |
| [[Index Frame]] | `library/I_fold/` | 概念：基准（frame），把位置映成读数 |
| [[0-index]] / [[1-index]] | `library/0_fold/` | 基准的两个取值 |

- 五张全部登记于 Raw Index of Algorithm（L2 簇登记）。
- **旧名已改正**：`Function called Index` → [[Index]]；`Links of different Indexes` → [[Index Frame]]（它不跨 Index 区域，本就不是 Links 卡；改名后体裁回到 node，文件移到 I_fold）。级联共改 9 处引用 / 5 个文件。
- **悬挂链已修**：原来那条「1-Index（大写 I）」改成小写 `1-index`，G3 转绿。
- 分工：节点讲**是什么**，本卡讲**怎么换算、换算写在哪**。

## 6. 命名规范（三处改名 + 变量命名）

| 旧写法 | 规范名 | 记号 | 为什么改 |
|---|---|---|---|
| k-index | **基准化坐标**（framed coordinate） | $(v \mid k)$ 或 $(v;\varphi)$ | 原名只说了「有 k」，没说 k 是**基准** |
| rank | **基准号 / frame index** | $k$，或整个 frame $\varphi=(a,b)$ | 「rank」与矩阵的秩 / 张量的阶撞名，而这是完全不同的东西 |
| $\rho(v,r)=v-r$ | **归一化映射**（normalization） | $\rho(v,\varphi)=\varphi^{-1}(v)$ | 与项目名「规范化」对齐，且 $a=1$ 时就是 $v-r$ |
| $H=\langle(1,1)\rangle$ | **基准群**（gauge group） | $H$ | 换基准的自由度 |
| index | **序号 / 位置**（Pos 侧） | $p\in\mathcal P$ | 与下面的 Vec 侧分开 |
| distance / length | **位移 / 长度**（Vec 侧） | $\Delta(p,q)$、$len$ | 只作用在差上 |
| count | **点数** | $len+1$ | 必须与 length 分开：rank 1 vs rank 0 |

**「第二位」与 frame 的关系**（易混，单独记）：元组 $(v \mid k)$ 的**第二位 $k$ 是 frame 的坐标（基准号），不是 frame 本身**；frame 是那位名字对应的函数 $\varphi_k(x)=x+k$。

$$\text{基准化坐标}=(v\mid k)=\big(\varphi_k(p),\,k\big),\qquad \rho(v,k)=\varphi_k^{-1}(v)=v-k$$

- **平移型 frame**（$k\mapsto\varphi_k$）下 $k$ 与 $\varphi_k$ **一一对应**（$\mathbb Z\cong$ 平移群），所以「第二位就是 frame」在这层成立；
- **仿射型 frame**（$x\mapsto ax+b$）下第二位要变成一对 $(a,b)$，且 frame 必须**作用**在读数上，不能再只当计数器；
- **区间形态**（半开/闭）与**数制注记**（1-based 供 `lowbit` 用）**根本没有「第二位」可放**——元组装不下整套 frame 数据。

**仿射型 frame 速查**：$\varphi(x)=ax+b$；$a\ne1$ 时它不只挪零刻度，还换了**单位**。

| 项 | 平移型（$a=1$） | 仿射型（$a\ne1$） |
|---|---|---|
| 参数 | 一个 $k$ | 一对 $(a,b)$，$a>0$ |
| 群律 | $\varphi_k\circ\varphi_j=\varphi_{k+j}$（**交换**） | $(a,b)\circ(c,d)=(ac,\ ad+b)$（**非交换**） |
| 归一 | $\rho(v,k)=v-k$ | $\rho\big(v,(a,b)\big)=\varphi^{-1}(v)=(v-b)/a$ |
| 现实来源 | 0/1-based、闭/半开 | 步长与单位（字节↔字）、chunk（$a=B$）、行主序线性化 $i\cdot W+j$、反向遍历（$a=-1,\ b=n-1$） |
| 代价 | 直和可裂，元组第二位够用 | 直和消失，必须背一个 frame 元素；数制算子（`%`/`lowbit`/`÷2`）与单位纠缠 |

变量命名约定（写代码时直接用）：

- 位置（Pos）：`p, q`（点）、`l, r`（frame 端点）、`x, y` 或 `i, j`（格点 / 矩阵格）
- 位移与长度（Vec）：`len, d, gap, w, step`；位移向量：`dx, dy` / `dirs`
- DP 状态：`i, j` 保留，但**必须注释声明它是前缀长度（Vec）**（样板：`Dynamic Programming Indexing` 的 `// handle 0-base index(centralized)`）
- 一行注释协议：`// [l,r) 半开`、`// pos ← len + offset(frame)`、`// 1-based (frame index 1)`

## 7. 运算签名（合法的只有这几条）

| 运算 | 签名 | 库里实例 |
|---|---|---|
| 差 $\Delta$ | Pos × Pos → **Vec** | `r - l`、`j - i` |
| 平移 $+$ | Pos × Vec → **Pos** | `(x+dx, y+dy)`、`mid = l + (r-l)/2`、`i += lowbit(i)` |
| 线性 $+,\cdot$ | Vec × Vec → Vec；$\mathbb Z\times$Vec → Vec | 前缀和/差分、`(a-b)%mod` |
| 仿射组合 | Posⁿ → Pos（$\sum\lambda_i=1$） | 首尾双指针相遇、加权平均 |
| 归一 $\rho$ | (Pos, Frame) → Vec | `[i-1]` to 0-based |
| 数制算子 $f_\varphi$ | 只能共轭出现：$\varphi\circ f_0\circ\varphi^{-1}$ | `÷2`（写成距离式）、`%n`、`lowbit`、`r*n+c` |
| frame 声明 | `[l,r)` / `[l,r]` → $len$ | `r-l` / `r-l+1` |

## 8. 工作流（写代码七步）

- **S0 声明 frame（一处）**：区间形态（半开 / 闭）+ 编号基准（0 / 1）。整个函数只允许一处声明。
- **S1 贴类型**：每个变量注释成 Pos / Vec / Frame。
- **S2 只做合法组合**：Δ、+、仿射组合、线性组合。
- **S3 边界写成语义正确的一侧**：Pos 范围 `0<=x<rs`，或 Vec 不等式 `i+len<=n`；**禁止** `i < n-len+1` 这种混合式。
- **S4 数制算子先停**：`÷2 % lowbit r*n+c` 出现时，写出它绑哪个 frame；`÷2` 一律距离式（`l+(r-l)/2`）。
- **S5 追溯 `±1`**：每个 `±1` 必须能指回 S0 的那条 frame，并在注释里写出来。
- **S6 返回值声明语义**：index（Pos）/ length（Vec）/ count（Vec+1）。
- **S7 收尾自检**：循环上界是 Pos 常量（[[Looper Design Normal Form]]）；本轮 frame 与下一轮一致（[[Loop Invariant Principle]]）。

**默认策略：单 frame 全程计算 + 出口一次 ρ**（2026-11-06 验证）

- 做法：S0 声明**唯一**的 frame → 全程所有量（位置与距离）都用该 frame 的**读数**做普通整数运算 → 只在出口/边界换回。
- 自洽性（已验证）：$\varphi(p+d)=\varphi(p)+a\,d$ ⟹ 只要**距离也按同一 frame 的单位存**（即存 $a\cdot d$），`pos + dis` 就是普通加法。
- 拉回只有两种：
  - **距离 / 长度**：平移型下差的读数**与基准无关**，根本不用拉回；仿射型下只差一次整体单位换算（$\times a$）。
  - **位置**：一次 $\rho$（$v\mapsto(v-b)/a$）。
- **唯一例外**：数制算子（`÷2` / `%` / `lowbit` / `r*n+c`）不因单一 frame 而变自由——它们在**哪个 frame 里合法是固定的**（`lowbit` 只在 1-based；取半在仿射 frame 下必须共轭）。它们是「局部共轭一次，再回主 frame」。
- 不因单 frame 而消失的还有两件事：**区间形态**（半开 `r-l` / 闭 `r-l+1`）与 **count vs length**（rank 1 / rank 0）—— 靠声明，不靠拉回。
- 样板：`C++ algorithm start up`（`// input 1-index -> 0-index` … `// output 0-index -> 1-index`）就是这个结构。
- 代价：frame 从类型里消失、只活在文档与命名里 ⟹ 必须**一处声明**（N5），否则退化成隐性约定。

## 9. 向量空间读法 + 练习

四类题族的读法（把 §2b 落到向量空间）：

- **网格 BFS/DFS**：序号空间 $=\mathbb Z^2$ 格点（Pos）；位移空间 $=\mathbb Z^2$（Vec），四向就是基向量 $\pm e_1,\pm e_2$——库里就是 `dirs`。邻居 `p+v` ∈ Pos×Vec；边界是 **Pos 落在半开区间** `[0,rs)×[0,cs)`；`rs,cs` 属 Vec 侧，只许出现在 frame 里。
- **矩阵旋转/翻转**：$D_4$ 的 8 个元素是 **Pos 上的仿射自同构**：`rot90: (i,j)↦(j, n-1-i)`、`flipH: (i,j)↦(i, n-1-j)`；每个 = 一次线性部分 + 一次平移（`n-1` 即「半圈」）。原地交换 = 写出这些元素在格点集上的**轨道分解**。与 frame 无关 ⟹ 可安全共轭。
- **螺旋 / Z 字形**：四边界 = 闭 frame 的四条边；`len = n-l-1` 是位置→距离；bug 教训 = 上界必须是 Pos 常量。
- **反折 / 回文 / 反转**：`i ↦ n-1-i` 是仿射（线性部分 $-1$，平移 $n-1$）；跨度 `n-1` 属 Vec。「两次反射 = 一次平移」正是 [[Matrix-based Simulation Problem]] 那句「两次镜像反射抵消旋转」的向量空间解释。
- **DP / 背包**：状态 = 前缀长度（Vec 带 origin），数组下标 = Pos，`[i-1]` = ρ；`300 LIS` 是忘记 ρ 的典型。
- **二分 / 滑窗**：`[l,r)` 的 `r-l` 是 length，`[l,r]` 的 `r-l+1` 是 count，差 1 = 基准号。

练习（答案紧跟，先自己判类型）：

1. `r - p.size() + 1` 里的 `+1` 从哪来？→ 闭 frame：窗口是 `[r-len+1, r]`，`len = r-(r-len+1)+1`；换到半开就是 `[r+1-len, r+1)`，`+1` 消失。
2. `m = (l+r)/2` 改成规范式？→ `l + (r-l)/2`。前者是 Pos+Pos（需原点）且 `l+r` 溢出；后者全程 Vec。
3. `(i,j) ↦ (n-1-j, i)` 是 $D_4$ 的哪个元素？→ `rot90` 的逆（因为 `rot90 = (i,j)↦(j, n-1-i)`）。
4. `visited(n+1, 0)` 的 frame index？→ 1（编号从 1 起，`vis[0]` 是不用的哨兵）。
5. `(i+1) % n` 属哪类？→ 数制算子（`%`），必须声明模数与自己选的代表元系；环上距离另需 circular norm `min(d, n-d)`。
6. `index = r*n + c` 怎么规范？→ 数制算子（n 进制商余）；只用于二维 ↔ 一维的**双向换算**，禁止拿它当距离做加减。
7. `dp[i]` 与 `a[i-1]` 的关系？→ `dp` 的 `i` 是长度（Vec），`a` 的下标是位置（Pos），差 1 就是 ρ。
8. `59` 的 `j < j + len` 用类型语言怎么解释？→ 上界是「动点 + 距离」，随迭代变化 ⟹ 不是 Pos 常量，违反 [[Looper Design Normal Form]]；修法 `edge = j + len` 冻结成 Pos。

### 9b. 题目对这套代数的要求（从库里原文反推）+ 8 个直观例子

**要求清单**——每条锚在库里的原文上，这就是代数必须提供的运算面：

| # | 出处（file:line） | 对代数的要求 |
|---|---|---|
| R1 | `Template of Fixed Window:21,29` `r - p.size() + 1` | Pos 与 Vec 分型；「距离 → 位置」有唯一换算 |
| R2 | `Template of Sliding Window:48` `r - l + 1` | 区间 frame 可变（半开 / 闭），长度由 frame 推出 |
| R3 | `Lower Bound:8-11`、`Upper Bound:11` `while(l<r)`、`m=l+(r-l)/2` | Pos+Vec→Pos（平移）与仿射组合（½,½）要闭合 |
| R4 | `Dynamic Programming Indexing:14` `b[j-1]`、`121 Stock:62` `prices[i-1]` | 「长度型下标」与「位置型下标」之间有固定 ρ |
| R5 | `Dual Sequence DP:6,14`「Index of DP is prefix length」+ `A[0:i]` | 状态量本身可以是长度（Vec），并允许切片 |
| R6 | `DFS Template`（网格版）、`200. Number of Islands:21,27-29` | 位移向量（基的线性组合）+ Pos 的区间判定 |
| R7 | `Matrix-based Simulation Problem` §1、`59:40` | Pos 上的**仿射自同构**（D₄）可表达 |
| R8 | `59. Spiral Matrix II:72` `j < j + len`（作者自注「broke Loop Invariant」） | 上界必须是**不随时间变的 Pos** |
| R9 | `Template of BFS with Cycles:8`「visited uses 1-based index!!!」、`lowbit` | 数制算子必须绑定 frame；0 是奇点 |
| R10 | `Monotonic Stack:26,32`「elements are **Index**」「按 index 写答案」 | 要区分「元素的值」与「元素的位置」（值不在代数里） |
| R11 | `Pre-condition Check:14` `limit = size()-3; i<=limit` | 边界可用「长度表达式」写，与 pos 式等价 |
| R12 | `Binary Search:3-4`（bool vs index）+ 滑窗 count | 返回值三态：index / length / count（rank 1） |

**8 个直观例子**

**例 1｜二分：`r` 从不指向元素（半开 frame）**——`Lower Bound:8-11`
`l,r` 是 Pos；`r-l` 是 len（Vec）；`m = l + ½(r-l)` 是仿射组合。直观点：**循环每轮把 `len` 减半，`len=0` 即停**——所谓「不变式」就是 `len = r - l` 这条等式每轮都成立。

**例 2｜固定滑窗的 `+1` 从哪来**——`Template of Fixed Window:21,29`
闭 frame `[l,r]` 的 `len = r-l+1` ⟹ `l = r-len+1`。直观点：那个 `+1` 是**闭 frame 的换算常数**；写成 `pos_from_len(r, len, closed)` 就没有坑，换半开写成 `[r+1-len, r+1)` 它自己会消失。

**例 3｜DP 的两种下标**——`Dynamic Programming Indexing:14`、`121 Stock:62`
`dp[i]` 的 `i` 是**长度**（Vec，带原点 0）；`a[i-1]` 是**位置**（Pos）；两者只靠 ρ 连接。直观点：忘掉 ρ，就写出 `300 LIS` 那种「1-based 公式压在 0-based 数组上」。

**例 4｜网格 BFS：位置 + 位移**——`DFS Template`、`200:21,27-29`
Pos ∈ ℤ²；`dirs = {±e₁, ±e₂}`（Vec 的基）；邻居 `p + v`；边界 = Pos ∈ `[0,rs)×[0,cs)`。直观点：`rs,cs` 是长度，只以 **frame 端点** 的身份进判定；拿它去和 `x` 相加减就是类型错。

**例 5｜旋转/翻转 = D₄ 的仿射自同构**——`Matrix-based Simulation Problem` §1、`59:40`
`(i,j) → (j, n-1-i)` = 线性部分（换轴 + 反号）+ 平移 `n-1`。已验证：**旋转保持任意两点的距离** ✓；`flipH ∘ flipV = rot180` ✓（正是库里那句「两次镜像反射抵消旋转」）。直观点：`n-1` 是跨度（距离），那个 `-1` 是 rank 痕迹；Δ 不变 ⟹ 与 frame 无关，可以放心共轭。

**例 6｜螺旋的崩点：不是写法问题，是类型问题**——`59:39-77`
`j < j + len` 的上界 = 动点 + 距离，随迭代变 ⟹ 不是 Pos 常量（作者自注「broke [[Loop Invariant Principle]]」）；修法 `edge = j + len` 冻结成 Pos。

**例 7｜树状数组为什么必须 1-based**——`Template of BFS with Cycles:8`（声明样板）+ `lowbit`
`lowbit` 是数制算子，`lowbit(0) = 0` 是奇点 ⟹ 它只在 1-based frame 有定义 ⟹ 写法 `f_φ = φ∘f₀∘φ⁻¹`（φ = `x ↦ x+1`）。直观点：**不是习惯，是 frame 依赖**。

**例 8｜同一个 `+1` 的四种身份（收束）**

| 出处 | `+1` 的身份 |
|---|---|
| `r - len + 1`（Fixed Window） | 闭 frame 的换算常数 |
| `a[i-1]`（DP Indexing） | 长度 → 位置的 ρ |
| `lowbit` / Fenwick | 数制算子的 frame 平移 |
| `n-1-i`（D₄） | 群作用里的平移部分 |

⟹ 直观认识：这个代数只有**三件东西**（Pos / Vec / Frame）和**五条运算**（Δ、+、仿射组合、ρ、共轭）。

## 10. 结语 / 下一步（待裁决）

- [ ] 本卡的 7 条规范是否接受？接受哪几条、哪条要改。
- [ ] 病灶 1–4 是**代码/伪码修订**（要不要我改，改哪些）。
- [ ] 缺口 5：四张空壳卡（Prefix Sum / Fenwick / Segment Tree / Sparse Table）是否按本卡写正文。
- [ ] 是否新建一张 library 卡 `Index–Distance Normal Form`（把 §2 + §3 收进正式体裁）。
- [x] 那条「1-Index（大写 I）」悬挂链：已改成小写 `1-index`，G3 转绿（2026-11-06）。
- [ ] root 队列现在 2 篇（`Well Define` / `Conjugate`，都是你的，我没动），`triage` 要不要走。
