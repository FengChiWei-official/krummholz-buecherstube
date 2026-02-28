---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
---

## qwq

``` cpp

vector<int> a, b;
int dp_a = a.size+1;
int dp_b = b.size+1;
vector<vector<int>> dp(dp_a, vector<int>(dp_b, 0));

// init: 1st one(a dummy node)
dp[0][0] = init_dp();
// init: 1st line(a dummy line)
for (int j = 1; j < dp_b; j++) {
	int current_b = b[j-1]; // handle 0-base index(centralized)
	int prev_b = b[j-k]; // k are vary for case to case.
	
	if (f(current_b,prev_b)) {
		dp[0][j] = trans_1_1(dp[0][j-k]);
	}
	else {
		dp[0][j] = trans_1_2([0][j-k]);
	}
}

for (int j = 1; j < dp_b; j++) {
	for (int i = 1; j < dp_a; i++) {
		int current_b = b[j-1]; // handle 0-base index(centralized)
		int prev_b = b[j-k]; // k are vary for case to case.
		int current_a = a[j-1]; // handle 0-base index(centralized)
		int prev_a = a[j-k]; // k are vary for case to case.
		pass;	
	}
}

return dp[dp_a-1][dp_b-1];
```


---
## **Related**：