---
aliases:
---

## Definition

$P(A)$ 是**测度在事件上的取值**：一个数。

**类型（输入 → 输出）**：集合 $\mapsto$ 数。

| 项 | 内容 |
|---|---|
| 输入 | 事件 $A\in\mathcal F$，即 $\Omega$ 的子集 |
| 输出 | $P(A)\in[0,1]$ |
| 参照测度 | 不需要 |

例：$A=\{X\le3\}=X^{-1}\bigl((-\infty,3]\bigr)$，所以

$$
P(A)=P\bigl(X^{-1}((-\infty,3])\bigr)=P(X\le3)
$$

——同一个数的两种写法：左边在原空间里指一个集合，右边是推前空间里的一条射线。

---
## **Related**

[[Probability measure]]: 是测度的一个取值。
[[Cumulative Distribution Function|CDF]]: 把"所有射线"的取值打包成函数；射线有序，所以能写成 $F_X$。
