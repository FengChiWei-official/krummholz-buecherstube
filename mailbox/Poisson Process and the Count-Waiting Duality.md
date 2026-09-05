---
tags:
  - type/permanent
  - status/in-progress
  - attr/concept
  - topic/math
---

> **Historical station**: from Poisson's law of small numbers (1837) to the continuous-time process. The rare-event count and the inter-event waiting time are not two distributions but two faces of one process — a duality the process formalism made precise.

## Definition

A **Poisson process** is a continuous-time stochastic process $\{N(t), t \ge 0\}$ that counts the number of events that have occurred by time $t$. It is defined by three postulates:

| Postulate | Meaning |
|-----------|---------|
| **1. Independent increments** | For disjoint time intervals, the counts are independent random variables. What happens in [0,t] and (t, t+s] are unrelated. |
| **2. Stationary increments** | The distribution of $N(t+s) - N(t)$ depends only on $s$, not on $t$. The process is "time-homogeneous." |
| **3. No simultaneity** | $P(N(\Delta t) \ge 2) = o(\Delta t)$ as $\Delta t \to 0$. Two events cannot occur at the exact same instant. |

From these three axioms, everything else follows.

---

## The Two Faces

The Poisson process has **two equivalent descriptions** that are dual to each other.

### Face 1: Count (forward in time)

Fix a time window $[0, t]$ and ask: *how many events occurred?*

$$
N(t) \sim \text{Poisson}(\lambda t)
$$

- $N(t)$ = number of events up to time $t$
- $\lambda$ = rate (expected events per unit time)
- $P(N(t) = k) = \frac{(\lambda t)^k}{k!} e^{-\lambda t}$

**The random variable is a count** — discrete, non-negative integer.

### Face 2: Waiting time (between events)

Fix an event count $r$ and ask: *how long until the r-th event?*

Define $S_1$ = time of first event, $S_2 - S_1$ = time between first and second, etc.

$$
S_1 \sim \text{Exponential}(\lambda)
$$

$$
S_r = \sum_{i=1}^r S_i \sim \text{Gamma}(r, \lambda)
$$

- $S_1$ = waiting time for 1st event
- $S_r$ = waiting time for r-th event
- $f_{S_r}(t) = \frac{\lambda^r t^{r-1} e^{-\lambda t}}{(r-1)!}$

**The random variable is a duration** — continuous, non-negative real.

---

## The Duality

The two faces are connected by a **fundamental equivalence**:

> $$\{N(t) \ge r\} \iff \{S_r \le t\}$$

In words: **the r-th event occurs at or before time t if and only if the number of events by time t is at least r.**

This is not an approximation. It is an exact logical equivalence. The count and the waiting time are **two observations of the same underlying process** — you just choose whether to fix time and observe count, or fix count and observe time.

```
Poisson Process
    │
    ├── Fix time t → N(t) ~ Poisson(λt)   (count)
    │
    └── Fix count r → S_r ~ Gamma(r, λ)   (waiting)
                           └── for r=1: S_1 ~ Exponential(λ)
```

---

## Markov Property

A Poisson process is a **continuous-time Markov chain** on the state space $\{0, 1, 2, ...\}$ where:

- State $N(t) = k$ means k events have occurred.
- From state $k$, the only transition is $k \to k+1$.
- The rate of this transition is $\lambda$ — constant, independent of $k$.

This is the simplest possible continuous-time Markov chain: a pure birth process with constant birth rate. It is Markov because the Exponential waiting time has no memory — from any state, the time to the next event is always $\text{Exponential}(\lambda)$, regardless of how long the process has been running.

### The three key properties (derived from axioms)

1. **Inter-arrival times are i.i.d. Exponential** — from the independent and stationary increments.
2. **Memorylessness of Exponential** — $P(S_1 > s + t \mid S_1 > s) = P(S_1 > t)$ — the future depends only on the present, not the past.
3. **Superposition and decomposition** — merging two independent Poisson processes yields a Poisson process with rate $\lambda_1 + \lambda_2$; thinning (marking each event as type A with prob p) yields independent Poisson processes with rates $p\lambda$ and $(1-p)\lambda$.

---

## Poisson as the Rare-Event Limit

### The law of small numbers

The Poisson distribution is the stable limit of counting **rare, independent events** over many opportunities:

> If $X_{n1}, ..., X_{nn}$ are independent Bernoulli($p_{ni}$) and all $p_{ni} \to 0$ while $\sum_{i=1}^n p_{ni} \to \lambda$, then $\sum_{i=1}^n X_{ni} \xrightarrow{d} \text{Poisson}(\lambda)$.

### What can be turned into Poisson

| Original | Mechanism | Approximation |
|----------|-----------|---------------|
| **Binomial(n, p)** | n large, p small, np = λ | Poisson(λ) |
| **Negative Binomial(r, p)** | r → ∞, p → 0, r(1-p)/p → λ | Poisson(λ) — rare successes over many attempts |
| **Poisson Binomial** (independent Ber($p_i$) with unequal $p_i$) | each $p_i$ small, $\sum p_i = \lambda$ | Poisson(λ) (Le Cam's inequality: $\| \text{PB} - \text{Pois}(\lambda) \|_{TV} \le \sum p_i^2$) |
| **Hypergeometric(N, K, n)** | N → ∞, K/N → p, n → ∞, np → λ | Poisson(λ) — limit of sampling without replacement |

### What cannot be turned into Poisson

- **Any continuous distribution** (Normal, Exponential, Gamma, ...) — Poisson is discrete, integer-valued.
- Any count distribution where events are not rare (p not small) — the Poisson approximation degrades rapidly.
- Any distribution with variance not ≈ mean — Poisson forces $\mathbb{E}[X] = \text{Var}(X)$. Overdispersed data needs Negative Binomial.

### Poissonization

Replace a fixed sample size $n$ (Binomial) with a random sample size $N \sim \text{Poisson}(\lambda)$ independent of the data.

$$
\text{If } X_i \overset{i.i.d.}{\sim} \text{Bernoulli}(p), \; N \sim \text{Poisson}(\lambda), \; \text{then } \sum_{i=1}^N X_i \sim \text{Poisson}(\lambda p)
$$

This **introduces independence** between disjoint blocks of a process — the count of events in [0,t] and [t,s] become independent Poisson counts, which makes many analytical derivations tractable.

### Summary: what can be "processed into Poisson"

```
    Bernoulli(p) ──(many, each rare)──→ Poisson(λ)    (law of small numbers)
    Binomial(n,p) ──(n large, p small)──→ Poisson(np) (a special case)
    Exponential(λ) ──(count events)──→ Poisson(λt)   (Poisson process)
    Negative Binomial ──(rare success)──→ Poisson     (limit)
```

**Poisson is the distribution of "how many?" when the answer is usually zero and rarely a small integer.** Any process whose output is a count of rare independent events will "want" to become Poisson.

---

## Superposition & Moments

| Operation | Result |
|-----------|--------|
| **Superposition**: merge two independent Poisson processes with rates λ₁, λ₂ | Result is a Poisson process with rate λ₁ + λ₂. |
| **Decomposition** (Thinning): independently mark each event as type A with prob p, type B with prob 1-p | Type A process ~ Poisson(pλ), type B ~ Poisson((1-p)λ), and they are independent. |

### Moments bridge

| | Poisson (count) | Exponential (waiting) | Gamma (waiting, r events) |
|---|---|---|---|
| **Random variable** | $N$ = number of events | $T$ = time to first event | $T$ = time to r-th event |
| **Support** | $\{0, 1, 2, ...\}$ | $[0, \infty)$ | $[0, \infty)$ |
| **PDF / PMF** | $P(N=k) = \frac{(\lambda t)^k}{k!} e^{-\lambda t}$ | $f_T(t) = \lambda e^{-\lambda t}$ | $f_T(t) = \frac{\lambda^r t^{r-1} e^{-\lambda t}}{(r-1)!}$ |
| **Expectation** | $\lambda t$ | $1/\lambda$ | $r/\lambda$ |
| **Variance** | $\lambda t$ | $1/\lambda^2$ | $r/\lambda^2$ |
| **Memoryless?** | N/A (it's a count) | ✅ Yes | ❌ No (shape r > 1 accumulates) |

### The unifying view

Poisson and Exponential are not separate distributions that happen to be related. They are **the same process observed through different lenses**:

```
         Poisson(λt)
    count ←───────────
    │                  │
    │  同一过程         │
    │                  │
    └───────────→ Exponential(λ)
           waiting
```

Choose your fixed quantity (time or count), and the random variable (count or time) is forced.

---

## Summary

| I fix | I observe | The random variable follows |
|-------|-----------|---------------------------|
| **Time** $t$ | **Count** of events in $[0,t]$ | $N \sim \text{Poisson}(\lambda t)$ |
| **Count** $r = 1$ | **Time** until the first event | $T \sim \text{Exponential}(\lambda)$ |
| **Count** $r$ | **Time** until the r-th event | $T \sim \text{Gamma}(r, \lambda)$ |

And the logical equivalence at the core:

$$
\{N(t) \ge r\} \iff \{S_r \le t\}
$$

This is the deepest relationship between Poisson and Exponential — they are not just mathematically connected; they are **epistemically dual**: two ways of looking at the same randomness.

---

## **Related**

[[Index of Probability]]
[[Probability System and Random Variables]]
[[Probability Spaces and the Universal Source]]
[[The Scenes and Processes of Probability]]
[[Universal Limit Theorems]]
[[Memorylessness, Time and Aging]]