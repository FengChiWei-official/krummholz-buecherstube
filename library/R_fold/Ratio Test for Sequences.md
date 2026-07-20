---
tags:
  - type/permanent
  - status/in-progress
  - topic/learning
  - attr/concept
---

## Definition

Given a sequence $\{x_n\}$ with **positive terms** ($x_n > 0$):  
Suppose the limit of the ratio of consecutive terms is $L$:  
$$\lim_{n \to \infty} \frac{x_{n+1}}{x_n} = L$$

> [!note]
> The sequence is **asymptotically geometric**.
> Let $a_{n+1} = k a_n + q$

- If $L < 1$: The sequence converges to zero ($\lim_{n \to \infty} x_n = 0$). 
	- $x_n$~$a_n$, where $k < 1$. 
- If $L > 1$: The sequence diverges to infinity ($\lim_{n \to \infty} x_n = \infty$).
- If $L = 1$: The test is inconclusive (判别失效).

---
## **Related**