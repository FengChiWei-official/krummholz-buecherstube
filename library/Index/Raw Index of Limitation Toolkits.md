---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/map
---

## Definition

## Core Concepts

### [[Object -- Identify the form of the limit]]

#### 概论：

不知道做什么的时候，
1. 把无法理解的部分恒等变化（幂指函数）
2. 把整体配凑为乘式
3. 通过技巧把没有手段研究的结构去掉（变限积分）
4. 性态估计，大致了解整体性质
5. 主部提取 A-A = A(1 - 1) = A(\frac{A'}{A} -1)


求解品味：

先化成可以理解/分析的未定式+普通极限
简单分式 先看条件，然后用等价无穷小/重要极限
不能适用，先考虑简单的主部提取
再次洛必达， 或者是变限积分

如果有差分或者复合，简单的可以使用taylor（不同类相减）或者mvt（同类相减），
太复杂就要落回主部提取化成主部（相对关系-1）

如果有无穷大，考虑倒代换/主部提取

夹逼准则有特殊的使用场景
1. 已知一个常数下界
2. 可以轻松放缩
3. 周期性
4. 有界性/极限（局部有界）
5. 无穷级数
6. 有界振荡

Reduce into [[Standard Limits]]
[[L'Hospital Rule]] simple fractions to even simpler ones.

### $\lim_n f(x, n)$

[[Case Analysis]]

### Infinitesimals
The first trick is [[Equivalent Infinitesimals]].

The second one is [[Focus on the Dominant]], which derives

Difference of Functions and Compounded Function -> [[Taylor Series]] or [[Mean Value theorem]]
> [[Principle of Reduction]].

or 
1. $\alpha = o(\beta) \to (\alpha + \beta) \~ \beta$
2. $\alpha = o(\beta) \to (\alpha \beta) = o(\beta^2)$

#### **Functions defined by integrals**

the major goal of it is using [[L'Hospital Rule]].
However, most of time you should use [[Taylor Series]] to simplizing it first.

1. $\int_0^x f(t) dt$ ，其中 $\lim_{t \to 0} f(t) = 0$。
2. $\int_0^{h(x)} f(t) dt$ ，其中当 $x \to a$ 时， $h(x) \to 0,  h(x) \ne 0$，而被积函数的极限 $f(t) \to A$（是一个非零常数）。

都可以看成先用泰勒提取主部，然后用洛必达证明等价。





# [[Object -- Determine continuity and discontinuity]]

可能间断点
1. 幂指函数 底数为正数
2. 分母不为0

什么条件下，我们常见结构是无穷大/无穷小

## [[Object -- Investigate the microscopic behavior of the function as x tends to some point]]


单调有界
定义
夹逼准则
局部有界 + 导数（差商） = 局部不等式  [[Raw Index of Inequality Toolkits]]

[[Boundedness]] $\to$ $\lim_{x \to \infty} f(x) = A, A \in \mathbb{R}$



## Key Methods

## Applications

---
## **Related**