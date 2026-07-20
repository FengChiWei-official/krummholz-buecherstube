---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## BFS Templates

Notes: Use "mark on enqueue" (visited when pushing to queue) to avoid duplicate enqueues. BFS is typically used for unweighted shortest paths and level-order traversal.

Minimal BFS (graph adjacency list)

```
void bfs(int start) {
    queue<int> q;
    vector<int> vis(n+1, 0);
    vis[start] = 1; // mark on enqueue
    q.push(start);

    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : g[u]) if (!vis[v]) {
            vis[v] = 1; // mark when enqueue
            q.push(v);
        }
    }
}
```

Grid BFS: replace `g[u]` iteration with 4-direction neighbor checks and `vis[r][c]` grid.

Examples
- [[archives/algorithms/841. Keys and Rooms]]

---

## Thoughts
