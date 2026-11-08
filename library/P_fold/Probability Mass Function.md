---
aliases:
  - PMF
---

## Definition

$$
p_X(x):=P_X(\{x\})
$$

即 $P_X$ **相对计数测度 $\#$ 的密度**：$P_X=\sum_xp_X(x)\,\delta_x$，支撑至多可数。

**类型（输入 → 输出）**：$x\mapsto$ 一个数。

| 项 | 内容 |
|---|---|
| 输入 | 点 $x$ |
| 输出 | 数 $p_X(x)\in[0,1]$ |
| 参照测度 | **计数测度 $\#$**（不是 Lebesgue） |
| 与 PDF | 同一个测度在不同参照下的分量；离散测度关于 $\lambda$ **没有**密度 |

性质：

1. $p_X\ge0$；
2. $\sum_xp_X(x)=1$；
3. $P_X(B)=\sum_{x\in B}p_X(x)$。

---
## **Related**

[[Probability Density Function|PDF]]: 连续型的对应物；参照测度从 $\#$ 换成 $\lambda$。
[[Probability measure]]: pmf 是测度在计数测度下的分量。
[[Cumulative Distribution Function|CDF]]: $F_X(x)=\sum_{t\le x}p_X(t)$，阶梯状，跳高即 $p_X(x)$。
