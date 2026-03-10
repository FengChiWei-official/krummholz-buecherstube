---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/concept
---

## Definition

A [[Stack]] where elements are always in a specific order.

## Operations
> The same as Stack.

### Push
Complexity is $O(1)$. 
> [!note]
> push might break monotonic. So the key of Implementing push is KEEPing its Monotonicity.
> 

Push operates in Such a way **POP all non-monotonic elements** then push.

### PoP
Nothing.


## How do It work?
### For area culculation
主要作用就是确定左右侧的最近的较大/较小值。
蕴含着定一动一思想。


## Check List
- [ ] What kind of elements it is? -> **Index**
- [ ] Pop marginal condition? 
- [ ] Empty Check? 
- [ ] Sentinels? no need.
- [ ] Stack breaks order, so you should 

> [!tip]
> **Since a monotonic stack processes elements out of their original order, you should assign values to the answer array by index instead of using `push_back`.**




---
## **Related**

### Classic Problems


- [[901. Online Stock Span]] todo
- [[Next Greater Elements]]
- [[84. Largest Rectangle in Histogram]]
- [[42. Trapping Rain Water]]
- [[739. Daily Temperatures]]



