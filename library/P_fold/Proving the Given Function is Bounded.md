---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Topic: [[Boundedness]] of $f(x) = \frac{x}{1+x^2}$

## 1. Problem Analysis 

- Goal: Prove the function is bounded (有界) on the interval $(-\infty, \infty)$.
- Key Concept: Finding a constant $M$ such that $|f(x)| \le M$.
- Observation: The function is a fraction (分式). Its structure suggests using the AM-GM Inequality (算术-几何平均值不等式).

## 2. Core Strategies (核心策略)

- [[Case Analysis]] (分类讨论): Since AM-GM requires positive terms, we analyze $|f(x)|$ to handle $x < 0$ and $x = 0$.
- [[Reciprocal Transformation ]](倒数变换): Converting the function into a [[Hook Function]] (耐克函数/对勾函数) form: $x + \frac{1}{x}$.
- [[Odd Function Property]] (奇函数性质): Since $f(-x) = -f(x)$, we only need to prove it is bounded for $x \ge 0$.

## 3. Proof Steps (证明步骤)

1. Special Case: If $x = 0$, $f(0) = 0$, which is clearly bounded.
2. General Case ($x \neq 0$):  
    Consider the absolute value $|f(x)| = \frac{|x|}{1+x^2}$.
3. Take the Reciprocal:  
    $$\frac{1}{|f(x)|} = \frac{1+x^2}{|x|} = \frac{1}{|x|} + |x|$$
4. Apply AM-GM Inequality:  
    For $|x| > 0$, according to AM-GM:  
    $$\frac{1}{|x|} + |x| \ge 2\sqrt{\frac{1}{|x|} \cdot |x|} = 2$$
5. Conclusion:  
    Since $\frac{1}{|f(x)|} \ge 2$, it follows that $|f(x)| \le \frac{1}{2}$.  
    The range of the function is $[-\frac{1}{2}, \frac{1}{2}]$, thus it is bounded.
