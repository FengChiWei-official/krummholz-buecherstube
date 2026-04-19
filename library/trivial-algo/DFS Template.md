---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text
```


void dfs(状态参数, vector<int>& path) {
    // 1. 【终点】：完成任务了吗？
    if (满足终止条件) {
        记录/输出答案;
```
// DFS Templates (two modes)

// 1) Connectivity DFS (global visited)
void dfs_connectivity(int u) {
    vis[u] = 1; // mark on entry
    for (int v : adj[u]) if (!vis[v]) dfs_connectivity(v);
}

// 2) Backtracking / Full-path DFS (path-local visited / undo state)
void backtrack(vector<int>& path) {
    if (terminal_condition) { answers.push_back(path); return; }
    for (choice : choices) {
        if (!valid(choice)) continue;
        // choose
        apply(choice);
        backtrack(path);
        // undo
        undo(choice);
    }
}

```

The examples below show practical uses: connectivity for `numIslands`, and backtracking for permutations/subset generation.

```
// Example: iterative DFS (grid) used in numIslands
class Solution {
public:
    vector<pair<int,int>> dirs = {{0,1},{1,0},{0,-1},{-1,0}};
    void dfs_iterative(vector<vector<char>>& g, vector<vector<int>>& vis, pair<int,int> start) {
        int rs = g.size(), cs = g[0].size();
        stack<pair<int,int>> st;
        st.push(start);
        vis[start.first][start.second] = 1; // mark on push
        while(!st.empty()) {
            auto [x,y] = st.top(); st.pop();
            for (auto [dx,dy] : dirs) {
                int nx = x + dx, ny = y + dy;
                if (nx>=0 && nx<rs && ny>=0 && ny<cs && g[nx][ny]=='1' && !vis[nx][ny]) {
                    vis[nx][ny] = 1;
                    st.push({nx,ny});
                }
            }
        }
    }
};
```

---

## Thoughts
// 调用方式：
// vis[start] = 1; count = 1;
// dfs(start, adj, vis, count);


```

---

## Thoughts
