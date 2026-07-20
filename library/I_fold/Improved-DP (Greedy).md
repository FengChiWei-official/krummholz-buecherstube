---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text
### Improved-DP (Greedy)

| Index | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1     | 10  | 4   | 4   | 2   | 2   | 2   | 1   | 1   |
| 2     |     |     | 5   | 5   | 3   | 3   | 3   | 3   |
| 3     |     |     |     |     |     | 7   | 7   | 7   |
| 4     |     |     |     |     |     |     |     | 18  |
| No.   | 10  | 4   | 5   | 2   | 3   | 7   | 1   | 18  |

- data: `Tails`
	- `tails[i]` is Minimal number that is an end of `i-length`subsequence.
- example: 
	- `step 5`: 
		- tails($[2,5]$) means the are 2 available subsequence:
			- $[2]$
			- $[x, 5]$ // May not 2(I mean `tails[0]`)
		- `nums[5]=3` $2>3>5$
			- you can imply that there are [2,3] that can replace `5`


### Tips
You should do **Lower Bound**  for each element in **tails**. And then, do case analyse with
1. case 1(found) replace 
2. and case 2(not found) push_back.
> [!tips] 
> Lower Bound means you cannot make your `tails` to be $[1, 2, 2]$.
> When you meet variance--(non-decreasing subsequence), you should replace it with **Upper Bound**.



---

## Thoughts
