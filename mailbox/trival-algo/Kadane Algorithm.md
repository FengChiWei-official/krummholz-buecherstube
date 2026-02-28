---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
---
it is a [[Dynamic Programming|DP]] algorithm

## Defines
Given input `nums`.

`dp` is state variable, standing for max sum of i-end subarray.
> 1 2 3 4 -> `dp` in index 3 is 6(of `1 2 3`, `2 3`, `3`)

`cur` is current value of index `i`.

`ans` is max value of `dp`.

## Transition
`dp = max(cur, dp+cur)`

## Steps
Traversal all in nums, update `dp` and then update `ans`.

---
## **Related**：
[[53. Maximum Subarray]]
