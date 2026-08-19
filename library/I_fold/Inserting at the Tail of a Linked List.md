---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/technique
---
## Variations & Features

### 1. [[Rear Pointer for a Linked List]] (Tail Pointer)

Allows inserting elements at the tail in $O(1)$ time by eliminating the need to traverse from the head.

* **Trade-off:** Requires careful maintenance (must be updated during tail insertions, tail deletions, or when the list becomes empty).

`[old_tail] -> [new_node] <- rear`

---

### 2. [[Doubly Linked List]] + [[Circular Linked List]]

Uses **more memory** (due to storing two pointers per node: `prev` and `next`), but makes node deletion and bidirectional traversal much easier.

* **Linear Tail Insertion:**
  `... <-> [old_tail] <-> [new_node]`

* **Circular Tail Insertion** *(if circular)*:
  `[tail] <-> [new_node] <-> [head]`

---
## **Related**