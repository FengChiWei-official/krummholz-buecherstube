---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/map
---

## Definition
Limit Strategy organizes solving routes by trigger: rational structure, substitution form, squeeze condition, and exponential conversion.

## 求解品味

### 概论：不知道做什么的时候

1. 把无法理解的部分恒等变化（幂指函数）
2. 把整体配凑为乘式
3. 通过技巧把没有手段研究的结构去掉（变限积分）
4. 性态估计，大致了解整体性质
5. 主部提取 A-A = A(1 - 1) = A(\frac{A'}{A} -1)

### 路线顺序

先化成可以理解/分析的未定式+普通极限
简单分式 先看条件，然后用等价无穷小/重要极限
不能适用，先考虑简单的主部提取
再次洛必达， 或者是变限积分

如果有差分或者复合，简单的可以使用taylor（不同类相减）或者mvt（同类相减），
太复杂就要落回主部提取化成主部（相对关系-1）

如果有无穷大，考虑倒代换/主部提取

Reduce into [[Standard Limits]]
[[L'Hospital Rule]] simple fractions to even simpler ones.

### 夹逼准则的使用场景

1. 已知一个常数下界
2. 可以轻松放缩
3. 周期性
4. 有界性/极限（局部有界）
5. 无穷级数
6. 有界振荡

## Route Selection

- Rational structure dominates: start with Rational Route.
- A power-exponential form appears, or $1^\infty,0^0,\infty^0$: start with Exponential Route.
- Bounds can be established, or monotone-bounded behavior exists: use Bounding Route.
- If the starting point is unclear: begin with Overview Route.

## Core Routes

### Rational Route
[[Rational Limit]]
[[Simplification Rational Limit]]

### Radical Route
[[Radical Normalization for Limit]]
### Exponential Route
[[Power-Exponential Functions Transform]]
[[Definition-of-E-like Limit]]

### logarithm
[[Logarithmic Functions Pattern for Limit]]
### Bounding Route
[[Monotonic Squeezing]]

### Overview Route
[[Links of Solving Limit of Function]]
[[Limit]]

## 特殊技巧

[[Denominator Normalization]] --> [[Radical Normalization]] --> [[Radical Normalization for Limit]]
有些时候可以显式化无穷小，降低求解难度。 让分母方便进一步变形。

[[Simplification Rational Limit]]
[[Power-Exponential Functions Transform]]

## Infinitesimals

The first trick is [[Equivalent Infinitesimals]].

The second one is [[Focus on the Dominant]], which derives

Difference of Functions and Compounded Function -> [[Taylor Series]] or [[Mean Value theorem]]
> [[Principle of Reduction]].

or 
1. $\alpha = o(\beta) \to (\alpha + \beta) \~ \beta$
2. $\alpha = o(\beta) \to (\alpha \beta) = o(\beta^2)$

## Functions defined by integrals

the major goal of it is using [[L'Hospital Rule]].
However, most of time you should use [[Taylor Series]] to simplizing it first.

1. $\int_0^x f(t) dt$ ，其中 $\lim_{t \to 0} f(t) = 0$。
2. $\int_0^{h(x)} f(t) dt$ ，其中当 $x \to a$ 时， $h(x) \to 0,  h(x) \ne 0$，而被积函数的极限 $f(t) \to A$（是一个非零常数）。

都可以看成先用泰勒提取主部，然后用洛必达证明等价。

## $\lim_n f(x, n)$

[[Case Analysis]]

## Typical Order

1. Determine which structural trigger selects the route.
2. Perform local simplification within that route (identity transforms/equivalent infinitesimals/factor extraction).
3. Return to the main limit line for convergence proof or value computation.

---
## **Related**

[[Raw Index of Limit Solving Toolkits]]
[[Index of Limit Properties Toolkits]]
[[Links of Solving Limit of Function]]
[[Index of Math Expressions Pattern]]
