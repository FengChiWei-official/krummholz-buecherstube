---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/map
---

## Definition

Limit Strategy organizes solving routes by trigger: rational structure, substitution form, squeeze condition, and exponential conversion.

## Solving Taste

### Route Order

1. First turn the expression into an indeterminate form plus an ordinary limit that can be understood and analyzed.
2. Simple fractions: check the condition first, then use equivalent infinitesimals / the notable limits. Reduce into [[Standard Limits]].
3. If neither applies, first try the simple dominant-part extraction.
4. Then L'Hospital's rule, or variable-limit integrals. [[L'Hospital Rule]] turns simple fractions into even simpler ones.

### Branches by Structure

- **Difference or composition**: when it is simple, use Taylor (subtracting terms of different types) or MVT (subtracting terms of the same type); when it is too complex, fall back to dominant-part extraction and reduce to the dominant part (relative relation $-1$).
- **Infinity**: consider reciprocal substitution / dominant-part extraction.

### When the Squeeze Theorem Applies

1. A constant lower bound is known.
2. The expression can easily be bounded.
3. Periodicity.
4. Boundedness / limit (local boundedness).
5. Infinite series.
6. Bounded oscillation.

### When You Do Not Know What to Do

1. Apply an identity transform to the part you cannot understand (power-exponential functions).
2. Arrange the whole expression into a product.
3. Remove, by a technique, the structure you have no means to study (variable-limit integrals).
4. Estimate the behaviour: get a rough picture of the overall properties.
5. Dominant-part extraction: $A - A = A(1 - 1) = A\left(\frac{A'}{A} - 1\right)$.

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

### Logarithmic Route

[[Logarithmic Functions Pattern for Limit]]

### Bounding Route

[[Monotonic Squeezing]]

### Overview Route

[[Links of Solving Limit of Function]]
[[Limit]]

## Special Techniques

[[Denominator Normalization]] --> [[Radical Normalization]] --> [[Radical Normalization for Limit]]

Sometimes you can make the infinitesimals explicit, lowering the difficulty of solving and keeping the denominator convenient for further transformation.

[[Simplification Rational Limit]]
[[Power-Exponential Functions Transform]]

## Infinitesimals

The first trick is [[Equivalent Infinitesimals]].

The second is [[Focus on the Dominant]], which derives:

- difference of functions and composite functions -> [[Taylor Series]] or [[Mean Value theorem]]
  > [[Principle of Reduction]].

Equivalently:

1. $\alpha = o(\beta) \to (\alpha + \beta) \sim \beta$
2. $\alpha = o(\beta) \to (\alpha \beta) = o(\beta^2)$

## Functions defined by integrals

The major goal here is using [[L'Hospital Rule]].
However, most of the time you should use [[Taylor Series]] to simplify it first.

1. $\int_0^x f(t) dt$ , where $\lim_{t \to 0} f(t) = 0$.
2. $\int_0^{h(x)} f(t) dt$ , where as $x \to a$ we have $h(x) \to 0$, $h(x) \ne 0$, and the integrand has limit $f(t) \to A$ (a non-zero constant).

Both can be seen as: extract the dominant part with Taylor first, then prove equivalence with L'Hospital's rule.

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