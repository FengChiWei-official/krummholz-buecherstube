---
tags:
  - type/permanent
  - status/in-progress
  - attr/principle
  - topic/math
---

> **Historical station**: the process turn. Markov (1906) introduced dependence, Wiener (1923) built Brownian motion, and the field moved from isolated random variables to processes in time. This note organizes the modern synthesis — the scenes and processes from which every standard distribution arises, stood against the universal limit theorems.

## The Failure Frame

An earlier attempt classified distributions by **what X measures**: trials (Bernoulli family) vs time (Exponential family). That classification failed because:

- **Bernoulli** measures neither trials nor time — it is an **indicator** on a single trial.
- **Poisson** is not a time measurement but a **count over continuous time**, falling between the two categories.

The error: classifying by a property of the random variable rather than by what process generates it. A better story starts from **process**, not from $X$.

---

## The Two Layers

We need three distinct layers, not one flat classification:

```
Layer 1: Concrete Processes
  - Bernoulli process (discrete-time, i.i.d. trials)
  - Poisson process (continuous-time, constant rate)
  - Finite-population sampling (without replacement)
  - Extreme-value sampling (take max of n i.i.d.)

Layer 2: Universal Limit Theorems (apply across processes)
  - Law of Large Numbers (LLN)     → sample mean → μ
  - Central Limit Theorem (CLT)    → sum → Normal
  - Law of Small Numbers           → rare-event count → Poisson
  - Extreme Value Theory (EVT)     → max → Gumbel / Fréchet / Weibull-EV

Layer 3: The Distributions
  - Some are "native" to a process (Bernoulli lives only in Bernoulli process)
  - Some are universal attractors (Normal, Poisson appear as limits of many processes)
```

### What belongs uniquely to which process

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

## The Process Map

### Process 1: The Bernoulli Process (Discrete-Time)

A sequence of independent Bernoulli(p) trials at discrete time steps $t = 1, 2, 3, ...$

```
Bernoulli Process
    │
    ├── Observe ONE trial (n=1)
    │       → X = indicator          (Bernoulli(p))
    │
    ├── Fix number of trials n, count successes
    │       → X = count              (Binomial(n, p))
    │
    ├── Fix target count, measure trials needed
    │       → X = waiting            (Geometric(p) / NegBin(r, p))
    │
    ├── n → ∞, p fixed, standardize
    │       → X = standardized count (Normal)      ← CLT limit for Binomial
    │
    └── n → ∞, p → 0, np = λ fixed
            → X = bounded rare count (Poisson)     ← Law of Small Numbers
```

### Process 2: The Poisson Process (Continuous-Time)

Events occur at constant rate $\lambda$ in continuous time, with independent increments and no simultaneous events.

```
Poisson Process
    │
    ├── Fix time window [0, t], count events
    │       → X = count       (Poisson(λt))
    │
    └── Fix target count, measure waiting time
            → T = waiting     (Exponential(λ) for target=1)
            → T = waiting     (Gamma(r, λ) for target=r)
```

**Note**: Poisson and Exponential are **dual** — they are two observations of the same underlying process.

### Complete Process Map

| Process | Indicator | Finite-N Count/Waiting | Limit as n→∞ (p fixed) | Limit as n→∞ (p→0) |
|---------|-----------|----------------------|----------------------|--------------------|
| **Bernoulli process** | Bernoulli(p) | Binomial(n,p), Geometric(p), NegBin(r,p) | **Normal** | **Poisson** |
| **Poisson process** | — | Poisson(λt), Exponential(λ), Gamma(r,λ) | — | — |
| **Extreme** | — | Gumbel / Fréchet / Weibull-EV | — | — |
| **Mixture** | any | any | any | any |

---

## The Seven Scenes

These are the irreducible generative stories. Everything else is composition, transformation, or limit of these.

### 1. Binary Trial

| | |
|---|---|
| **Story** | One experiment, two possible outcomes. |
| **Distribution** | Bernoulli(p) |
| **Random variable** | $X = \begin{cases}1 & \text{success} \\ 0 & \text{failure}\end{cases}$ |
| **Parameter** | $p = P(\text{success})$ |
| **Real-world** | coin flip, click-through, survival at one instant, indicator of any binary event |
| **Time model** | No time — a single snapshot |

### 2. Independent Repeats (Same Trial)

| | |
|---|---|
| **Story** | Perform the same trial $n$ times independently. |
| **Distribution** | **Product space** $\Omega_0^n$ with product measure |
| **Scene variants** | |
| Binary trial repeated → count successes | Binomial(n, p) |
| Binary trial repeated → trials until first success | Geometric(p) |
| Binary trial repeated → trials until r-th success | Negative Binomial(r, p) |
| Binary trial repeated → all n outcomes recorded | $\{0,1\}^n$ (full sequence) |
| K-ary trial repeated → counts per category | Multinomial(n, $\mathbf{p}$) |
| **Parameter** | n or stopping rule |
| **Real-world** | survey of n people, n days of operation, repeated measurements |
| **Time model** | Discrete steps; each step is an independent experiment |

### 3. Rare Event Count (Law of Small Numbers)

| | |
|---|---|
| **Story** | A large number of independent opportunities, each with a small chance of success. Count the total successes. |
| **Distribution** | Poisson(λ) |
| **Random variable** | $X = \#$ of events occurring |
| **Parameter** | $\lambda = \sum p_i$ (average rate) |
| **Relation** | Limit of Binomial(n, p) when $n \to \infty$, $p \to 0$, $np = \lambda$; also limit of Poisson Binomial |
| **Real-world** | number of emails in an hour, mutations in a genome, Geiger counter clicks, customer arrivals in a minute |
| **Time model** | Counts per fixed interval; events are independent and rare |

### 4. Continuous Waiting (Poisson Process)

| | |
|---|---|
| **Story** | Events occur continuously and independently at a constant average rate $\lambda$. Measure the time between events. |
| **Distribution** | Exponential(λ) |
| **Key property** | Memoryless — $P(T > s+t \mid T > s) = P(T > t)$ |
| **Extension** | Wait for $r$ events: $\text{Gamma}(r, \lambda)$ |
| **Related** | Number of events in [0,t] is Poisson(λt) |
| **Real-world** | radioactive decay, bus arrival under constant rate, time between phone calls at a switchboard |
| **Time model** | Continuous, memoryless. Time does nothing (exponential) or time accumulates stages (Gamma). |

### 5. Additive Accumulation (Many Small Shocks)

| | |
|---|---|
| **Story** | A quantity is the sum of a large number of independent small contributions — none dominating. |
| **Distribution** | Normal(μ, σ²) |
| **Theorem** | Central Limit Theorem: if $X_i$ i.i.d. with mean μ, variance σ², then $\frac{\sqrt{n}(\bar{X}_n - \mu)}{\sigma} \xrightarrow{d} N(0,1)$ |
| **Real-world** | measurement error, height distribution, stock returns (approximately), any aggregate of many independent factors |
| **Time model** | No inherent time; it models the **equilibrium distribution** after enough accumulation |

### 6. Extreme (Min or Max of Many)

| | |
|---|---|
| **Story** | Observe many independent copies of a random variable; take only the largest (or smallest). |
| **Limit distributions** (Extreme Value Theory) | |
| Maximum of light-tailed variables | Gumbel |
| Maximum of Pareto-type (power-law tail) | Fréchet |
| Maximum of bounded variables | Weibull (for maxima of bounded) |
| **Real-world** | maximum flood level in 100 years, record temperature, strongest earthquake in a decade, smallest bolt in a batch |
| **Time model** | Time as the number of observations; extremes get more extreme as the sample grows |

### 7. Mixture / Composition

| | |
|---|---|
| **Story** | A process has two or more regimes, chosen randomly. First pick a regime, then generate data within that regime. |
| **Form** | $f(x) = \sum_{i=1}^k \pi_i f_i(x)$, where $\sum \pi_i = 1$ |
| **Examples** | |
| Continuous mixture | Normal mixture models, topic models |
| Hierarchical | Beta-Binomial (Beta prior on p, then Binomial data) |
| **Real-world** | population of heights from men and women (2-component Normal mixture), word topics in a document, customer segments |
| **Time model** | Time can be embedded in the mixing weights (switching between regimes) |

---

## Placements: Normal, Uniform, Hypergeometric

### Normal — CLT Attractor

Normal is not a separate process. It is the **Bernoulli process viewed at the limit of infinitely many steps**, after standardization. More broadly, it is the CLT attractor for **any** i.i.d. sum with finite variance — it has no native process and appears wherever aggregation happens.

| Common confusion | Correction |
|-----------------|-----------|
| "Normal is the distribution of everything" | ❌ — only aggregates. A single observation is rarely Normal. |
| "Normal is the default when you know mean and variance" | ✅ — maximum entropy under those constraints. |

### Uniform — Universal Source

Uniform does not arise from a temporal or counting process. It belongs to a different category: **the distribution of complete spatial / structural ignorance**.

```
Uniform Process
    │
    ├── "Pick a point randomly from an interval"       → Uniform(a, b)
    ├── "Pick a point randomly from a 2D region"       → Uniform over the region
    └── "No information except bounds"                 → Uniform(a, b) (max entropy)
```

Uniform(0,1) is also the **raw material** from which all other distributions are built via inverse transform: if $U \sim \text{Uniform}(0,1)$ and $F$ is a CDF, then $X = F^{-1}(U)$ has distribution $F$.

### Hypergeometric — Finite-Population Bernoulli

The Hypergeometric distribution is the **without-replacement analogue of Binomial**.

| | Binomial | Hypergeometric |
|-------------|---------|---------------|
| Population | Infinite (or infinite relative to sample) | **Finite** N |
| Sampling | With replacement (or equivalent — i.i.d. trials) | **Without replacement** |
| Trial dependence | Independent | **Dependent** — each draw changes the composition |
| Variance | $np(1-p)$ | $n\frac{K}{N}(1-\frac{K}{N})\frac{N-n}{N-1}$ |

Two key observations:
1. As $N \to \infty$, Hypergeometric → Binomial. The finite-population correction factor $\frac{N-n}{N-1}$ goes to 1, and the dependence vanishes.
2. As $n$ large, $K/N = p$ small, $np = \lambda$ — Hypergeometric → Poisson (rare-event limit, like Binomial).

---

## Composition and Derived Scenes

These are not atomic — they arise from transformation or composition of the atomic scenes.

| Derived scene | Parent atoms | How |
|--------------|-------------|-----|
| **Uniform(a,b)** | Complete ignorance | Maximum entropy on a bounded interval; can be transformed from Bernoulli(½) via infinite coin flips |
| **Beta(α,β)** | Prior for Bernoulli p | A distribution on probabilities; conjugate to Binomial |
| **Weibull(k,λ)** | Exponential | Power transform $T^\frac{1}{k}$ of Exponential; introduces aging |
| **Log-normal** | Normal | $e^X$ where $X \sim N(\mu,\sigma^2)$; multiplicative accumulation |
| **Pareto(α)** | Exponential mixture | $T \sim \text{Exp}(\Lambda)$ where $\Lambda \sim \text{Gamma}$; or $e^X$ for Exponential $X$ |
| **t distribution** | Normal + Chi-square | $Z / \sqrt{\chi^2_k / k}$ where $Z \sim N(0,1)$ |
| **F distribution** | Two Chi-squares | $(\chi^2_a / a) / (\chi^2_b / b)$ |
| **Cauchy** | Normal ratio | $X/Y$ where $X, Y \sim N(0,1)$; no expectation |
| **Order statistics** | Sorting n i.i.d. samples | Min, max, median, quantiles of a sample |

### The Composition Lattice

```
Atomic Scene ──→ Transform (g(X)) ──→ Derived scene
Atomic Scene ──→ Sum of i.i.d.  ──→ New distribution (CLT or Gamma sum)
Scene A ──→ Mixture with Scene B ──→ Multi-modal or hierarchical model
Scene A + Scene B ──→ Joint distribution ──→ Conditional → Regression/classification
Scene × Time ──→ Stochastic process ──→ Temporal dependence
```

---

## **Related**

[[Index of Probability]]
[[Probability System and Random Variables]]
[[Probability Spaces and the Universal Source]]
[[Universal Limit Theorems]]
[[Poisson Process and the Count-Waiting Duality]]
[[Memorylessness, Time and Aging]]