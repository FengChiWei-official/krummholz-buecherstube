---
tags:
  - type/permanent
  - attr/principle
  - topic/learning
  - status/evergreen
---
### Key Points
- [[Contiguous]]:  Subarray,yes; subsequence, no.
- [[Monotonicity in PC]], when you expand your window, your state shift should be [[Monotonicity in PC]].
	- i.e.  for (array, max subarray), you get a **minus integer**, your algorithm will collapse.
- [[Reversibility]]: operation for **in and out** should be low cost.

## Template
### Principles
1. initialize the window outside the loop
2. update the window, when window **expand**, **not failed**.

[[Template of Sliding Window]]
> i.e. [[1438. Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit]]

[[Template of Fixed Window]]

---
## **Related**：
