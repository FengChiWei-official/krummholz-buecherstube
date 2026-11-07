---
aliases:
---

## Definition

给定概率空间 $(\Omega,\mathcal F,P)$ 与可测映射（随机变量）

$$X:\Omega\to\mathbb R^n,$$

**推前测度**（pushforward measure）定义为

$$P_X:=P\circ X^{-1},\qquad P_X(B)=P\big(X^{-1}(B)\big)=P(X\in B),\quad B\in\mathcal B(\mathbb R^n).$$

于是

$$\big(\mathbb R^n,\ \mathcal B(\mathbb R^n),\ P_X\big)$$

本身是一个概率空间——它就是 $X$ 的**分布**（law）。

它值得单独命名，是因为**在它里面 $X$ 不再是映射，而是坐标本身**：原空间里 $X$ 是"从 $\omega$ 到数"的通道，推前空间里"样本"直接就是数。

### 两个方向

| 方向 | 对象 | 定义 | 需要逆映射吗 |
|---|---|---|---|
| **拉回** | 事件、函数 | $B\mapsto X^{-1}(B)$；$h\mapsto h\circ X$ | 不需要 |
| **推前** | 测度 | $P_X=P\circ X^{-1}$ | 不需要 |

两者由**伴随恒等式**绑定：

$$
\int_{\mathbb R^n} h\,\mathrm dP_X=\int_{\Omega}(h\circ X)\,\mathrm dP .
$$

这条恒等式同时是换元公式与 LOTUS 的测度层形式：左边在新空间积分，右边把函数拉回原空间再积分。

### 不是同态

同态要求保持代数结构；$\Omega$ 上没有加法、乘法或序可保。$X$ 只要求**可测**——"保持结构"是这个 $X$ 的偶然性质（例如 $X=2\,\mathrm{id}$），不是随机变量的定义性质。

### 它丢掉了什么

$X$ 一般不是单射：纤维 $X^{-1}(x)$ 上的所有 $\omega$ 被压成一个点。因此推前空间是原空间对 $\sigma(X)$ 的**商**——它只保留 $X$ 能分辨的信息。

### 为什么推到 $\mathbb R^n$

因为 $\mathbb R^n$ 有 $\Omega$ 没有的三件东西，而它们正好对应三类概率对象：

| $\mathbb R^n$ 的结构 | 由此才有的对象 |
|---|---|
| 序 | 分布函数 $F_X(x)=P_X\big((-\infty,x]\big)$ |
| Lebesgue 测度 | 密度 $f_X=\mathrm dP_X/\mathrm d\lambda^n$（要求 $P_X\ll\lambda^n$） |
| 加法 | $X+Y$、卷积 |

**参照测度是这一步的隐藏条件**：推前只给出测度，密度要等选定 $\lambda^n$ 才存在；$P_X$ 若是原子测度（如 $U$ 的情形），它关于 $\lambda$ 的密度就不存在。

### 函子性

$$
(g\circ X)_*P=g_*\,(X_*P).
$$

推前可以逐段做，不必回到 $\Omega$——"求 $g(X)$ 的分布"就是这条式子。

## 例子：单位正方形

**舞台.** $\Omega=[0,1]^2$，$\mathcal F=\mathcal B([0,1]^2)$，$P=$ 面积测度，$\omega=(\omega_1,\omega_2)$。

**1. 恒等映射（校准）.** $(X,Y)(\omega)=(\omega_1,\omega_2)$。则 $P_{(X,Y)}=\lambda^2=P$：推前不是换空间，而是把同一个测度搬过去；恒等映射下两个空间重合。

**2. 非单射的映射.** $U(\omega)=\mathbf 1\{\omega_1>\omega_2\}$，记 $A=\{\omega_1>\omega_2\}$。

拉回（集合层）：

$$
U^{-1}(\{1\})=A,\qquad U^{-1}(\{0\})=A^{c},\qquad \sigma(U)=\{\varnothing,\ A,\ A^{c},\ \Omega\}.
$$

推前（测度层）：

$$
P_U(\{1\})=P(A)=\tfrac12,\qquad P_U(\{0\})=\tfrac12 .
$$

丢掉的东西：$A$ 是整块三角形（连续多个 $\omega$），被压成一个点——这就是"商"的具体形状。

**3. 伴随校验.** 取 $h(u)=u$：

$$
\int_{\mathbb R} h\,\mathrm dP_U=0\cdot\tfrac12+1\cdot\tfrac12=\tfrac12
=P(A)=\int_{\Omega}(h\circ U)\,\mathrm dP .
$$

**4. 二次推前.** $Z=X+Y=(+\circ(X,Y))$，故 $P_Z=+_*(\lambda^2)$，其密度为 $1-\lvert z-1\rvert$ 于 $(0,2)$。

$$
\int_{\mathbb R} z\,\mathrm dP_Z=1=\int_{\Omega}(\omega_1+\omega_2)\,\mathrm dP .
$$

**卷积就是加法映射的推前**；而上面这个期望，用右边（原空间）算即可，不必先把 $P_Z$ 的密度求出来——这正是伴随恒等式的作用。

---

## **Related**

[[Probability Spaces]]: 本页展开它最后一句——随机变量把测度推前到哪里。
[[Random Variables]]: $X$ 的可测性定义在那篇；本页只用"可测"这一个词。
[[Index of Probability]]: 上位；本站六个站点的编号在该页。
