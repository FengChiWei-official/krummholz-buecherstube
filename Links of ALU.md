---
aliases:
---

## Definition

[[Arithmetic Logic Unit|ALU]] computes on the quotient group

$$G=\mathbb Z/2^n\mathbb Z=\mathbb Z/M\mathbb Z,\qquad M=2^n.$$

Its output $F$ is a [[Section]] value: $F=s([x])$, a representative of the result class. The carry $c_{out}$ is the kernel coordinate relating the representatives chosen for the operands and for the result:

$$s(x)+s(y)+c_{in}=s(x+y+c_{in})+M\,c_{out}.$$

So the ALU computes two things at once: the class modulo $M$, and the lift defect $c_{out}$.

## Perspectives

**Integer layer — keeps the quotient**:

$$A+B+c_{in}=c_{out}M+F.$$

Here $A,B,F$ are the chosen representatives, and $c_{out}$ is the quotient.

**Congruence layer — drops the quotient**:

$$A+B+c_{in}\equiv F\pmod M.$$

Only the class remains; $c_{out}$ is discarded.

**Section**:

$$s([a])=\min\{a+kM\mid a+kM\ge0\}.$$

This is the least nonnegative representative. It is one possible section; the framework does not require it.

**Subtraction**:

$$-B\equiv M-B=\bar B+1\pmod M,\qquad \bar B=(M-1)-B,$$

so

$$A-B\equiv A+\bar B+1\pmod M.$$

At the integer layer:

$$A+\bar B+1=c_{out}M+F.$$

- $A\ge B$: $c_{out}=1$, $F=A-B$;
- $A<B$: $c_{out}=0$, $F=A-B+M$.

In the second case, $F$ is the least nonnegative representative; the signed value is $F-M=A-B$. The raw $F$ is not the signed true value.

## Distinctions

- **Integer vs congruence**: the integer equation keeps $c_{out}$; the congruence drops it.
- **Representative vs value**: $F$ is a section value, not necessarily a number with a fixed sign reading.
- **$c_{out}$ vs carry/borrow**: $c_{out}$ is the kernel coordinate of the section defect; “carry” or “borrow” are names for it under a particular section or instruction, not intrinsic.
- **No carry**: if $c_{out}=0$, the sum of the chosen representatives is already the section value of the result class:

$$A+\bar B+1=F.$$

This is expected for the least nonnegative section; it is unexpected only if one expects the balanced/signed representative $F-M$.

> The section defect and the 2-cocycle identity, with a concrete two-section example, are in [[Section]].

## Examples

$n=8$, $M=256$:

- $5-3$: $5+\bar 3+1=5+252+1=258=1\cdot256+2$; $c_{out}=1$, $F=2$.
- $3-5$: $3+\bar 5+1=3+250+1=254=0\cdot256+254$; $c_{out}=0$, $F=254$; the signed value is $254-256=-2$.

## Related

- [[Quotient Group]]: the result class lives in the quotient; $F$ represents it.
- [[Section]]: $F$ is a section value; $c_{out}$ measures the section defect.
- [[Additive Group of Integers]]: the integer lift is where the equation with $c_{out}$ lives.
- [[Group]]: the algebraic setting.
- [[Links of Additive Group of Integer]]: the integer-layer perspective.
- [[Links of Quotient Groups of Additive Group]]: the quotient-layer perspective.
