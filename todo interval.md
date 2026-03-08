---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text

這份 C++ 模板將這兩類問題的「骨架」提取出來，你會發現邏輯高度對稱。

## 1. C++ 模板對比

## 【類型 A：求最大不重疊數量】（LC 435 / 452）

核心：按右端點排序，騰出空間。

```cpp
int eraseOverlapIntervals(vector<vector<int>>& intervals) {
    if (intervals.empty()) return 0;

    // 1. 貪心策略：按右端點 (end) 升序
    sort(intervals.begin(), intervals.end(), [](const vector<int>& a, const vector<int>& b) {
        return a[1] < b[1]; 
    });

    int count = 1; // 最大不重疊區間數
    int end = intervals[0][1];

    for (int i = 1; i < intervals.size(); ++i) {
        // 2. 如果下一個的起點 >= 當前的終點，說明不重疊
        if (intervals[i][0] >= end) {
            count++;
            end = intervals[i][1]; // 更新邊界
        }
    }
    return intervals.size() - count; // 總數減去保留數 = 移除數
}
```

## 【類型 B：合併區間】（LC 56）

核心：按左端點排序，順序掃描。

```cpp
vector<vector<int>> merge(vector<vector<int>>& intervals) {
    if (intervals.empty()) return {};

    // 1. 策略：按左端點 (start) 升序
    sort(intervals.begin(), intervals.end()); // vector 預設按第一個元素排

    vector<vector<int>> merged;
    for (const auto& interval : intervals) {
        // 2. 如果結果為空或不重疊，直接加入
        if (merged.empty() || interval[0] > merged.back()[1]) {
            merged.push_back(interval);
        } else {
            // 3. 重疊，更新前一個的終點為兩者最大值
            merged.back()[1] = max(merged.back()[1], interval[1]);
        }
    }
    return merged;
}
```

---

## 2. 題型識別：一眼看穿本質

在刷題時，看到以下特徵即可快速歸類：

1. 「最多/最少」+「不重疊」 $\rightarrow$ 類型 A
    
    - _識別語：_ 「最多能參加多少活動」、「最少移除多少區間」、「最少用幾隻箭」。
    - _解法：_ 右端點排序，選結束早的。
    
2. 「覆蓋」+「範圍合併」 $\rightarrow$ 類型 B
    
    - _識別語：_ 「合併所有重疊區間」、「求覆蓋後的總長度」。
    - _解法：_ 左端點排序，一路向右推。
    
3. 「資源佔用」+「並發數」 $\rightarrow$ 類型 C（隱藏題型）
    
    - _識別語：_ 「最少需要多少間會議室」、「車站最少需要多少月台」。
    - _解法：_ 這種通常要把 Start 和 End 分開排序，或使用 最小堆 (Priority Queue)。
    

---

## 3. 為什麼區間題是「難點」？

很多同學覺得區間題難，是因為它有兩個容易踩坑的地方：

- 邊界的開閉（$<$ 還是 $\le$？）
    
    - 題目會說「邊界接觸算重疊」還是「不算」。例如氣球題（452）邊界接觸也算爆，所以判斷條件會變。
    
- 排序維度的選擇
    
    - 如果右端點相同，左端點要怎麼排？在基礎的 435 題中，右端點排好後，左端點順序其實不影響結果，但在更複雜的題目（如 LC 1353 最多參加活動）中，細節就很關鍵。
    

如果你想挑戰最後的大 BOSS：  
我可以解釋 「LC 1024. 影片拼接」 這種「用最少區間覆蓋 [0, T] 區間」的問題，它是區間類題目中最難的一種貪心邏輯。

你準備好挑戰最難的「區間覆蓋」邏輯，還是先去練習 452 題鞏固一下？


---

## Thoughts