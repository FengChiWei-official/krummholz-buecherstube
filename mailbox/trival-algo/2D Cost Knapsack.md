---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
---
In most cases, weight is a `1D` vector, however, sometimes it is more than `1d`.
## qwq

### Entities
- Item
	- weights: `[x, y, ...]`
	- value:
- Knapsack
	- capacity: `[x, y, ...]`
	- total_value:

### State Space
`Item ID * [x, y, ...]`
In most cases, I Shrimp it into `[x, y, ...]`.

### Template
``` cpp
//given
vector<int> items;

for (int z = 0; z < items.size(); z++) {
	int wm = items[z].get_m();
	int wn = items[z].get_n();
	for (int i = m; i >= wm; i--) {
		for (int j = n; j >= wn; j--) {
			dp[i][j] = max(dp[i][j], dp[i-wm][j-wn]+1);
		}
	}
}

return dp[m][n];
```


---
## **Related**：
[[474. Ones and Zeroes]]