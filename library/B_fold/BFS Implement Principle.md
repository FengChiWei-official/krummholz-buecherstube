---
tags:
  - type/permanent
  - attr/principle
  - topic/learning
  - status/evergreen
---

## Definition
Breadth-First Search (BFS)

Purpose: find shortest paths in unweighted graphs, level-order traversal, and reachability. BFS is the standard choice when you need the minimum number of edges from a start to targets.

Key points

1. Define your graph properly (directed? undirected?).
2. Mark/visit when you enqueue ("mark-on-push") to avoid multiple enqueues.
3. Enqueue the start node(s) explicitly and initialize their distance/state.

When to prefer BFS vs Connectivity-DFS

- Use BFS when you need shortest-path (unweighted) or level-order processing.
- Use Connectivity DFS when you only need to know reachability or count components (no shortest path requirement).

## Template
[[BFS Templates]]

## Example
- [[archives/algorithms/841. Keys and Rooms]]
- [[牛客_小红走迷宫]]

---
## **Related**
See [[Connectivity DFS]] for connectivity-oriented traversals and the differences in visited semantics.
