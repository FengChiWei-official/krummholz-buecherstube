---
aliases:
---

## Definition

$P:\mathcal F\to[0,1]$，满足

1. $P(\varnothing)=0$，$P(\Omega)=1$；
2. 对两两不交的可数族 $A_1,A_2,\dots\in\mathcal F$：$P\bigl(\bigcup_kA_k\bigr)=\sum_kP(A_k)$。

即：**集合函数**，归一 + σ-可加。

**类型（输入 → 输出）**：$\mathcal F$ 中的**集合** $\mapsto$ $[0,1]$ 中的**数**。

| 项 | 内容 |
|---|---|
| 输入 | 集合 $A\in\mathcal F$（不是点） |
| 输出 | 数 $P(A)\in[0,1]$ |
| 参照测度 | **不需要**——测度自身不依赖参照，只有密度才需要 |
| 对偶身份 | $h\mapsto\int h\,\mathrm dP$，即有界可测函数空间上的正线性泛函 |

---
## **Related**

[[Probability Spaces]]: 是它的基础之一。
[[Push-forward Probability Space]]: 我们真正有办法了解 measure 的空间。
[[Cumulative Distribution Function|CDF]]: 我们通过它可以完整地表示 measure。
