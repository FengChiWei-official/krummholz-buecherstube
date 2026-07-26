---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/views
---

## 1. Core Properties & Linear Transformations
Given that $f(x)$ is an **increasing** function:

*   **Inverse Function:** $f^{-1}(x)$ is also **increasing**.
*   **Linear Transformations:**
    *   $-f(x)$ is **decreasing**.
    *   $f(-x)$ is **decreasing**.
    *   $-f(-x)$ is **increasing**.
*   **Reciprocal:** $\frac{1}{f(x)}$ is **decreasing** (assuming $f(x) \neq 0$).

---

## 2. Compound Functions (The "Same-Increase" Rule)
Let $g(x)$ be a monotonic function. The monotonicity of the composite function $f(g(x))$ depends on the direction of $g(x)$:

*   **Same Direction:** If $g(x)$ is increasing, $f(g(x))$ is **increasing**.
*   **Opposite Direction:** If $g(x)$ is decreasing, $f(g(x))$ is **decreasing**.

> [!note]
> There is a [[Isomorphism]] $$ \text{sgn} (f) = \left \{ \begin{align} & 1 &&f \text{ is increasing }\\ & -1 &&f \text{ is decreasing }\\ \end{align} \right . $$
> $\text{sgn} (f_1 \circ f_2) = \text{sgn} (f_1) \circ \text{sgn}(f_2)$

---

## 3. Operations with Multiple Functions
Assume $g(x)$ is also an increasing function:

*   **Sum:** $f(x) + g(x)$ is **increasing**.
*   **Product:** $f(x) \cdot g(x)$ is **increasing** *only if* both $f(x), g(x) > 0$.
*   **Difference:** $f(x) - g(x)$ is **indeterminate** (the result depends on the relative rate of change of each function).

---

## 4. Symmetry & Parity
The behavior of an increasing function on one side of the y-axis determines its behavior on the other based on its parity:

*   **Odd Function:** If $f(x)$ is odd and increasing on $(0, +\infty)$, it is also **increasing** on $(-\infty, 0)$.
*   **Even Function:** If $f(x)$ is even and increasing on $(0, +\infty)$, it is **decreasing** on $(-\infty, 0)$.

---

## 5. Absolute Values
The monotonicity of $|f(x)|$ depends on the sign of $f(x)$:

*   If $f(x) \geq 0$, $|f(x)|$ is **increasing**.
*   If $f(x) \leq 0$, $|f(x)|$ is **decreasing**.

---

## 6. Transcendental Transformations
Assuming $f(x)$ is in the domain of the following operations:

*   **Logarithmic:** $\ln(f(x))$ is **increasing** (for $f(x) > 0$).
*   **Exponential:** $e^{f(x)}$ is **increasing**.
*   **Power:** $[f(x)]^n$ is **increasing** if $n > 0$ and $f(x) > 0$.

---

## 7. Calculus Perspective
If $f(x)$ is differentiable, its monotonicity is defined by its derivative:

*   **General Rule:** $f(x)$ is increasing if and only if $f'(x) \geq 0$.
*   **Verification of Symmetry:** For the transformation $-f(-x)$:
    $$\frac{d}{dx}[-f(-x)] = -f'(-x) \cdot (-1) = f'(-x)$$
    Since $f(x)$ is increasing, $f'(-x) \geq 0$, confirming that $-f(-x)$ remains **increasing**.
## Examples

---
## **Related**

[[View of Composition of a Function with a Monotonic Function]]