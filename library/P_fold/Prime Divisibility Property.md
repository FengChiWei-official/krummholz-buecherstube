---
tags:
  - type/permanent
  - attr/principle
  - topic/learning
  - status/in-progress
aliases:
  - Euclid's Lemma
---

#principle #math/algebra/abstract 
## Definition
### given
- $p$ is a prime.
- $a, b$ are integers
### premise
$p$ divides $ab$,
### conclusion:
$p$ divides $a$ or $p$ divides b.

## Proof
### Lemma
Lemma1[^1]: [[Characterization of GCD via Linear Combinations|The Bézout Identity for Integers]]
### Steps
suppose $p$ cannot divide $a$.
> one of them, $a$ and $b$ are equal here. 

Considering set $\mathbb{Z}k = \mathbb{Z}a + \mathbb{Z}p$, for Lemma1[^1] , 
Howe get $\exists r, s \in \mathbb{Z} \text{ s.t. } ra+sp = 1$.
therefore, $rab + spb = b$. 
therefore, $rmp+sbp = b \to (rm+sb)p = b$
so, p is a factor of b.

## technique
[[构造法]]
[[]]

---
## **Related**
[^1]: [[Characterization of GCD via Linear Combinations]]
