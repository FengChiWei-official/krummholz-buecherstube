---
aliases:
  - 积分中的展开
---

## Definition

Given a function $f(x)$, we can expand it as

$$
f(x) = \sum_{i=0}^{\infty} \frac{f^{(i)}(x_0)}{i!}(x-x_0)^i ,
$$

with $P_n(x) = \sum_{i=0}^{n} \frac{f^{(i)}(x_0)}{i!}(x-x_0)^i$ its $n$-th partial sum.

On an interval $[a,b]$, take $x_0 = \frac{a+b}{2}$; then the integral over the interval is

$$
\int_a^b \left( \sum_{i=0}^{n} \frac{f^{(i)}\!\left(\frac{a+b}{2}\right)}{i!}\left(x-\frac{a+b}{2}\right)^i \right)
+ \frac{f^{(i+1)}(\xi)}{(i+1)!}\left(x-\frac{a+b}{2}\right)^{(i+1)} dx ,
$$

where the trailing term is the remainder of the $n$-term form. [[Parity]] then deletes the odd terms, leaving

$$
\int_a^b \left( \sum_{i=0}^{\infty} \frac{f^{(2i)}\!\left(\frac{a+b}{2}\right)}{(2i)!}\left(x-\frac{a+b}{2}\right)^{2i} \right)
+ \left( \frac{f^{(i+1)}(\xi)}{(i+1)!}\left(x-\frac{a+b}{2}\right)^{(i+1)} \right) dx .
$$

---
## **Related**

[[Taylor Series]]: the expansion is its Taylor series.
[[Polynomials]]: the partial sums $P_n$ are polynomials.
[[Parity]]: it is what deletes the odd terms.
[[Secant Integral Inequality by Midpoint Expansion]]: the inequality this expansion is used to prove.
