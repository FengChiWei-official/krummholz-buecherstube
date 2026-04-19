---
tags:
  - type/permanent
  - attr/principle
  - topic/learning
  - status/evergreen
---

## Definition
This note gives implementation principles for DFS. There are two common DFS modes: connectivity-style (global visited) and backtracking/full-path (path-local visited). See [[Connectivity DFS]] and [[Backtracking DFS]] for the recommended templates and examples.

- **Pass by Reference (`&`) is recommended** for large structures to avoid copies.
- **The "mark before entering/pushing" rule (connectivity mode):** set `vis[nxt] = 1` immediately before calling `dfs(nxt)` (or `q.push(nxt)` in BFS) to prevent duplicate processing.
- **Implicit termination:** the `if (!vis[nxt])` check prevents revisiting nodes and provides a natural termination.

---
## Template

[[DFS Template]]


---
## **Related**
