---
aliases:
---

## Definition

期望是**测度上的泛函**：把随机变量映成一个数。

$$
E[X]:=\int_{\Omega}X\,\mathrm dP
$$

同一个数也可以写成对推前测度的积分：

$$
E[X]=\int_{\mathbb R}x\,\mathrm dP_X(x)
$$

**类型（输入 → 输出）**：随机变量 $\mapsto$ 数。

| 项 | 内容 |
|---|---|
| 输入 | 可测函数（随机变量）$g(X)$ |
| 输出 | 数 $E[g(X)]\in\mathbb R$（可能不存在） |
| 参照测度 | **不需要** |
| 身份 | 测度 $P_X$ 作为线性泛函作用在 $g$ 上：$g\mapsto\int g\,\mathrm dP_X$ |



---

## **Related**

[[Push-forward Probability Space]]: LOTUS 就是那篇的伴随恒等式取 $h=g$。
[[Probability Spaces]]: 期望的测度层定义（测度作为泛函）在那篇收尾。
[[Random Variable]]: $g(X)$ 仍是可测映射，可测性的依据在那篇。
[[Index of Probability]]: 概率簇的上位；本卡的登记边在 Raw Index of Probability 的「技术层」。
[[LOTUS]]: 计算方法