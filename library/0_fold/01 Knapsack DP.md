---
tags:
  - type/permanent
  - topic/learning
  - attr/concept
  - status/evergreen
---

## Definition
### Entities
1. [[knapsack Item]]
	1. weight
	2. value
2. [[knapsack]]
	1. capacity
	2. value
### State Space

dimension is `object * capacity(may be n dimension)`

| Object ID\|Remain Space | 0   | 1   | 2     | ... | Kn Capacity |
| ----------------------- | --- | --- | ----- | --- | ----------- |
| void object             | 0   | 0   | 0     | 0   | 0           |
| Object 1                | 0   |     |       |     |             |
| Object 2                | 0   |     |       |     |             |
| Object i                | 0   |     | Value |     |             |
| ...                     | 0   |     |       |     |             |
| Object n                | 0   |     |       |     |             |
## Transition
`dp[i] = max(dp[i], dp[i-w_cur]+v_cur)`
Its logic is **Choice or not**.
## Type

[[01 Knapsack DP Classes]] 


---
## **Related**：
### Belonging
[[Knapsack DP]]
