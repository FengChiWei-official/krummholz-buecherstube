---
aliases:
  - 割线型积分不等式
---

## Definition

$f$ is twice differentiable on $[a,b]$.

[[Concavity]]

$f''$ inherits [[Continuity]] from $f$: continuity is what carries the sign of $f''$ from a point to a neighbourhood.

$$
f\!\left(\frac{a+b}{2}\right) \le \frac{1}{b-a}\int_a^b f(x)\,dx
\qquad \text{iff.} \qquad f''(x) \ge 0
$$

**This conclusion is stronger than the familiar one** ([[Jensen Inequality]]).

$$
f\!\left(\frac{a+b}{2}\right) \le \frac{1}{b-a}\int_a^b f(x)\,dx \le \frac{f(a)+f(b)}{2}
$$

### Proof

[[Expansion in the Integral]]. Expand to the $x^2$ term:

$$
\begin{aligned}
\int_a^b f(x)\,dx
&= \int_a^b \left[ f\!\left(\frac{a+b}{2}\right)
   + f'\!\left(\frac{a+b}{2}\right)\left(x-\frac{a+b}{2}\right)
   + \frac{f''(\xi)}{2}\left(x-\frac{a+b}{2}\right)^2 \right] dx \\
&= \int_a^b f\!\left(\frac{a+b}{2}\right)
   + \frac{f''(\xi)}{2}\left(x-\frac{a+b}{2}\right)^2 dx .
\end{aligned}
$$

The linear term drops out because $x - \frac{a+b}{2}$ is odd about the midpoint; $\xi = \xi(x)$ depends on $x$.

Trivially,

$$
\int_a^b f\!\left(\frac{a+b}{2}\right) + \frac{f''(\xi)}{2}\left(x-\frac{a+b}{2}\right)^2 dx
\ge \int_a^b f\!\left(\frac{a+b}{2}\right) dx .
$$

### Necessity

[[a Proof by Contradiction]]

Let $x = m$, where $f''(m) \le 0$. [[Continuity]], [[Limit]]'s property $\Rightarrow$ $x \in u(m, l)$, $f''(x) \le 0$.

Trivially, we can get

$$
f\!\left(\frac{a+b}{2}\right) \le \frac{1}{b-a}\int_a^b f(x)\,dx \ge \frac{f(a)+f(b)}{2} ,
$$

which leads to a contradiction.

---
## **Related**

[[Mean Value theorem]]: the edge of the MVT's capacity. (It can work here.)
[[Taylor Series]]: the basis.
[[Parity]]: Taylor series are sums of odd and even parts, which is what removes the half terms in integrals and means.
[[a Proof by Contradiction]]: a key method.
[[Jensen Inequality]]: the familiar bound this one improves on.

