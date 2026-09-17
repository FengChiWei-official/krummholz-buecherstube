---
tags:
  - type/permanent
  - status/in-progress
  - topic/learning
  - attr/concept
---

## Definition

In calculus and mathematical analysis, **equivalent infinitesimals** (often denoted by the symbol $\sim$) are functions that approach zero at the same rate as the independent variable approaches a specific point (usually $0$). They are powerful tools used to simplify complex limits, evaluate indeterminate forms (like $\frac{0}{0}$), and approximate functions.

Here is a comprehensive breakdown of what they are, how they work, and a handy cheat sheet of standard equivalents.

---

### 1. Formal Definition
Two functions, $\alpha(x)$ and $\beta(x)$, are called **infinitesimals** as $x \to x_0$ if:
$$\lim_{x \to x_0} \alpha(x) = 0 \quad \text{and} \quad \lim_{x \to x_0} \beta(x) = 0$$

They are said to be **equivalent infinitesimals** as $x \to x_0$ if the limit of their ratio is equal to $1$:
$$\lim_{x \to x_0} \frac{\alpha(x)}{\beta(x)} = 1$$

When this happens, we write:
$$\alpha(x) \sim \beta(x) \quad (\text{as } x \to x_0)$$

*(Note: Unless specified otherwise, we usually consider $x \to 0$.)*

---

### 2. The Main Principle (Substitution Theorem)
The primary reason we use equivalent infinitesimals is the **Substitution Theorem for Limits**:

> If $\alpha(x) \sim \alpha_1(x)$ and $\beta(x) \sim \beta_1(x)$ as $x \to x_0$, then:
> $$\lim_{x \to x_0} \frac{\alpha(x)}{\beta(x)} = \lim_{x \to x_0} \frac{\alpha_1(x)}{\beta_1(x)}$$

**Crucial Warning:** You can substitute equivalent infinitesimals freely in **products and quotients**, but **generally NOT in sums or differences** (doing so can lead to severe errors due to cancellation).

---

### 3. Common Equivalent Infinitesimals (as $x \to 0$)
These standard equivalences can be derived using **Taylor's Theorem (Maclaurin series)** and are memorized for quick calculus problem-solving:

#### Trigonometric Functions
* $\sin x \sim x$
* $\tan x \sim x$
* $\arcsin x \sim x$
* $\arctan x \sim x$
* $1 - \cos x \sim \frac{x^2}{2}$
* $\sec x - 1 \sim \frac{x^2}{2}$

#### Exponential and Logarithmic Functions
* $e^x - 1 \sim x$
* $a^x - 1 \sim x \ln a$
* $\ln(1 + x) \sim x$
* $\log_a(1 + x) \sim \frac{x}{\ln a}$

#### Algebraic / Binomial Functions
* $(1 + x)^k - 1 \sim kx \quad (\text{for any real number } k)$
* $\sqrt{1 + x} - 1 \sim \frac{1}{2}x$
* $\sqrt[n]{1 + x} - 1 \sim \frac{1}{n}x$

---

### 4. Examples of Usage

#### Example 1: Evaluating a Limit
Evaluate:
$$\lim_{x \to 0} \frac{\sin(3x)}{\ln(1 + 2x)}$$

* **Step 1:** Recognize that as $x \to 0$, $3x \to 0$ and $2x \to 0$. 
* **Step 2:** Apply standard equivalences:
  * Since $\sin(\theta) \sim \theta$, we have $\sin(3x) \sim 3x$.
  * Since $\ln(1 + \theta) \sim \theta$, we have $\ln(1 + 2x) \sim 2x$.
* **Step 3:** Substitute into the limit:
  $$\lim_{x \to 0} \frac{3x}{2x} = \frac{3}{2}$$

#### Example 2: Algebraic Simplification
Evaluate:
$$\lim_{x \to 0} \frac{\cos(x) - 1}{x^2}$$

* **Step 1:** Recall the identity/equivalence for cosine: $1 - \cos x \sim \frac{x^2}{2}$, which means $\cos x - 1 \sim -\frac{x^2}{2}$.
* **Step 2:** Substitute:
  $$\lim_{x \to 0} \frac{-\frac{x^2}{2}}{x^2} = \lim_{x \to 0} \left(-\frac{1}{2}\right) = -\frac{1}{2}$$
  *(This avoids having to use L'Hôpital's Rule twice!)*

---

### 5. Relation to Landau Symbols (Big-O and Little-o)
Equivalence of infinitesimals is closely tied to asymptotic notation:
* Saying $\alpha(x) \sim \beta(x)$ means that $\alpha(x) - \beta(x) = o(\beta(x))$ as $x \to x_0$.
* It means the difference between the two functions is a *higher-order infinitesimal* compared to $\beta(x)$.

---
## **Related**