---
tags:
  - type/permanent
  - topic/learning
  - attr/concept
  - status/evergreen
aliases:
  - Connectivity DFS
---

## Connectivity DFS (reachability / connected components)

Purpose: explore which nodes are reachable from a start and/or count connected components. Typical problems: "Number of Islands", reachability, connected components, simple graph traversals.

Visited semantics:
- Mark a node as visited when you first encounter it (before recursing or pushing). This prevents duplicate work and infinite loops for undirected graphs.

Canonical templates

Graph (recursive)

```
void dfs(int u) {
    vis[u] = 1; // mark on entry
    for (int v : g[u]) if (!vis[v]) dfs(v);
}

// usage: for every node i, if (!vis[i]) { dfs(i); component_count++; }
```

Grid (4-directional)

```
void dfs_grid(int r, int c) {
    vis[r][c] = 1; // mark on entry
    for (dir : 4 directions) {
        nr = r + dr; nc = c + dc;
        if (in_bounds && !vis[nr][nc] && is_land) dfs_grid(nr, nc);
    }
}
```

Common pitfalls
- Forgetting to mark before recursion causes exponential revisits.
- Using the wrong visited scope (global vs path-local) — connectivity uses global visited.

Examples
- [[200. Number of Islands]] — grid connected components using connectivity DFS.
- [[archives/algorithms/841. Keys and Rooms]] — reachability in a graph (also solved with BFS).

Related
- See [[Backtracking DFS]] for problems that require enumerating full paths or using temporary (path-local) visited semantics.
