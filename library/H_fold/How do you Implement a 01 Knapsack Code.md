---
tags:
  - type/permanent
  - topic/learning
  - attr/technique
  - status/in-progress
---

## Definition

### Step 1: Draw you Knapsack
1. What is your [[knapsack Item]]
2. Draw your [[knapsack]] in a table of $\text{ID} \times \text{Weight Vector} \to \text{Value}$ 
### Step 2: Implement the template
``` cpp
// 假設有 n 個維度，這裡以 2 維背包為例
// items: 存放物品的向量
// dim_1, dim_2: 各個維度的最大容量上限

// 1. 初始化 DP 陣列
// 使用二維向量，dp[i][j] 表示在第一維容量為 i、第二維容量為 j 時的最大價值
// **NOTE-1**
vector<vector<int>> dp(dim_1 + 1, vector<int>(dim_2 + 1, 0));

// 2. 遍歷所有物品
for (int id = 0; id < items.size(); id++) {
    Item cur = items[id];
    int cur_w1 = cur.weight1; // 取得物品在維度 1 的消耗
    int cur_w2 = cur.weight2; // 取得物品在維度 2 的消耗
    int cur_val = cur.value;  // 物品本身的價值

    // 3. 逆序遍歷維度 (為了節省空間複雜度，使用一維/二維滾動陣列避開重複計算)
    for (int i = dim_1; i >= cur_w1; i--) {
	    //**NOTE-3**
        for (int j = dim_2; j >= cur_w2; j--) {
            // 狀態轉移方程：考慮「不放入」與「放入」當前物品
            //**NOTE-4** 不要忘记选择item时，加上item的value.
            dp[i][j] = max(dp[i][j], dp[i - cur_w1][j - cur_w2] + cur_val);
        }
    }
}


```

> [!note] 
> 常见错误有：
> 1. dp 维度忘记 `+1`
> 2. cur 有可能 `-1`
> 3. j >= cur_w2 要取等号
> 4. 不要忘记选择item时，加上item的value.

---
## **Related**
