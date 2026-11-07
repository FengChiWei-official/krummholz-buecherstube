## Definition

$$(\Omega,\ \mathcal F,\ P)$$

- $\Omega$ 是**样本空间**，元素 $\omega$ 叫样本点。$\Omega$ 可以是任意集合——数列空间、函数空间、路径空间都行；这正是"先造空间、再把测度推走"的理由。
- $\mathcal F\subseteq 2^{\Omega}$ 是**事件 $\sigma$-代数**：对补、对可数并封闭。其中的元素叫事件。"可测"不是"性质好到可以派发概率"，而是**属于 $\mathcal F$**——这是公理选择，不是性质判断。
- $P:\mathcal F\to[0,1]$ 是**概率测度**（集合函数）：$P(\varnothing)=0$、$P(\Omega)=1$、对互不相交的可数族可加。

随机变量 $X:\Omega\to\mathbb R^{n}$ 是**可测映射**（定义见 [[Random Variables]]）。它同时给出两个方向的作用：

| 方向 | 对象 | 定义 |
|---|---|---|
| **拉回** | 事件、函数 | $B\mapsto X^{-1}(B)$；$h\mapsto h\circ X$ |
| **推前** | 测度 | $P_X := P\circ X^{-1}$，即 $P_X(B)=P(X\in B)$ |

两者由伴随恒等式绑定：

$$
\int_{\mathbb R^n} h\,\mathrm dP_X=\int_{\Omega}(h\circ X)\,\mathrm dP
$$

于是 $(\mathbb R^{n},\ \mathcal B(\mathbb R^{n}),\ P_X)$ 本身是一个概率空间（[[Push-forward Probability Space]]）——它就是 $X$ 的**分布**。在这个空间里 $X$ 不再是映射，而是坐标本身。

这**不是同态**：同态要保持代数结构，而 $\Omega$ 上没有代数结构可保；推前发生在测度层，映射层只是"可测"。

---

## **Related**

[[Random Variables]]: $X$ 的可测性定义在那篇；本页只说到"它把测度推前"为止。
[[Manifold]]: 对照项——流形用**局部图册**把局部搬到 $\mathbb R^n$（要求同胚），推前用**单个整体映射**把测度搬到 $\mathbb R^n$（不要求可逆）。
[[Homomorphism]]: 好好考虑什么不是同态