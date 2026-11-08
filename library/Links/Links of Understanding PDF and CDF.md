---
aliases:
---
## Definition

[[Probability measure]]

[[Random Variable]]

[[Cumulative Distribution Function|CDF]]

[[Probability Density Function|PDF]]

[[Linear Algebra]]

## Perspectives

### Measure and PDF

$P:\mathcal F\to[0,1]$ is a **set function**: input a set, output a number.

$\mathrm dP$ is not a second function. It is the infinitesimal element of the measure — the thing you integrate against: $\int h\,\mathrm dP$. When $P\ll\lambda$ it can be written in coordinates as $\mathrm dP=f\,\mathrm d\lambda$; when $P$ is atomic it cannot.

Pushing forward is available for **every** random variable, continuous or not:

$$
P_X:=P\circ X^{-1},\qquad P_X(B)=P\bigl(X^{-1}(B)\bigr).
$$

Continuity plays no role here; it only decides whether a density exists.

### PDF and CDF

The measure and the CDF are different types of object:

$$
F_X(x)=P_X\bigl((-\infty,x]\bigr)
$$

They determine each other, but one is a measure (set $\mapsto$ number) and the other a function (point $\mapsto$ number).

When $P_X\ll\lambda$, $F_X$ is differentiable a.e. and

$$
f_X=F_X'=\frac{\mathrm dP_X}{\mathrm d\lambda},\qquad P_X(\mathrm dx)=f_X(x)\,\mathrm dx .
$$

So $f_X$ is the **component** of $P_X$ in the Lebesgue "basis", and $f_X\,\mathrm dx$ is $P_X$ itself. The same picture as $v=v^i e_i$ in [[Linear Algebra]]: the component changes with the basis, the object does not.

## Distinctions

| | measure $P_X$ | density $f_X$ |
|---|---|---|
| input | set | point |
| reference measure needed | no | yes ($\lambda$) |
| existence | always | only if $P_X\ll\lambda$ |
| uniqueness | unique | a.e. unique |
| can exceed 1 | — | yes |

- $P_X$ vs $F_X$: measure vs function; $F_X$ is $P_X$ read on the halflines.
- $f_X$ vs $p_X$: **the same measure**, described against $\lambda$ vs against the counting measure $\#$.
- $F_X$ always exists; $f_X$ may not; when it does, $F_X'=f_X$ a.e.

## Examples

Take $\Omega=[0,1]^2$ with area measure $P$.

**A continuous case.** $X(\omega)=\omega_1$.

$$
P_X=\lambda,\qquad F_X(x)=x,\qquad f_X(x)=1,\qquad P_X\bigl((0.2,0.5]\bigr)=0.3
$$

All three descriptions agree: CDF difference, density integral, area of the vertical strip.

**A discrete case.** $\mathbf 1_A$ with $A=\{\omega_1>\omega_2\}$.

$$
P_{\mathbf 1_A}=\tfrac12\delta_0+\tfrac12\delta_1,\qquad
F \text{ is a step (jump } \tfrac12 \text{ at } 0 \text{ and } 1),\qquad
f \text{ does not exist}
$$

Same kind of object (a measure), no density; its components live under the counting measure instead.

---
## **Related**

[[Probability Density Function|PDF]]: the component of $P_X$ in the Lebesgue basis.
[[Cumulative Distribution Function|CDF]]: the same measure read on halflines.
[[Linear Algebra]]: the covector/component picture this card borrows.
