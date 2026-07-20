---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/technique
---

## Definition

$$\prod_{k=0}^{n-1} \cos(2^k x) = \frac{\sin(2^n x)}{2^n \sin x}$$

如果你将两侧同时乘以 $2^n \sin x$，它就变成了一个**连锁递归**过程：
*   $\cos(x) \sin(x) = \frac{1}{2} \sin(2x)$
*   $(\frac{1}{2} \sin(2x)) \cos(2x) = \frac{1}{4} \sin(4x)$
*   $(\frac{1}{4} \sin(4x)) \cos(4x) = \frac{1}{8} \sin(8x)$

---
## **Related**