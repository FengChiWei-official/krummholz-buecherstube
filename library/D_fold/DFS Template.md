---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---
## DFS 模板（整理）

简要说明：DFS 常见有两类用法 —— 1) 对图/网格的连通性搜索（使用全局 visited），2) 回溯/枚举全部解（使用路径局部状态并回滚）。下面给出统一、清晰的模板与要点。

### 1) 递归 - 连通性 DFS（global visited）
```cpp
void dfs_connectivity(int u) {
    vis[u] = 1; // 在进入时标记，避免重复遍历
    for (int v : adj[u]) {
        if (!vis[v]) dfs_connectivity(v);
    }
}
```

要点：
- 标记时机：递归时通常在进入节点（entry）标记 `vis[u]=1`。
- 如果需要遍历多个连通分量，主循环：for (all nodes) if (!vis[i]) dfs_connectivity(i);

### 2) 迭代 - 使用栈的 DFS（connectivity）
```cpp
void dfs_iterative_pair(pair<int,int> start, vector<vector<int>>& vis, vector<vector<char>>& g) {
    int rs = g.size(), cs = g[0].size();
    vector<pair<int,int>> dirs = {{0,1},{1,0},{0,-1},{-1,0}};
    stack<pair<int,int>> st;
    st.push(start);
    vis[start.first][start.second] = 1; // 在 push 时标记，防止入栈重复
    while (!st.empty()) {
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
```

注意：迭代版要在“入栈时”标记 `vis`，否则同一节点可能被多次入栈。

### 3) 回溯 / 枚举（path-local state, undo）
```cpp
void backtrack(vector<int>& path) {
    if (terminal_condition) {
        answers.push_back(path);
        return;
    }
    for (auto choice : choices) {
        if (!valid(choice)) continue;
        // 选择
        path.push_back(choice);
        apply_state(choice);
        backtrack(path);
        // 撤销
        undo_state(choice);
        path.pop_back();
    }
}
```

要点：
- 回溯使用显式的 `path` / 状态栈，并在递归返回前撤销修改。
- 若有禁止重复元素的约束，可以使用局部 `used` 数组，并在选择前后切换状态。

### 常见示例
- numIslands（网格连通块，递归版）
```cpp
void dfs_island(int x, int y, vector<vector<char>>& grid, vector<vector<int>>& vis) {
    int rs = grid.size(), cs = grid[0].size();
    if (x<0 || x>=rs || y<0 || y>=cs) return;
    if (grid[x][y] != '1' || vis[x][y]) return;
    vis[x][y] = 1;
    dfs_island(x+1,y,grid,vis);
    dfs_island(x-1,y,grid,vis);
    dfs_island(x,y+1,grid,vis);
    dfs_island(x,y-1,grid,vis);
}
```

- permutations（回溯列举）
```cpp
void permute(vector<int>& a, vector<int>& cur, vector<vector<int>>& ans, vector<int>& used) {
    if (cur.size() == a.size()) { ans.push_back(cur); return; }
    for (int i = 0; i < (int)a.size(); ++i) {
        if (used[i]) continue;
        used[i] = 1;
        cur.push_back(a[i]);
        permute(a, cur, ans, used);
        cur.pop_back();
        used[i] = 0;
    }
}
```

### 常见坑与建议
- 递归深度：注意递归深度可能导致栈溢出，必要时使用迭代或增加递归深度限制（竞赛环境谨慎）。
- visited 的粒度：连通性问题用全局 `vis`，枚举路径用局部 `used`/`path`。
- 标记时机：递归在进入时标记；迭代在入栈时标记。
- 性能：尽早剪枝、避免不必要的状态复制。

---

（已整理：统一模板、补充递归/迭代/回溯示例与要点）
