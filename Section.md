---
aliases:
---

## Definition

A **section** of the quotient map

$$\rho:\mathbb Z\longrightarrow G=\mathbb Z/M\mathbb Z$$

is a map $s:G\to\mathbb Z$ with

$$\rho\circ s=\mathrm{id}_G.$$

It chooses one representative per coset.

The **section defect** of $x,y\in G$ is the unique integer $c_{out}$ such that

$$s(x)+s(y)=s(x+y)+M c_{out}.$$

Equivalently,

$$c_{out}=\frac{s(x)+s(y)-s(x+y)}{M}.$$

It is a 2-cocycle: associativity gives

$$c_{out}(x,y)+c_{out}(x+y,z)=c_{out}(y,z)+c_{out}(x,y+z).$$

## Example

Take $n=4$, $M=16$, $x=5$, $y=6$; then $x+y=11$.

| section | $s(5)$ | $s(6)$ | $s(11)$ | $s(5)+s(6)-s(11)$ | $c_{out}$ |
|---|---|---|---|---|---|
| least nonnegative | 5 | 6 | 11 | 0 | 0 |
| balanced | 5 | 6 | -5 | 16 | 1 |

The bit pattern of the result is `1011` in both readings. The raw ALU adder produces `1011` with carry-out $0$; that is the cocycle of the least nonnegative section. If the same bits are read with the balanced section, the section defect is $1$; the physical carry is still $0$.

The transition is $s_{\mathrm{bal}}=s_0+M\beta$ with $\beta(5)=\beta(6)=0$ and $\beta(11)=-1$, so

$$c_{out}^{\mathrm{bal}}
=c_{out}^{0}+\beta(5)+\beta(6)-\beta(11)
=0+0+0-(-1)=1.$$

So $c_{out}$ is not a function of the class alone; it is the kernel coordinate relative to the section. The class and the bit pattern can stay the same while the section defect changes.

## **Related**

[[Quotient Group]]: A map about it.
