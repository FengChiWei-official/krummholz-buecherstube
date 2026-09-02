---
tags:
  - type/lit
  - topic/learning
  - status/archive
---

## Text

``` cpp
class Solution {

public:

bool isMatch(string s, string p) {

int m = s.size();

int n = p.size();

// dp[i][j] 表示: s 的前 i 个字符 (长度为 i) 和 p 的前 j 个字符 (长度为 j) 是否匹配

// 因此 dp 的大小需要是 (m+1) * (n+1)

vector<vector<bool>> dp(m + 1, vector<bool>(n + 1, false));

  

// 1. Base Case: 两个空字符串是匹配的

dp[0][0] = true;

  

// 2. 初始化第 0 行: s 为空，p 不为空的情况

// p 只有形如 "a*", "a*b*", "a*b*c*" 这种模式才能匹配空串

// 遇到 '*' 时，看跳过 '*' 和它前一个字符后的状态 (即 j-2)

for (int j = 1; j <= n; j++) {

if (p[j - 1] == '*') {

dp[0][j] = dp[0][j - 2];

}

}

  

// 3. 填表

// 习惯上我们先遍历 i (s)，再遍历 j (p)，但在本题中顺序不影响结果

for (int i = 1; i <= m; i++) {

for (int j = 1; j <= n; j++) {

// 技巧：先取出当前要比较的字符，避免在逻辑里反复写下标

// dp 里的 i 对应 s 里的 i-1

// dp 里的 j 对应 p 里的 j-1

char sChar = s[i - 1];

char pChar = p[j - 1];

  

if (pChar != '*') {

// 情况 A: p 当前字符不是 *

// 必须字符匹配 或者 p 是 '.'

if (sChar == pChar || pChar == '.') {

dp[i][j] = dp[i - 1][j - 1];

}

} else {

// 情况 B: p 当前字符是 *

// pChar 是 '*'，那么它控制的是 p 中的前一个字符，我们叫它 prevChar

char prevChar = p[j - 2]; // 因为 j 是长度，j-1 是 *，j-2 是 * 前面的字符

  

// 子情况 1: * 代表匹配 0 次 (直接扔掉 "x*")

// 我们直接看去掉这两个字符后的状态 (j-2)

bool matchZero = dp[i][j - 2];

  

// 子情况 2: * 代表匹配 1 次或多次

// 前提是：s 的当前字符 sChar 必须和 p 的 prevChar 匹配

bool matchMany = false;

if (sChar == prevChar || prevChar == '.') {

// 如果匹配，s 向前缩减一位 (i-1)，p 保持不动 (继续用 * 匹配更多)

matchMany = dp[i - 1][j];

}

  

dp[i][j] = matchZero || matchMany;

}

}

}

  

return dp[m][n];

}

};
```
## Thoughts