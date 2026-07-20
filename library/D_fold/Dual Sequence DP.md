---
tags:
  - type/permanent
  - attr/principle
  - topic/learning
  - status/evergreen
aliases:
  - LCS-like DP
---

## qwq

Index of DP is current prefix length of each Sequence.
The transfer logic is 
1. Check `A[i] == B[j]`
	1. case yes: `A[0:i]` and `B[0:j]` have no need to be consider.
		1. look at the following table that you will find it is one of the best solution
	2. case no: `A[i], B[j]`should consider their Prefix.
		1. (`A[0:i]` and `B[0:j-1]`) or (`A[0:i-1]` and `B[0:j]`)


|      |           |                   |     |
| ---- | --------- | ----------------- | --- |
|      | i2-1      | i2                |     |
| i1-1 | basis     | basis(+1)         |     |
| i1   | basis(+1) | current=basis(+1) |     |

$dp[i1-1][i2-1] \le (dp[i1-1][i2], dp[i1][i2-1]) \le dp[i1][i2]$

---
## **Related**：

### Example
standard
[[1143. Longest Common Subsequence]]
[[583. Delete Operation for Two Strings]]

continuous
[[718. Maximum Length of Repeated Subarray]]