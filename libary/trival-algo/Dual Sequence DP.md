---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
aliases:
  - LCS-like DP
---

## qwq

Index of DP is current prefix length of each Sequence.
The transfer logic is 
1. Check `A[i] == B[j]`
	1. case yes: `A[0:i]` and `B[0:j]` have no need to be consider.
	2. case no: `A[i], B[j]`should consider their Prefix.

---
## **Related**：