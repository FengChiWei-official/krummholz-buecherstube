---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
---

## qwq

## Prerequisites
### **Contiguous Data**
The data must be in a **linear and contiguous** structure. Sliding window only works on **subarrays** or **substrings**, not on "subsequences" (where elements can be picked from random positions).

## [[Monotonicity]]
The most important logical prerequisite, especially for **Variable-size Windows**, is **Monotonicity**.  
As you expand the window (add elements), the target metric (like sum, length, or count) must **only move in one direction** (increase or decrease).

- **Example:** In a "Maximum Sum" problem, adding a **positive number** must increase the total sum. If the array contains negative numbers, the sum isn't monotonic, and a simple sliding window might fail (you might need **Dynamic Programming** or **Prefix Sums** instead).

## Reversibility
You must be able to **efficiently update** the window's state when an element enters or leaves.

- When the `right` pointer moves, you **add** the new element.
- When the `left` pointer moves, you **subtract** or **remove** the old element.  
    If the calculation is "destructive" or cannot be reversed easily (e.g., finding the median of a window requires more complex data structures like a Heaps/Priority Queues), the sliding window becomes much harder to implement.

---
## **Related**：