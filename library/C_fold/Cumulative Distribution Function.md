---
aliases:
  - CDF
---

## Definition

$$
F_X(x):=P_X\bigl((-\infty,x]\bigr)=P(X\le x)
$$

即 [[Push-forward Probability Space|推前测度]] 在一族特殊集合（射线）上的取值，打包成的函数。

**类型（输入 → 输出）**：$x\in\mathbb R\mapsto$ 数 $F_X(x)\in[0,1]$。

| 项 | 内容 |
|---|---|
| 输入 | 点 $x\in\mathbb R$ |
| 输出 | 数（概率） |
| 参照测度 | **不需要**（只用 $\mathbb R$ 的序） |
| 信息量 | $F_X$ 与 $P_X$ 互相唯一决定 |

基础性质：

1. 单调不减；
2. $\lim_{x\to-\infty}F_X(x)=0$，$\lim_{x\to+\infty}F_X(x)=1$；
3. 右连续。

反过来也成立：满足这三条的函数必是某个概率测度的 CDF。所以 CDF 可以当作分布的**完整代表**。

进一步三条：

- **跳跃 = 原子**：$F_X$ 在 $x$ 处的跳跃量等于 $P_X(\{x\})$。
- **导数 = 密度**：当 $P_X\ll\lambda$ 时，$f_X=F_X'$（a.e.）。
- 连续型 $\Longrightarrow$ $F_X$ 处处连续；**反之不成立**（Cantor 分布处处连续却没有密度）。

---
## **Related**

[[Probability measure]]: CDF 是它的完整表示。
[[Push-forward Probability Space]]: CDF 定义在推前空间上，只用序结构。
[[Probability Density Function|PDF]]: CDF 的导数（a.e.）。
