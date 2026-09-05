---
tags:
  - type/permanent
  - status/in-progress
  - attr/concept
  - topic/math
---

> **Historical station**: the expansion of the sample space — from Pascal's finite, equally-likely outcomes (1654) to Kolmogorov's abstract measurable spaces (1933) and their surprising universal source: the infinite product of fair coins generates every distribution there is.

## Product Spaces

When you repeat an experiment $n$ times independently, the combined space is the **product space** of $n$ copies of the single-trial space $\Omega_0$:

$$
\Omega^{(n)} = \Omega_0 \times \Omega_0 \times \cdots \times \Omega_0 \quad (n \text{ times})
$$

with the **product measure** $P^{\otimes n}$. This construction is universal — it works for any $\Omega_0$ and any $n$ (including $n = \infty$).

| Single-trial space | n repeats → combined space | Aggregate distribution |
|-------------------|---------------------------|----------------------|
| $\{1,...,K\}$ (Categorical) | $\{1,...,K\}^n$ | Multinomial(n, $\mathbf{p}$) |
| $\mathbb{R}$ (a continuous RV) | $\mathbb{R}^n$ | Distribution of sample mean, max, etc. |
| $\{0,1\}$ (Bernoulli) | $\{0,1\}^n$ | Binomial(n, p) |

**The product space $\Omega^{(n)} = \Omega_0^n$ is always the correct combined space for independent repeats.** Bernoulli trials are the special case where $\Omega_0 = \{0,1\}$.

---

## Binary Encoding of Discrete Spaces

Any finite set of size $K$ can be encoded into $\{0,1\}^m$ as long as $2^m \ge K$ (i.e., $m \ge \lceil \log_2 K\rceil$). The encoding is a **bijection** between the original outcomes and a subset of $\{0,1\}^m$.

| $K$ outcomes | encode as | lives in |
|-------------|-----------|----------|
| Die roll (6) | 3-bit binary strings | $\{0,1\}^3$ (8 pts, 2 unused) |
| Card from deck (52) | 6-bit strings | $\{0,1\}^6$ (64 pts) |
| Categorical (K) | $\lceil \log_2 K\rceil$ bits | $\{0,1\}^m$ |

But the distribution on $\{0,1\}^m$ is **not** the product of independent Bernoulli($1/2$) measures. It concentrates on $K$ specific points. The measure is not product Bernoulli.

So: *the space* can be binary, but *the measure* is arbitrary.

---

## The Universal Randomness Source

If you have access to an infinite supply of independent Bernoulli($1/2$) variables — the product space $(\{0,1\}^\infty, \text{Bernoulli}(1/2)^{\otimes \infty})$ — you can construct **any** discrete random variable as a deterministic function of them.

### The inverse-transform construction

1. From the infinite coin-flip sequence, build $U \sim \text{Uniform}(0,1)$ by reading the bits as a binary expansion:

$$
U = \sum_{i=1}^\infty B_i \cdot 2^{-i}, \quad B_i \overset{i.i.d.}{\sim} \text{Bernoulli}(1/2)
$$

2. Given a desired distribution $P$ with CDF $F$, define the quantile function:

$$
G(u) = \inf\{x \in \mathbb{R} : F(x) \ge u\}
$$

3. Then $X = G(U)$ has distribution $P$.

### What this tells us

The space $\{0,1\}^\infty$ with product Bernoulli($1/2$) measure is a **universal probability space**:

$$
(\{0,1\}^\infty, \text{Bernoulli}(1/2)^{\otimes \infty}) \;\xrightarrow{\text{any discrete $X$}}\; (\mathbb{R}, P_X)
$$

Every discrete distribution is a pushforward of the infinite Bernoulli product measure along some measurable function.

> **A single infinitely-fair coin can generate any discrete randomness there is.**

This is the mathematical basis of **pseudo-random number generation**: every random draw in a computer is ultimately a deterministic function of a binary IID source.

The infinite Bernoulli product space is not just universal for discrete distributions — it is **universal for all distributions on Polish spaces** (any complete separable metric space). Every probability distribution on a Polish space can be realized as the pushforward of $U \sim \text{Uniform}(0,1)$. Since $\text{Uniform}(0,1)$ itself comes from $\{0,1\}^\infty$ with i.i.d. Bernoulli($1/2$), we get:

$$
\{0,1\}^\infty \;\xrightarrow{\text{bits} \to U}\; [0,1] \;\xrightarrow{\text{quantile}}\; X \sim P
$$

The product space of infinitely many fair coins is a **generator for all probability theory**.

---

## What Representation Really Means

| Claim | True? | Meaning |
|-------|-------|---------|
| "Every discrete space can be encoded in a binary space" | ✅ | The *outcome set* becomes $\{0,1\}^m$ via bit encoding |
| "Every discrete **distribution** is a pushforward of i.i.d. Bernoulli(1/2)" | ✅ | Using quantile construction from infinite coins |
| "Every discrete distribution can be **written as** i.i.d. Bernoulli + deterministic function" | ✅ | Same as above |
| "The space of $n$ i.i.d. **discrete** trials is $\Omega_0^n$, which is itself a binary space" | ❌ | Only if $\Omega_0 = \{0,1\}$. Otherwise $\Omega_0^n$ is a product of non-binary spaces, but those outcomes can be re-encoded as bits (expanding the dimension). |
| "Bernoulli variables are sufficient for all discrete modeling" | 🟡 | Sufficient as a *randomness source*, but the resulting variables in a model (e.g., a Categorical) are functions of Bernoullis — not themselves Bernoulli. The model's *natural* variables are not binary. |

**Summary**: the space-level encoding fact and the universal-source construction are deep — they reveal that all randomness can be reduced to fair coin flips. But modeling in that reduced language obscures the structure; we keep product spaces $\Omega_0^n$ as the natural description for independent repetition.

---

## **Related**

[[Index of Probability]]
[[Probability System and Random Variables]]
[[The Scenes and Processes of Probability]]
[[Universal Limit Theorems]]
[[Poisson Process and the Count-Waiting Duality]]
[[Memorylessness, Time and Aging]]