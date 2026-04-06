---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
---

## Definition
- **Pass by Reference (`&`) is Mandatory:**
- **The "Mark Before Entering/Pushing" Rule:**
    - Always set `vis[nxt] = 1` **immediately before** executing the `dfs(nxt...)` call (or `q.push(nxt)` in BFS).
- **Reuse Input Data Directly:**
- **Implicit Termination Condition:**
    - In graph-based DFS, the `if (!vis[nxt])` check acts as the natural termination condition. It guarantees that each node is processed exactly once, preventing infinite loops and redundant computations.

---
## Template

[[DFS Template]]


---
## **Related**