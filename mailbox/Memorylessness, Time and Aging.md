---
tags:
  - type/permanent
  - status/in-progress
  - attr/concept
  - topic/math
---

> **Historical station**: the theory of waiting times, born of actuarial science (Gompertz) and the Poisson process. Only Exponential (continuous) and Geometric (discrete) forget the past; every other waiting-time distribution is a claim about how time leaves its mark — modeled through the hazard function.

## Definition

**Memorylessness** (or the "forgetfulness property") means:

$$
P(X > s + t \mid X > s) = P(X > t), \quad \forall s, t \ge 0
$$

The probability of surviving an additional $t$ units, given you've already survived $s$ units, is exactly the same as surviving $t$ units from the start. **The process does not "remember" how long it has already been running.**

For discrete waiting times (number of trials):

$$
P(X > n + m \mid X > n) = P(X > m), \quad \forall n, m \ge 0
$$

### Why memorylessness matters

| Context | What memorylessness implies |
|---------|---------------------------|
| Radioactive decay | One atom: probability of decay in the next second is constant, regardless of atom age |
| Customer waiting | The time until the next bus arrival does not depend on when the last bus left |
| Network packets | The residual time of a packet transmission does not depend on how long it has already been transmitting |
| Machine failure | A lightbulb that is "memoryless" is no more likely to fail tomorrow than a brand-new one |

---

## The Uniqueness

The survival function $S(t) = P(X > t)$ satisfies the functional equation:

$$
S(s + t) = S(s) S(t), \quad \forall s, t \ge 0
$$

This is **Cauchy's exponential equation**. The only non-negative, non-constant solutions are:

| Domain | Only memoryless distribution | Survival function |
|--------|------------------------------|-------------------|
| Continuous, non-negative | **Exponential**(λ) | $S(t) = e^{-\lambda t}$ |
| Discrete, positive integers | **Geometric**(p) | $S(n) = (1-p)^n$ |

### Proof sketch

The survival function $S(t) = P(X > t)$ satisfies $S(s + t) = S(s) S(t)$ for all $s, t \ge 0$. Under mild regularity (monotonicity), the only continuous solutions are $S(t) = e^{-\lambda t}$, giving the Exponential distribution. In the discrete case with $S(n) = P(X > n)$, the equation forces $S(n) = (1-p)^n$, giving the Geometric distribution.

### Near-misses

| Distribution | Memoryless? | Why not |
|-------------|-------------|---------|
| **Weibull**(shape=1) | ✅ | It's Exponential |
| **Weibull**(shape≠1) | ❌ | $S(t) = e^{-(\lambda t)^k}$; $S(s+t) \neq S(s)S(t)$ |
| **Gamma**(shape=r≠1) | ❌ | Sum of r Exponentials: mixing introduces memory |
| **Pareto** | ❌ | Heavy tail: $S(s+t) = c(s+t)^{-\alpha} \ne c s^{-\alpha} \cdot c t^{-\alpha}$ |
| **Negative Binomial**(r≠1) | ❌ | Sum of r Geometrics; the waiting time for the r-th success remembers how many successes have occurred |

**The only memoryless distribution is Exponential (continuous) or Geometric (discrete).** All other distributions either "age" (hazard rate increases/decreases) or "accumulate evidence."

Memorylessness is an extremely strong assumption. When you model with Exponential, you are asserting: **this process has no internal clock, no wear, no learning, no fatigue.** That is appropriate for radioactive decay, Poisson arrivals, and thermal noise — but rarely for biological or mechanical systems.

---

## The Hazard Function

Waiting-time distributions are characterized not by their PDF or CDF alone, but by their **hazard function** (failure rate, force of mortality):

$$
\lambda(t) = \lim_{\Delta t \to 0} \frac{P(t \le T < t + \Delta t \mid T \ge t)}{\Delta t} = \frac{f(t)}{S(t)}
$$

$\lambda(t)$ answers: *"Given it has survived to time $t$, how likely is it to fail in the next instant?"*

| Hazard shape | Meaning | What time does |
|-------------|---------|---------------|
| **Constant** $\lambda(t) = \lambda$ | No aging. The probability of failing in the next instant is independent of age. | **Time does nothing.** |
| **Increasing** $\lambda'(t) > 0$ | Aging / wear-out. The older the unit, the more likely it fails now. | **Time accumulates damage.** |
| **Decreasing** $\lambda'(t) < 0$ | Burn-in / infant mortality. The longer it survives, the less likely it is to fail. | **Time screens out weak units.** |
| **Bathtub** (↓ then → then ↑) | Initial defects wear off, stable period, then aging. | **Three regimes — real-world most common.** |

### The map of waiting-time distributions

| Distribution | Hazard $\lambda(t)$ | What time does | Typical real-world scenario |
|-------------|--------------------|----------------|---------------------------|
| **Exponential**(λ) | constant λ | **Nothing.** No aging. | Radioactive decay, Poisson arrivals, completely random failure |
| **Weibull**(shape=k>1) | $k \lambda (\lambda t)^{k-1}$, increasing | **Aging.** Wear accumulates. | Mechanical fatigue, bearing wear |
| **Weibull**(shape=k<1) | $k \lambda (\lambda t)^{k-1}$, decreasing | **Burn-in.** Weak ones die early. | Electronics early failures, startup mortality |
| **Gamma**(r, λ) | starts at 0, increases to λ | **Learning phase** then stabilizes. | System with r-stage preparation; r=1 is Exponential |
| **Log-normal** | increases then decreases (non-monotonic) | **Complex aging.** Failure rate peaks then drops. | Crack growth, some biological processes |
| **Pareto**(α) | $\alpha / t$, decreasing | **Always improving** (rich-get-richer). | Earthquake sizes, wealth distribution, file sizes |
| **Gompertz** | $a e^{bt}$, accelerating | **Accelerating aging.** | Human mortality (after ~30) |
| **Geometric**(p) | constant (discrete) | No aging (discrete version). | Number of Bernoulli trials until first success |

---

## Distributions and Their Time

Each distribution models not just "amount of time" but *how time works* in the system:

| Distribution | Its implicit theory of time |
|-------------|---------------------------|
| Exponential | Time is a constant-rate ticking. Duration is irrelevant; the process has no history. |
| Weibull(k>1) | Time is a destructive force. The longer you wait, the harder it hits. |
| Gamma(r,λ) | Time is a series of stages. You cannot finish until all r sub-tasks are done. |
| Log-normal | Time has multiplicative noise. Progress accumulates by multiplying random factors. |
| Pareto | Time doesn't age you — it gives you advantage. The longer you've survived, the longer you'll keep surviving. |

### How they are generated from atomic building blocks

```
Exponential(λ) ──(power transformation)──→ Weibull(k, λ)
Exponential(λ) ──(sum of r i.i.d.)──→ Gamma(r, λ)
Exponential(λ) ──(min of n i.i.d.)──→ Exponential(nλ) (faster, still memoryless)
Exponential(λ) ──(max of n i.i.d.)──→ not Exponential anymore (memory emerges!)
Gamma(r, λ) ──(scale mixing)──→ Pareto (if mixing with another Gamma)
Exponential + randomness in λ ──→ Pareto / Log-normal (mixtures create memory)
```

**Aging emerges from transformation or composition.** The Exponential atom itself is "time-neutral." Combine it, transform it, mix it — and time becomes meaningful.

---

## Why It Matters

### Markov property

Memorylessness gives you the **Markov property**:

$$
P(X_{n+1} \mid X_n, X_{n-1}, ..., X_0) = P(X_{n+1} \mid X_n)
$$

The past is irrelevant beyond the present state. Continuous-time Markov chains rely on Exponential holding times between transitions — precisely because memorylessness lets you "forget" when the chain entered the current state.

### Poisson process anchor

The Poisson process is memoryless because its inter-arrival times are Exponential. This makes the process Markovian — the future depends only on the present count, not on the entire arrival history. Without memorylessness, the Poisson process would not be "Poisson": the independent-increments property would break.

### Scene-specificity

Probability theory is deeply **scene-specific** (高度场景化). Every distribution encodes a commitment about how the world works; the choice is not mathematical but semantic.

```
Real-world process  →  Choose a generative story  →  Pick a distribution  →  Work with the math
```

Three people modeling "time until a machine fails" might pick three different distributions — because they disagree about what time does:

| Person | Belief | Distribution chosen |
|--------|--------|-------------------|
| A | The machine has no moving parts; failure is random shock. | Exponential |
| B | The machine wears out. | Weibull(shape=2) |
| C | The machine has an initial defect that might show early; otherwise stable. | Weibull(shape=0.8) then constant |

A probabilist who only knows formulas but cannot match them to scenarios is **mechanically fluent but semantically blind.** The hardest part of probability is not the math — it's deciding *which* math applies to *this* situation.

---

## **Related**

[[Index of Probability]]
[[Probability System and Random Variables]]
[[Probability Spaces and the Universal Source]]
[[The Scenes and Processes of Probability]]
[[Universal Limit Theorems]]
[[Poisson Process and the Count-Waiting Duality]]