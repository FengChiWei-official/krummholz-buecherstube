---
tags:
  - type/permanent
  - status/in-progress
  - attr/principle
  - topic/math
---

> **Historical station**: the spine of the subject. Bernoulli's LLN (1713) showed aggregate regularity; De Moivre and Laplace found its shape in the Normal curve (CLT); Poisson (1837) found the rare-event law; extreme value theory completed the family. Normal and Poisson are the two 'homeless' attractors these theorems keep producing.

## The Two Layers (Processes vs Limit Laws)

Distributions come from two distinct sources:

1. **Concrete processes** — specific generative stories (Bernoulli trials, Poisson arrivals, finite-population draws) with native distributions.
2. **Universal limit theorems** — patterns that emerge when you push any process to infinity (LLN, CLT, Law of Small Numbers, EVT).

Normal and Poisson appear in both layers: Poisson is both a native count (Poisson process) and a limit (Bernoulli process). Normal is purely a limit theorem — it has no native process.

| Distribution | Native to process? | Also appears as limit of? |
|-------------|-------------------|--------------------------|
| **Bernoulli(p)** | ✅ Bernoulli process only | — |
| **Binomial(n,p)** | ✅ Bernoulli process only | — |
| **Geometric(p)** | ✅ Bernoulli process only | — |
| **NegBin(r,p)** | ✅ Bernoulli process only | — |
| **Exponential(λ)** | ✅ Poisson process only | — |
| **Gamma(r,λ)** | ✅ Poisson process only | — |
| **Poisson(λ)** | ✅ Poisson process (native count) | ⬅️ Bernoulli process (rare-event limit) |
| **Normal(μ,σ²)** | ❌ No native process | ⬅️ **Any** i.i.d. sum via CLT |
| **Gumbel / Fréchet / Weibull-EV** | ❌ No native process | ⬅️ Max of any i.i.d. sample via EVT |

**Normal and the extreme-value distributions are "homeless"** — they do not originate from a single concrete process. They are emergent patterns that appear at the limit of many different processes.

---

## The Universal Laws

There are four universal limit theorems that govern how distributions behave at scale:

| Theorem | What it says | Limit distribution | Applies to |
|---------|-------------|-------------------|------------|
| **Law of Large Numbers (LLN)** | Sample mean converges to population mean | Degenerate at $\mu$ | Any i.i.d. sequence with finite mean |
| **Central Limit Theorem (CLT)** | Standardized sum converges to Normal | **Normal(0,1)** | Any i.i.d. sequence with finite variance |
| **Law of Small Numbers (Poisson limit)** | Sum of rare independent events converges to Poisson | **Poisson(λ)** | Sum of Bernoulli($p_{ni}$) with each $p_{ni} \to 0$, $\sum p_{ni} \to \lambda$ |
| **Extreme Value Theory (EVT)** | Maximum of i.i.d. sample converges to one of three families | **Gumbel / Fréchet / Weibull-EV** | Max of any i.i.d. sample (under regularity) |

---

## The Attractors

**Normal** is the universal attractor for sums. The CLT says that for **any** i.i.d. sequence $X_1, X_2, ...$ with finite mean and variance:

$$
\frac{\sum X_i - n\mu}{\sigma\sqrt{n}} \xrightarrow{d} N(0,1)
$$

The $X_i$ need not be Bernoulli. They can be Exponential, Poisson, Gamma — any distribution with finite variance. Normal does not "belong" to the Bernoulli process; it emerges whenever you sum enough independent contributions.

**Poisson** is the universal attractor for rare-event counts. The Law of Small Numbers says that if you have many independent Bernoulli trials, each with vanishingly small success probability, their sum converges to Poisson — regardless of the underlying trial structure.

**Gumbel / Fréchet / Weibull-EV** are the universal attractors for extremes. No matter what distribution you start with, the sample maximum (under regularity) converges to one of these three.

---

## The Two Directions of ∞

The Bernoulli process has two knobs: number of trials $n$ and success probability $p$. Pushing each to its limit produces a different attractor:

```
Binomial(n, p)
    │
    ├── n → ∞, p fixed
    │       → Normal(np, np(1-p))      (CLT for Binomial)
    │
    └── n → ∞, p → 0, np = λ fixed
            → Poisson(λ)               (Law of Small Numbers)
```

| What I let → ∞ / → 0 | Result | Interpretation |
|----------------------|--------|---------------|
| **$n \to \infty$, $p$ fixed** | **Normal** | The count grows unbounded; CLT rescales it. The absolute count becomes irrelevant — what matters is the standardized deviation from the mean. |
| **$n \to \infty$, $p \to 0$, $np = \lambda$** | **Poisson** | The count stays bounded ($\lambda$ fixed). The absolute count remains meaningful. Rare events over many opportunities. |
| **$n$ fixed, $p$ fixed** | **Binomial** itself | Finite window. Always valid. |

**The key difference**: Normal standardizes away the mean (you lose the absolute scale), Poisson preserves the absolute count because the mean stays constant by construction.

All count distributions converge to either Normal or Poisson as you push them:

| Count distribution | Limit as parameter → ∞ |
|-------------------|----------------------|
| **Binomial(n, p)** | $n \to \infty$, $p$ fixed → **Normal** |
|  | $n \to \infty$, $p \to 0$, $np=\lambda$ → **Poisson** |
| **Poisson(λ)** | $\lambda \to \infty$ → **Normal(λ, λ)** |
| **Negative Binomial(r, p)** | $r \to \infty$, $p$ fixed → **Normal** |
|  | $r \to \infty$, $p \to 0$, $r(1-p)/p = \lambda$ → **Poisson** |
| **Hypergeometric(N, K, n)** | $N \to \infty$, $K/N = p$ → **Binomial(n, p)** |
|  | then $n \to \infty$, $p \to 0$ → **Poisson** or |
|  | $n \to \infty$, $p$ fixed → **Normal** |

**All roads lead to Normal if you push the mean to infinity. All roads lead to Poisson if you push the mean to a finite constant while making individual events rarer.**

```
                  Binomial
                  /      \
                 /        \
                /          \
         Normal              Poisson
    (n→∞, p fixed)      (n→∞, p→0, np=λ)
               \          /
                \        /
                 \      /
            Negative Binomial, Hypergeometric, etc.
```

---

## Summary

| Layer | What lives there | Examples |
|-------|-----------------|----------|
| **Concrete processes** | Native distributions tied to a specific generative story | Bernoulli, Binomial, Geometric, NegBin, Exponential, Gamma |
| **Universal limit theorems** | Distributions that emerge at the limit of many processes | Normal, Poisson (also native to Poisson process), Gumbel, Fréchet, Weibull-EV |

Normal is what happens when counts become large and you standardize. Poisson is what happens when counts stay moderate but events become rare. Both are limit laws that transcend the specific process generating the data.

---

## **Related**

[[Index of Probability]]
[[Probability System and Random Variables]]
[[Probability Spaces and the Universal Source]]
[[The Scenes and Processes of Probability]]
[[Poisson Process and the Count-Waiting Duality]]
[[Memorylessness, Time and Aging]]