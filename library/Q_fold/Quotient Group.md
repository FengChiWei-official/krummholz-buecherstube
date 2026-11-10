## Definition

### Notation

$$
Q = G/H
$$
where $G$ is a Group and $H$ is a [[Normal Subgroup]] of $G$($H \vartriangleleft G$).

> [!why]
>  Why we need $H$ to be a [[Normal Subgroup]]?
>  We need to define the new operation well.
>  





### Element

Each element of a [[Quotient Group]] is a [[Coset]].

$Q = \{aH|\forall a \in G, H \vartriangleleft G \}$
However,  $\exists a, b, aH \equiv bH$.

### Operation

$+ :=  aH + bH = (ab)H$

[[Well Define]]: We need to guarantee that :
$\forall a^{\prime}, !\exists , \; a^{\prime} = ag \in aH$,
$a^{\prime} H + bH = (a^{\prime}b)H$,
we get:
$(a^{\prime}b)H \equiv (ab)H$.

#### How?

$(a^{\prime}+b)H = (agb)H = \{agbv| \forall v \in H \}$

if $H$ is a [[Normal Subgroup]], then, we [[Conjugate]]$C_a(x)$.
$\{agbv| \forall v \in H \} = \{agb| \forall v \in H \}$
### EG


```
Z+ = {0, -1, +1, -2, +2...}, +
Normal Subgroup 4Z+ = {4*0, 4*-1, 4*+1, 4*-2, 4*+2...}, +
Cyclic Subgroup: {},+
Cosets: 
	0(4Z+) = 4(4Z+) = 8(4Z+) = {4*0, 4*-1, 4*+1, 4*-2, 4*+2...}, +
	1(4Z+) = {1+4*0, 1+4*-1, 1+4*+1, 1+4*-2, 1+4*+2...}, +
	2(4Z+) = {2+4*0, 2+4*-1, 2+4*+1, 2+4*-2, 2+4*+2...}, +
	3(4Z+) = {3+4*0, 3+4*-1, 3+4*+1, 3+4*-2, 3+4*+2...}, +
Quotient Group
Z/4 = {0(4Z+), 1(4Z+), 2(4Z+), 3(4Z+)}	
+ of Z/4 : a4Z + b4Z = (a+b)4Z
```




---
## **Related**

[[Lagrange's Theorem]]: Size counter.
[[Fundamental Homomorphism Theorem|First Isomorphism Theorem]]: Tells you how to find a operatable representation.
[[Correspondence Theorem|The Fourth Isomorphism Theorem]]: Tell you what is the structure of a quotient group.
