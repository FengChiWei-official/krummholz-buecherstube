---
tags:
  - type/permanent
  - status/in-progress
  - topic/learning
  - attr/concept
---

## Definition

$$
\frac{cx}{\sqrt{a+bx^{2}}}
$$

This is a classic functional form that appears often in physics (especially relativity and electrodynamics) and in calculus. Although different from the $x + 1/x$ structure you previously looked at, it has notable symmetry and geometric properties:

## 1. It is "bounded" (S-shaped / sigmoid-like) [[Sigmoid Function]]

If $a, b > 0$, the function behaves like a soft-saturating function.

- Asymptotes: as $x \to \infty$, $f(x) \to \frac{c}{\sqrt{b}}$; as $x \to -\infty$, $f(x) \to -\frac{c}{\sqrt{b}}$.
- Shape: near the origin it is approximately linear (slope $c/\sqrt{a}$); as $x$ grows the increase slows and eventually levels off. This makes it useful as a normalization or activation-like function.

## 2. "Velocity" and "momentum" in physics

In special relativity, setting $a=1, b=1/c^2$ recovers the familiar relation between momentum and velocity:

- It maps Newtonian linear velocity into a form bounded by the finite speed of light.
- The Lorentz factor $\gamma = 1/\sqrt{1-v^2/c^2}$ is essentially a variant of the denominator.

## 3. Antiderivative symmetry

One attractive feature is the closed-form antiderivative:
$$\int \frac{cx}{\sqrt{a+bx^2}} dx = \frac{c}{b}\sqrt{a+bx^2} + C$$

- Remark: the antiderivative is proportional to the denominator. This "denominator inside derivative, denominator after integration" property is convenient when solving potential-energy style integrals.

## 4. Relation to hyperbolic functions ([[Hyperbolic Functions]])

With the substitution $x = \sqrt{a/b}\sinh(\theta)$:

- the denominator becomes $\sqrt{a}\cosh(\theta)$.
- the whole expression simplifies to a simple ratio of hyperbolic sine/cosine, indicating a projection of hyperbolic geometry into Euclidean coordinates.

## 5. Link to $x + 1/x$

([[Euler Substitution]])

If you set $x = \tfrac{1}{2}(t - \tfrac{1}{t})$ (a transform related to Chebyshev-type substitutions), then
$$\sqrt{1+x^2} = \tfrac{1}{2}(t + \tfrac{1}{t})$$
which converts the "minus" symmetry into an "additive" symmetry.

Summary: this function strikes a balance between linear growth and square-root suppression.

Are you encountering this in a particular integral transform, or when studying activation functions in neural networks (it resembles the Softsign)?


---
## **Related**