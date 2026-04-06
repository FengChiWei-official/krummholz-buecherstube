---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text
```
#include <iostream>
#include <vector>
#include <queue>

using namespace std;

/**
 * 模板说明：
 * 1. 使用 vector<vector<int>> 建立邻接表 (Adj List)
 * 2. 状态更新遵循“入队即标记”，防止重复入队
 * 3. 适用于无向图 (Undirected Graph, UDG)
 */

void solve() {
    int n, m;
    if (!(cin >> n >> m)) return;

    // 1. 建图：n个点，m条边
    vector<vector<int>> g(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u); // 无向图的关键：双向加边
    }

    // 2. BFS 初始化
    queue<int> q;
    vector<int> vis(n + 1, 0); // 访问标记数组

    // 起点处理（以1号房为例）
    int start_node = 1;
    vis[start_node] = 1;
    q.push(start_node);

    // 3. 核心循环
    while (!q.empty()) {
        int curr = q.front();
        q.pop();

        // 遍历当前节点的所有邻居
        for (int next_node : g[curr]) {
            // 条件判断：未访问过 && (可选：符合业务逻辑，如非陷阱)
            if (!vis[next_node]) { 
                vis[next_node] = 1; // 入队即标记！
                q.push(next_node);
            }
        }
    }

    // 4. 输出结果 (根据题目要求排序输出)
    for (int i = 1; i <= n; i++) {
        if (vis[i]) cout << i << (i == n ? "" : " ");
    }
    cout << '\n';
}

int main() {
    // 职业选手的快速 IO
    ios::sync_with_stdio(0);
    cin.tie(0);

    solve();

    return 0;
}


```

---

## Thoughts