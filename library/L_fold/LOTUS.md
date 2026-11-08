---
aliases:
---

## Definition

LOTUS 是**期望的计算替代规则**：把"先求 $g(X)$ 的分布、再对它积分"换成"直接对 $X$ 的分布积分"。

它断言的是两个数的相等：

$$
\int_{\mathbb R}g(x)\,\mathrm dP_X(x)=\int_{\Omega}g\bigl(X(\omega)\bigr)\mathrm dP(\omega)
$$

**类型（各符号的输入 → 输出）**：

| 符号 | 类型 | 输入 → 输出 |
|---|---|---|
| $g$ | 映射 | 点 $\mapsto$ 数（定义域 $\mathbb R$） |
| $g\circ X$ | 映射 | 点 $\mapsto$ 数（定义域 $\Omega$） |
| $P_X$ | 测度 | 集合 $\mapsto$ 数 |
| $P$ | 测度 | 集合 $\mapsto$ 数（原空间） |
| 等式两边 | 数 | — |

### LOTUS（无意识统计学家定理）

对任意可测 $g:\mathbb R\to\mathbb R$（$\int\lvert g\rvert\,\mathrm dP_X<\infty$）：

$$
\boxed{\
E[g(X)]=\int_{\mathbb R}g(x)\,\mathrm dP_X(x)=\int_{\Omega}g\bigl(X(\omega)\bigr)\,\mathrm dP(\omega)\
}
$$

**中间项的测度是 $P_X$（$X$ 的分布），不是 $P_{g(X)}$。** 这就是"无意识"三个字的来处：你无意识地把 $g(x)$ 当成被积函数、把 $f_X$ 当成权重，跳过了"先求 $g(X)$ 的分布"这一步——而它是对的。

一句话版本：**要算 $g(X)$ 的期望，只需要 $X$ 的分布；$g(X)$ 自己的分布可以不出现。**

直接推论（全部只用原空间）：

| 想求 | 用 LOTUS |
|---|---|
| $P(A)$ | $E[\mathbf 1_A]=\int_\Omega \mathbf 1_A\,\mathrm dP=P(A)$ |
| $\operatorname{Var}(g)$ | $E[g^2]-\bigl(E[g]\bigr)^2$ |
| $\operatorname{Cov}(g,h)$ | $E[gh]-E[g]\,E[h]$ |
| $E[\text{任意可测表达式}]$ | $\iint \text{那个表达式}\cdot f_{XY}$ |

---
## **Related**

[[Expectation]]: 主要应用场景——LOTUS 把期望的计算搬到原空间。
[[Push-forward Probability Space]]: 本定理就是那篇的伴随恒等式取 $h=g$。
