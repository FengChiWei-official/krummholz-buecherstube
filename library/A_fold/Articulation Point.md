## Definition

割点：删掉它之后，连通分量个数增加的顶点。判据在 DFS 树上，与「有没有环」无关——树的所有非叶结点都是割点。

## 判据（Tarjan）

- 记 `dfn[u]` 为进入时间，`low[u]` 为「u 及其子树能回到的最小 dfn」。
- 非根结点 $u$：若存在孩子 $v$ 使 `low[v] >= dfn[u]`，则 $u$ 是割点——$v$ 这一支回不到 $u$ 的祖先。
- 根结点：它有 **两个以上** DFS 孩子才是割点（一个孩子时删掉它只少一个点，不增连通分量）。

## 骨架

```
dfs(u, parent):
    dfn[u] = low[u] = ++timer
    child = 0
    for v in adj[u]:
        if (!dfn[v]):
            dfs(v, u); child++
            low[u] = min(low[u], low[v])
            if (u != root && low[v] >= dfn[u]) isCut[u] = 1
        else if (v != parent):
            low[u] = min(low[u], dfn[v])      // 回边
    if (u == root && child > 1) isCut[u] = 1
```

## 复杂度

$O(n+e)$ 时间，一次 DFS。

## 真题

考纲第六章拓展题（割点），大题未出现。

## 相关

[[Depth First Search]] · [[Connectivity DFS]] · [[Bipartite Graph]]
