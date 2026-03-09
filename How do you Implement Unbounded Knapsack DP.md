---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---


## Definition (完全背包版)

## Step 1: Draw your Knapsack

1. What is your [[knapsack Item]] (每個物品有 無限個)
2. Draw your [[knapsack]] in a table of $\text{ID} \times \text{Weight Vector} \to \text{Value}$

## Step 2: Implement the template

```cpp
// 假設有 n 個維度，這裡以 2 維完全背包為例
// items: 存放物品的向量
// dim_1, dim_2: 各個維度的最大容量上限

// 1. 初始化 DP 陣列
// **NOTE-1** dp 维度記得 +1
vector<vector<int>> dp(dim_1 + 1, vector<int>(dim_2 + 1, 0));

// 2. 遍歷所有物品
for (int id = 0; id < items.size(); id++) {
    Item cur = items[id];
    int cur_w1 = cur.weight1; 
    int cur_w2 = cur.weight2; 
    int cur_val = cur.value;  

    // 3. 正序遍歷維度 (完全背包核心：允許在同一個物品下重複選取)
    // 從物品重量開始「從小到大」遍歷
    for (int i = cur_w1; i <= dim_1; i++) {
        //**NOTE-3** j 從 cur_w2 開始，且包含等於
        for (int j = cur_w2; j <= dim_2; j++) {
            // 狀態轉移方程：
            // 此時 dp[i - cur_w1][j - cur_w2] 可能已經包含過當前物品
            //**NOTE-4** 加上 cur_val 達成累加效果
            dp[i][j] = max(dp[i][j], dp[i - cur_w1][j - cur_w2] + cur_val);
        }
    }
}
```

> [!tip]  
> 完全背包與 0/1 背包的關鍵差異：
> 
> - 0/1 背包：內層迴圈逆序（從 `dim` 到 `cur_w`），確保每個物品只被選取 一次。
> - 完全背包：內層迴圈正序（從 `cur_w` 到 `dim`），利用已更新的狀態達成 無限次 選取。

> [!note]  
> 常見錯誤補充：
> 
> 1. 初始化值：如果題目要求「恰好裝滿」，`dp[0][0]` 應設為 0，其餘設為 `-INF`。
> 2. 遍歷順序：在多維完全背包中，所有限制維度（i 和 j）都必須是正序遍歷。
> 3. 溢出風險：若 `cur_val` 很大或求方案數時，注意 `int` 是否會溢出（需用 `long long`）。

---

## Related

