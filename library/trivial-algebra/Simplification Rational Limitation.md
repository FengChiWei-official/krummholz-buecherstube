---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
---

## Definition

The goal of `Simplification Rational Limitation` is to turn expressions that are hard to compare, cancel, or substitute
into standard forms that are comparable, cancelable, and directly substitutable through structured rewrites.

## Core Workflow

1. Unify scale first: extract non-zero dominant factors.
2. Then linearize locally: replace controllable small blocks with equivalent infinitesimals.
3. Finally rewrite structure: use identity transforms to convert denominators or composite forms into cancelable forms.

## Technique Stack

### 1) Dominant Factor Extraction
- Typical trigger: numerator and denominator are polynomial/radical/exponential combinations with mixed orders.
- Core action: factor out the highest-order or dominant-growth common factor.
- Goal: reduce the limit to a ratio of "constant + small perturbation".

### 2) Equivalent Infinitesimals
- Typical trigger: basic small blocks such as $\sin x, \tan x, e^x-1, \ln(1+x), 1-\cos x$ appear.
- Core action: replace only near the zero limit point, and only for controllable terms in multiplicative/divisive structures.
- Goal: quickly eliminate high-complexity nonlinear terms.

Common equivalent pairs ($x \to 0$):
- $\sin x \sim x$
- $\tan x \sim x$
- $e^x - 1 \sim x$
- $\ln(1+x) \sim x$
- $1-\cos x \sim \frac{x^2}{2}$

### 3) Identity Transform
- Typical trigger: denominator is complex, sum/difference structures appear, or composite functions are hard to compare directly.
- Core action: prioritize rewrites that are exactly true, rather than early approximation.
- Goal: create cancelable factors or rewrite the denominator into a monomial-like structure.

Common identity templates:
- Conjugate: $(a-b)(a+b)=a^2-b^2$
- Trigonometric identities: $1-\sin^2 x=\cos^2 x$, $1+\tan^2 x=\sec^2 x$
- Exponential-log conversion: $u(x)^{v(x)}=e^{v(x)\ln u(x)}$ (requires $u(x)>0$)
- Homogeneous ratio conversion: see [[The Ratio Substitution]]

## Decision Rules

1. If factor extraction is possible, do not start with equivalent infinitesimal replacement.
2. If identity transforms can simplify exactly, avoid premature approximation.
3. After approximation, check whether the dominant order has changed.
4. When the denominator is complex, prioritize conjugation and normalization.

## Common Pitfalls

- Cancelling "terms" directly instead of cancelling factored components.
- Misusing equivalent infinitesimals outside the zero-limit neighborhood.
- Incorrect replacement in additive/subtractive structures (equivalent infinitesimals are safer in multiplicative/divisive chains).
- Ignoring domain constraints (for example, $\ln u(x)$ requires $u(x)>0$).

## Related Techniques

- [[Rational Limitation]]
- [[Power-Exponential Functions Transform]]
- [[The Ratio Substitution]]
- [[Monotonic Squeezing]]
- [[Denominator Normalization]]


---
## **Related**

[[Index of Math Expressions Pattern]]
[[Index of Limit Strategy]]
[[Index of Scaling and Normalization]]