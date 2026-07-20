---
tags:
  - status/evergreen
---

# Algorithm
## Recognition

  

If you see a problem like this:

$$ result = op^{d}(x) $$

Here $d$ is an integer, so $d$ can be separated into base-$n$ digits; for example, $7 = [1,1,1]_2$.

  

From the point of view of algebra, we can say that this is the exponentiation of an operation (one with **associativity** and **identity**), i.e. repeated application of the operation.

  

## What it can do

  

It computes exponentiation efficiently, reducing the time complexity from $O(n)$ to $O(\log n)$.

## From
[[Additive Group of Integers]]
