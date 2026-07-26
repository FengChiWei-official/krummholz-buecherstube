---
tags:
  - type/permanent
  - topic/learning
  - attr/views
  - status/in-progress
---
## Tree Mental Models

1. **The Lollipop Model (Incoming-Edge Bijection)**
   - *Perspective:* Global topology & invariants.
   - *Takeaway:* Every non-root node has 1 parent edge ($E = V - 1$). Useful for parent-pointer structures.

2. **The Octopus Model (Outgoing-Branching)**
   - *Perspective:* Structural recursive definition ($Tree = Node + List<Tree>$).
   - *Takeaway:* A node manages its children through outgoing branches. Useful for top-down traversal (DFS/BFS).

3. **The Local Unrolling Model (FP Pattern Matching)**
   - *Perspective:* Dynamic execution & recursive thinking.
   - *Takeaway:* Expand only 1–2 levels locally to reason about recursion without cognitive overload.

---
## **Related**

[[View of Haskell's Properties]]