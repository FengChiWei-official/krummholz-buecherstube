---
tags:
  - type/permanent
  - attr/principle
  - topic/learning
  - status/in-progress
---

## Definition
let a, b **not both 0**,  $d = \gcd (a, b)$, 
$\mathbf{S} = \mathbb{Z}a + \mathbb{Z}b$, so $\mathbb{Z}d = \mathbb{Z}a + \mathbb{Z}b$.
> [!note]
> Equals to [[Subgroup Generation Theorem for the Integer Additive Group|Zd = Za + Zb]]
> Note: You cannot use gcd's properties, for they are not defined yet.

then:
$$
	\begin{align}
	&\text{(a) }\text{d divides a and b} \\
	&\text{(b) }\text{if an integer e divides both a and b, it also divides d} \\
	&\text{(c) }\text{There are integers r and s such that} \quad d = ra + sb
	\end{align}
$$
---
## **Proof**
### Basis
[[The Cyclic Decomposition Theorem for Subgroups of the Addition Group of Integers|**Lemm 1**: The Cyclic Decomposition Theorem]].

**Lemm 2** : $e | a, e | b \to e | ra+sb,\quad r,s \in \mathbb{Z}$ proof[^1]
### Premise
$$
\exists d \quad s.t. \\
\mathbb{Z}d = \mathbb{Z}a + \mathbb{Z}b = \mathbf{S}
$$
$$
\text{Let }d := \gcd (a, b)
$$
### Conclusion
$$
\begin{align}
(a) \quad & d\mid a \quad \text{and} \quad d\mid b, \\
(b) \quad& \forall e, \text{ s.t. } e\mid a \text{ and }e\mid b \to e\mid d, \\
(c) \quad&d = ra + sb.
\end{align}
$$
### Tech 
[[Based on Definition]]

[[how to prove a element is greatest one in a set]]

### Roadmap
1. For **Lemma 1** and Premise -> d = ra + sb
2. $\{a, b\} \subset \mathbf{S} \to \exists k_1, k_2, \text{ s.t. } k_1d=a, k_2d=b$ 
3. For (c) and **Lemma2**[^1] $e \mid d$

[^1]:  following
> [!tip]
> divide equals to modulo($a\mid b \quad \cong \quad b \equiv 0 \pmod a$) 
> $$
> \begin{align}
> &given: \\
> & && a \equiv 0 \pmod e，\\
> & && b \equiv 0 \pmod e \\
> &\forall r, s \in \mathbb{Z},\\
> & && ra \equiv 0 \pmod e \\
> &  && sb \equiv 0 \pmod e \\
> & \text{Thus:} \\
> & && ra+sb \equiv 0 \pmod e
> \end{align}
> $$

