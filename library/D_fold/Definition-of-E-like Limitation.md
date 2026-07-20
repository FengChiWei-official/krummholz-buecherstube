---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/technique
---

## Definition

[[Limitation That Defines E]]
$$\lim_{x \to \infty} 1^x$$

## Mean to Solve

$$
\lim u(x)^{f(x)} = \ e^{\lim f(x)(u(x)-1)}
$$


## Case 1 Rational Base

$\lim_{x \to \infty} (\frac{kx^2+c_1x+c_2}{kx^2+c_3x+c_4})^{f(x)}$, where $lim_{x \to \infty} f(x) = \infty$.
> [!note] 
> $\lim_{x \to \infty} \frac{kx^2+c_1x+c_2}{kx^2+c_3x+c_4} = 1$ for sure.

## Case 2 Trigonometric Base

$$\lim_{x \to 0} (\cos x)^{x^{-k}}$$

## Case 3 Mean of Exponentiation

$$
A = lim_{x \to 0} (\frac{e^x+e^{2x  }+e^{3x}}{3})^{\frac{k}{x}}
$$
$A = e^{\frac{k}{3}(\lim \frac{e^x-1}{x} +\lim \frac{e^{2x}-1}{x} +\lim \frac{e^{3x}-1}{x})}$
> $e^{kx} - 1  =  kx$

---
## **Related**