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

**与存储面的对应**：棒棒糖 = 双亲表示法（往上问），八爪鱼 = 孩子 / 孩子兄弟表示法（往下走），见 [[Storage of Tree]]。

---
## **Related**

[[Links of Haskell's Properties]]