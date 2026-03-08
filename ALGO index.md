---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text

> [!summary] 算法知识体系 MOC (完全体)
> 建立对算法版图的全局掌控感。识别题型、映射数据结构、制定解题策略。

## 🧱 1. 基础功底：模拟与字符串 (Basic & String)
- [[模拟算法|Simulation]]：按题意办事 $\rightarrow$ *考察代码掌控力。常见范围：**矩阵遍历** (螺旋/对角线)、**大数运算** (加减乘除)、**日期/时间推算**、**复杂格式化** (IP解析/提取数字)*。
- [[字符串基础|Basic String]]：基础字符操作 $\rightarrow$ *回文判定/反转 (双指针)、字符频次统计 (Hash数组)、单词拆分*。
- [[字符串匹配]]：模式查找 $\rightarrow$ *$O(N+M)$ 高效匹配 (KMP 算法)、字符串哈希 (Rabin-Karp)*。

## 🧩 2. 线性结构：区间与序列 (Linear & Intervals)
- [[双指针|Two Pointers]]：首尾或快慢指针 $\rightarrow$ *数组去重、两数之和、链表找环*。
- [[滑动窗口]]：同向双指针 $\rightarrow$ *找满足条件的最长/最短连续子串、子数组*。
- [[单调栈]]：栈内元素单调 $\rightarrow$ *$O(n)$ 找左右两边第一个比自己大/小的数* (如：接雨水)。
- [[区间处理]]：排序贪心 $\rightarrow$ *求最多不重叠区间 (按右端点排)、合并重叠区间 (按左端点排)*。
- [[前缀和与差分]]：预处理 $\rightarrow$ *$O(1)$ 查询区间和，或 $O(1)$ 区间整体增减*。

## 🗺️ 3. 搜索与组合数学 (Search & Math)
- [[DFS与BFS]]：基础搜索 $\rightarrow$ *DFS 走到底 (递归)，BFS 逐层扩 (无权最短路)*。
- [[回溯算法|Backtracking]]：DFS进阶 $\rightarrow$ *选它 $\rightarrow$ 递归 $\rightarrow$ 撤销选择* (解决所有组合、子集、数独问题)。
- [[排列与组合|Permutation & Combination]]：数学与生成 $\rightarrow$ *全排列生成、求「下一个排列」(找拐点翻转)、组合数 $C_n^m$ 计算*。
- [[双向BFS]]：起点终点同时扩散 $\rightarrow$ *大空间搜索快速相遇，防指数级爆炸*。

## 🕸️ 4. 图论与树 (Graph Theory & Trees)
- **图的基础与连通性**：
  - [[并查集|Union-Find]]：找祖先+路径压缩 $\rightarrow$ *动态判断连通性、求连通分量*。
  - [[拓扑排序|Topological Sort]]：利用入度 $\rightarrow$ *解决有先后依赖顺序的任务编排* (如：课程表)。
  - [[二分图|Bipartite Graph]]：染色法 $\rightarrow$ *判断图是否能分成互不内部交卷的两组*。
- **带权图经典算法**：
  - [[最短路径|Shortest Path]]：Dijkstra (单源非负权)、Bellman-Ford / SPFA (含负权)、Floyd (多源)。
  - [[最小生成树|MST]]：Kruskal (边排序+并查集)、Prim (点扩展) $\rightarrow$ *用最低成本连通所有点*。
- **高级树形结构**：
  - [[字典树|Trie]]：多叉树结构 $\rightarrow$ *高效处理字符串前缀匹配*。
  - [[线段树与树状数组]]：$\rightarrow$ *解决单点修改 + 区间查询的高性能需求*。

## 🧠 5. 最优化与进阶思维 (Optimization & Advanced)
- [[动态规划|DP]]：状态转移 $\rightarrow$ *背包问题、打家劫舍、最长递增子序列 (LIS)*。
- [[二分答案|Binary Search on Answer]]：在答案值域里猜 $\rightarrow$ *解决“最小化最大值”或“最大化最小值”*。
- [[堆|Heap]]：优先队列 $\rightarrow$ *动态维护最值，解决 Top K 问题、合并 K 个有序链表*。
- [[状态压缩|Bitmask]]：二进制位代表开关 $\rightarrow$ *解决 $N \le 20$ 的小规模搜索/状压 DP*。*
---

## Thoughts
[[算法决策树]]