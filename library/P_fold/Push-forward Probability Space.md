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

### 类型：输入 → 输出

| 符号 | 类型 | 输入 | 输出 |
|---|---|---|---|
| $X$ | 可测映射 | $\omega\in\Omega$ | $X(\omega)\in\mathbb R^n$ |
| $P$ | 测度（**集合函数**） | $A\in\mathcal F$ | $P(A)\in[0,1]$ |
| $P_X$ | 测度（**集合函数**） | $B\in\mathcal B(\mathbb R^n)$ | $P_X(B)\in[0,1]$ |
| $h$ | 可测函数（**点函数**） | $x\in\mathbb R^n$ | $h(x)\in\mathbb R$ |
| $h\circ X$ | 可测函数（**点函数**） | $\omega\in\Omega$ | $h\big(X(\omega)\big)\in\mathbb R$ |
| $X^{-1}$ | 集合运算 | $B\subseteq\mathbb R^n$ | $X^{-1}(B)\subseteq\Omega$ |
| $X_*$ | 测度搬运 | $\Omega$ 上的测度 $\mu$ | $\mathbb R^n$ 上的测度 $X_*\mu$ |
| $\langle h,\mu\rangle$ | 配对 | $(h,\mu)$ | $\int h\,\mathrm d\mu\in\mathbb R$ |

四类对象不能互换：$P$ 与 $P_X$ **吃集合**，$h$ 与 $h\circ X$ **吃点**，$X^{-1}$ **吃集合吐出集合**，$\langle\cdot,\cdot\rangle$ **吃函数与测度吐出数**。

### 复合的方向

$$
h\circ X:\qquad \omega\ \xrightarrow{\ X\ }\ X(\omega)\ \xrightarrow{\ h\ }\ h\big(X(\omega)\big)
$$

$\circ$ 右边先作用，读法从右往左：先 $X$，再 $h$。复合结果的**定义域是 $\Omega$**，所以它是**拉回**——把 $\mathbb R^n$ 上的函数搬回 $\Omega$。

$$
P_X=P\circ X^{-1}:\qquad B\ \xrightarrow{\ X^{-1}\ }\ X^{-1}(B)\ \xrightarrow{\ P\ }\ P\big(X^{-1}(B)\big)
$$

这里 $X^{-1}$ 先把集合从 $\mathbb R^n$ **拉回** $\Omega$，$P$ 再在 $\Omega$ 上计量；但复合结果的**定义域是 $\mathcal B(\mathbb R^n)$**，所以整体是**推前**。

**判据：看复合结果的定义域。**

| 复合 | 定义域 | 性质 |
|---|---|---|
| $h\circ X$ | $\Omega$ | 拉回 |
| $P\circ X^{-1}$ | $\mathcal B(\mathbb R^n)$ | 推前 |

**"复合的先后"与"推前／拉回"是两件事**：前者是书写顺序（右先左后），后者是定义域搬到了哪一边。$P\circ X^{-1}$ 里 $X^{-1}$ 写在右边、却正是把集合往外拉——不要用书写顺序去判方向。

### 三个记号陷阱

1. $X^{-1}(B)$ 是**原像**，不是反函数：$X$ 一般不可逆，点上的 $X^{-1}$ 根本不存在。
2. $P(B)$ 无意义（$B\subseteq\mathbb R^n$ 不在 $\mathcal F$ 里）；$P_X(A)$ 同理。两个测度的定义域不同，不能混用。
3. $h$ 的定义域是 $\mathbb R^n$，不是 $\Omega$；要在 $\Omega$ 上使用它，必须先复合 $X$。

拉回与推前由**伴随恒等式**绑定：

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

**参照测度是这一步的隐藏条件**：推前只给出测度，密度要等选定 $\lambda^n$ 才存在；$P_X$ 若是原子测度（如 $\mathbf 1_A$ 的情形），它关于 $\lambda$ 的密度就不存在。

### 函子性

$$
(g\circ X)_*P=g_*\,(X_*P).
$$

推前可以逐段做，不必回到 $\Omega$——"求 $g(X)$ 的分布"就是这条式子。

## 例子：单位正方形

**舞台.** $\Omega=[0,1]^2$，$\mathcal F=\mathcal B([0,1]^2)$，$P=$ 面积测度，$\omega=(\omega_1,\omega_2)$。

**1. 恒等映射（校准）.** $(X,Y)(\omega)=(\omega_1,\omega_2)$。则 $P_{(X,Y)}=\lambda^2=P$：推前不是换空间，而是把同一个测度搬过去；恒等映射下两个空间重合。

**2. 一个非单射的映射 $\mathbf 1_A$.**

先定义事件

$$
A=\{\omega\in\Omega:\ \omega_1>\omega_2\}\qquad(\text{下三角，面积 }\tfrac12).
$$

**定义（指示函数）**：

$$
\mathbf 1_A(\omega)=
\begin{cases}
1, & \omega\in A,\\[2pt]
0, & \omega\notin A .
\end{cases}
$$

三种写法是同一件事：

$$
\mathbf 1_A(\omega)=\mathbf 1\{\omega_1>\omega_2\}=\mathbf 1_{\{\omega_1>\omega_2\}}(\omega).
$$

逐点看：

| $\omega$ | $\omega_1$ | $\omega_2$ | $\omega\in A$? | $\mathbf 1_A(\omega)$ |
|---|---|---|---|---|
| $(0.9,\ 0.1)$ | 0.9 | 0.1 | 是 | **1** |
| $(0.4,\ 0.3)$ | 0.4 | 0.3 | 是 | **1** |
| $(0.2,\ 0.7)$ | 0.2 | 0.7 | 否 | **0** |
| $(0.5,\ 0.5)$ | 0.5 | 0.5 | 否（"大于"不含等号） | **0** |

对角线 $\{\omega_1=\omega_2\}$ 落在 0 那一支：它是零测集，不影响任何概率，但属于定义的一部分，不能删。

**为什么它自动是随机变量**：像空间只有 $\{0,1\}$，是离散集，任何子集都可测；所以只要"属于哪个集合"说得清，指示函数就可测。

拉回（集合层）——由定义直接读出，不需要计算：

$$
\mathbf 1_A^{-1}(\{1\})=A,\qquad
\mathbf 1_A^{-1}(\{0\})=A^{c},\qquad
\sigma(\mathbf 1_A)=\{\varnothing,\ A,\ A^{c},\ \Omega\}.
$$

推前（测度层）：

$$
P_{\mathbf 1_A}(\{1\})=P(A)=\tfrac12,\qquad
P_{\mathbf 1_A}(\{0\})=P(A^{c})=\tfrac12 .
$$

丢掉的东西：$A$ 是整块三角形（连续多个 $\omega$），在推前空间里被压成一个点 $1$——这就是"商"的具体形状。

**3. 伴随校验.** 取 $h:\{0,1\}\to\mathbb R$，$h(u)=u$：

$$
\int_{\mathbb R} h\,\mathrm dP_{\mathbf 1_A}
=0\cdot\tfrac12+1\cdot\tfrac12=\tfrac12
=P(A)=\int_{\Omega}\bigl(h\circ\mathbf 1_A\bigr)\,\mathrm dP .
$$

**4. 二次推前.** $Z=X+Y=(+\circ(X,Y))$，故 $P_Z=+_*(\lambda^2)$，其密度为 $1-\lvert z-1\rvert$ 于 $(0,2)$。

$$
\int_{\mathbb R} z\,\mathrm dP_Z=1=\int_{\Omega}(\omega_1+\omega_2)\,\mathrm dP .
$$

**卷积就是加法映射的推前**；而上面这个期望，用右边（原空间）算即可，不必先把 $P_Z$ 的密度求出来——这正是伴随恒等式的作用。

---

## **Related**

[[Probability Spaces]]: 本页展开它最后一句——随机变量把测度推前到哪里。
[[Random Variable]]: $X$ 的可测性定义在那篇；本页只用"可测"这一个词。
[[Index of Probability]]: 上位；本站六个站点的编号在该页。
