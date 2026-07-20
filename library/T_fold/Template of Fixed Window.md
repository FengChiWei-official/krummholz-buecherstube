---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text
```cpp
class Solution {
public:
    vector<int> findAnagrams(string s, string p) {
        if (s.size() < p.size()) return {};
        
        vector<int> p_cnt(26, 0); // 目標頻率
        vector<int> s_cnt(26, 0); // 窗口頻率
        vector<int> ans;

        // 1. 初始化：統計 p 的頻率
        for (char c : p) p_cnt[c - 'a']++;

        // 2. 開始滑動窗口
        for (int r = 0; r < s.size(); r++) {
            // 【進窗】：右指針進入，更新頻率
            s_cnt[s[r] - 'a']++;

            // 【出窗】：當窗口大小超過 p.size()，左指針必須移動
            // 這裡 left 隱式為 r - p.size() + 1
            if (r >= p.size()) {
                s_cnt[s[r - p.size()] - 'a']--;
            }

            // 【結算】：比較兩個頻率數組是否完全一致
            // vector 的 == 運算符已經重載過，會比較內容是否相同，複雜度 O(26)
            if (s_cnt == p_cnt) {
                ans.push_back(r - p.size() + 1);
            }
        }

        return ans;
    }
};
```



```cpp
vector<int> findAnagrams(string s, string p) {
    unordered_map<char, int> target;
    for (char c : p) target[c]++;
    
    unordered_map<char, int> window;
    int satisfy = 0; // 有多少種字符的數量已經完全匹配了
    vector<int> ans;

    for (int r = 0; r < s.size(); r++) {
        char cur = s[r];
        if (target.count(cur)) {
            window[cur]++;
            if (window[cur] == target[cur]) satisfy++;
        }

        if (r >= p.size()) {
            char out = s[r - p.size()];
            if (target.count(out)) {
                if (window[out] == target[out]) satisfy--;
                window[out]--;
            }
        }

        // 當滿足條件的字符種類數等於 target 的大小時，說明找到了
        if (satisfy == target.size()) {
            ans.push_back(r - p.size() + 1);
        }
    }
    return ans;
}

```

---

## Thoughts
[[Bucketing Chars]] -> [[Bucketing with Vector]]