---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/concept
aliases:
  - Sum to Product
---

## Definition

Mechanism $$x+\frac{1}{x} \ge 2$$
Transforming a **SUM** of reciprocal terms into a **Constant Product**
It give a **Lower Boundary** of the [[Hook Function]].
> [!note] 
> Therefore, It usually don't appear in [[Limitation]] Proof, who's common form is $C \le f(x)$ and a [[Inequality]] given it's upper bound.



## Common Variant: Fraction

### Type 1: Fraction (degree difference = +1)

$$
\begin {align}

& && \frac{Ax^2 + Bx + C} {Dx + E} \\
& \to && \frac{Ax^2 + Bx + C}{a(x+b)} \\
& \to && d(x+b) + \frac{k}{a(x+b)} + c


\end {align}
$$
> [!note]
> How do you recognize it?
> Degree Difference is ** 2 to 1 **. 

And it have a Reciprocal Form $\frac {Dx + E} {Ax^2 + Bx + C}$, which need you take a **Reciprocal** again.

### Type 2: Transcendental Nested Type (Exponential/Logarithmic)
#### Exponential Form
$$
\begin {align}
& && a(x+b) + \frac{k}{a(x+b)}\\
& \to && \frac{b(x+c)^2 +k}{ax+ac}\\
& \to && \frac{bx^2+2bcx + bc^2 + k}{ax+ac}

& &&ae^x + be^{-x} + c \\
& \to && a t + \frac{b}{t} + c, \\
& && \quad \text{where }t = e^x, t\ge 0.
\end {align}
$$
#### Logarithmic Form

$$
\begin{align}
&&&\ln (ax^2 + b) - \ln (x) \\
& \to &&\ln(\frac{ax^2+b}{x}) \\
& \to && \ln (ax + \frac{b}{x}) 
\end{align}
$$
> [!note]
> $\ln f(x) - \ln g(x) = \ln \frac{f(x)} {g(x)}$


### Type3. Irrational (Radical) Type

Often found in geometric optimization problems (Volume/Surface Area).
#### Inside a Root
$$
\begin{align}
&&&\frac{x+a}{\sqrt x} \\
& \to && \frac {t^2 + a} {t}, \text { where } t = \sqrt{x} \\
& \to && t + \frac{a}{t} \\
\end{align}
$$

---
## **Related**