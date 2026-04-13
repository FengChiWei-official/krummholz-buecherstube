---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/technique
---
## **Preliminary Deductions**

1.  **Direction of Monotonicity:**
    *   Given $f(b_n) - f(a_n) = a_n$ and $a_n > 0$, it follows that $f(b_n) > f(a_n)$.
    *   Since you stated $b_n > a_n$, the function $f(x)$ must be **strictly increasing**. (If $f$ were decreasing, $b_n > a_n$ would imply $f(b_n) < f(a_n)$).

2.  **Basic Inequality:**
    *   Because $f$ is increasing and $a_n = f(b_n) - f(a_n)$, the value $a_n$ represents the "growth" of the function between $a_n$ and $b_n$.

---

### **Case 1: The Recursive Sequence ($b_n = a_{n-1}$)**

If we set $b_n = a_{n-1}$, the equation becomes:
$$f(a_{n-1}) - f(a_n) = a_n$$
> $f(a_{n-1}) - a_n = f(a_n)$

#### **1. Proof that $a_n$ is decreasing**
*   Since $a_n > 0$ for all $n$, then $f(a_{n-1}) - f(a_n) > 0$.
*   This implies $f(a_{n-1}) > f(a_n)$.
*   Because $f$ is strictly increasing, $f(a_{n-1}) > f(a_n) \implies a_{n-1} > a_n$.
*   Therefore, $\{a_n\}$ is a **strictly decreasing sequence**.

#### **2. Proof of the existence of a limit**
*   The sequence $\{a_n\}$ is monotonic (decreasing).
*   The sequence is bounded below (given $a_n > 0$).
*   By the **Monotone Convergence Theorem**, the limit $\lim_{n \to \infty} a_n = L$ exists and $L \ge 0$.

#### **3. Determining the Limit ($L$)**
If $f$ is continuous, we take the limit of both sides:
$$\lim_{n \to \infty} [f(a_{n-1}) - f(a_n)] = \lim_{n \to \infty} a_n$$
$$f(L) - f(L) = L$$
$$0 = L$$
**Conclusion:** In Case 1, the sequence $a_n$ converges to $0$.

---

### **Case 2: The Squeeze Limit**

You noted: $\lim_{n \to \infty} b_n = 0$ and $b_n > 0 > a_n > 0$ (Note: the second part appears to be a typo, likely intended as $b_n > a_n > 0$).

#### **1. Limit of $a_n$**
*   If $b_n \to 0$ and we are given $0 < a_n < b_n$:
*   By the **Squeeze Theorem (Sandwich Theorem)**, since $b_n$ goes to 0 and $a_n$ is trapped between 0 and $b_n$, then:
    $$\lim_{n \to \infty} a_n = 0$$

#### **2. Consistency Check**
*   If $\lim a_n = 0$ and $\lim b_n = 0$, then $f(b_n) - f(a_n) = a_n$ becomes:
    $$f(0^+) - f(0^+) = 0$$
*   This holds true for any function $f$ that is right-continuous at $x=0$.
### **Example Function**
Let $f(x) = 2x$.
Then the equation $f(b_n) - f(a_n) = a_n$ becomes:
$2b_n - 2a_n = a_n \implies 2b_n = 3a_n \implies a_n = \frac{2}{3}b_n$.

*   In **Case 1** ($b_n = a_{n-1}$): $a_n = \frac{2}{3}a_{n-1}$. This is a geometric progression with $r = 2/3$, which clearly decreases to 0.
*   In **Case 2**: If $b_n \to 0$, then $a_n = \frac{2}{3}b_n$ must also $\to 0$.