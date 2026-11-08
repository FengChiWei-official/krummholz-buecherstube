---
aliases:
  - PDF
---

## Definition

$$
f_X:=\frac{\mathrm dP_X}{\mathrm d\lambda}
$$

前提：$P_X\ll\lambda$（关于 Lebesgue 绝对连续）。它是**测度在参照测度 $\lambda$ 下的分量**——只在选定 $\lambda$ 之后才有意义，并且在零测集上可以任意改动（同一个分布有无数个版本）。

**类型（输入 → 输出）**：$x\in\mathbb R\mapsto$ 一个数。

| 项 | 内容 |
|---|---|
| 输入 | 点 $x$ |
| 输出 | 数 $f_X(x)$，**可以大于 1** |
| 参照测度 | **必须**：Lebesgue $\lambda$ |
| 与 CDF | $f_X=F_X'$（a.e.） |

性质：

1. 非负（a.e.）；
2. $\int_{\mathbb R}f_X\,\mathrm d\lambda=1$；
3. $P_X(B)=\int_Bf_X\,\mathrm d\lambda$。

三个常被说错的地方：

- **$f_X(x)$ 不是概率**，只是"每单位长度的质量"；$U(0,\tfrac12)$ 的密度处处是 $2$。
- **众数是密度的局部极大点**，不是"密度的最高值"。密度可以无界（在端点发散）、可以多峰、可以没有众数。
- **对称 $\Longrightarrow$ 均值 $=$ 中位数 $=$ 对称中心**（若均值存在）；**众数不一定**——对称双峰密度的两个众数都不在中心。

---
## **Related**

[[Cumulative Distribution Function|CDF]]: 它的导数（a.e.）。
[[Probability Mass Function|PMF]]: 同一个测度改用计数测度作参照的分量。
