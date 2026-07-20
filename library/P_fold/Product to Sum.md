---
tags:
  - type/permanent
  - topic/learning
  - attr/concept
  - status/evergreen
---

## 1. Fundamental Definition
The Arithmetic Mean-Geometric Mean (AM-GM) inequality provides an **upper bound for products** in terms of their sums. For a set of positive real numbers $a_1, a_2, \dots, a_n$:

$$\sqrt[n]{\prod_{i=1}^n a_i} \le \frac{\sum_{i=1}^n a_i}{n}$$

Equality holds if and only if $a_1 = a_2 = \dots = a_n$.

### Special Case: The Factorial Bound
By applying the inequality to the set $\{1, 2, \dots, n\}$, we can bound the $n$-th root of the factorial:
*   **Geometric Mean:** $\sqrt[n]{\prod_{i=1}^n i} = \sqrt[n]{n!}$
*   **Arithmetic Mean:** $\frac{\sum_{i=1}^n i}{n} = \frac{n(n+1)}{2n} = \frac{n+1}{2}$
*   **Bound:** $\sqrt[n]{n!} \le \frac{n+1}{2}$, which implies $n! \le \left(\frac{n+1}{2}\right)^n$.

---

## 2. Optimization Techniques
### Type 1: Constrained Product Maximization
**Problem:** Given $\sum_{i=1}^n a_i x_i = C$, find the maximum of $f = \prod_{i=1}^n x_i^{m_i}$.
*   **Strategy:** Utilize the "Method of Undetermined Coefficients" or split the variables to match the ratios of the exponents $m_i$, allowing for the direct application of AM-GM.

### Type 2: The "Substitution of 1" and Term Expansion
This technique is particularly useful for minimizing the sum of reciprocals under a linear constraint.

**Problem:** Given $\sum_{i=1}^n x_i = C$, minimize $f = \sum_{i=1}^n \frac{1}{x_i}$.

**Derivation:**
We multiply the expression by $\frac{\sum x_i}{C}$ (which is 1):

$$
\begin{align}
f &= \frac{1}{C} \left( \sum_{i=1}^n x_i \right) \left( \sum_{j=1}^n \frac{1}{x_j} \right) \\
&= \frac{1}{C} \left( \sum_{i=1}^n \frac{x_i}{x_i} + \sum_{i \neq j} \frac{x_i}{x_j} \right) \\
&= \frac{1}{C} \left( n + \sum_{i < j} \left( \frac{x_i}{x_j} + \frac{x_j}{x_i} \right) \right)
\end{align}
$$

**Insight:**
*   Since $\frac{x_i}{x_j} + \frac{x_j}{x_i} \ge 2$ (by AM-GM), the expression is minimized when $x_i = x_j$ for all $i, j$.
*   At the minimum point ($x_i = \frac{C}{n}$), the value becomes:
    $$f_{min} = \frac{1}{C} \left( n + \frac{n(n-1)}{2} \times 2 \right) = \frac{n^2}{C}$$

---

## 3. Key Takeaways
*   **Constraint Handling:** Always look for ways to introduce the value "1" (via the given constraint) to transform the algebraic structure.
*   **Expansion:** Expanding a product of sums is a powerful way to reveal cross-terms, which are often easily bounded using the basic AM-GM inequality.
*   **Symmetry:** These problems typically achieve their extrema when variables are equal (under symmetric constraints). If the constraints are weighted, adjust the ratios accordingly.
