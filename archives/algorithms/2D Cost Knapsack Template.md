---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text
``` cpp
//given
vector<Item> items;

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

## Thoughts
