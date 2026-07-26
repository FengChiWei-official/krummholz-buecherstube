---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/technique
---

## Definition

Insertion is one of the most important operations in a [[Linked List]].

## Understanding

In general, insertion consists of:
1. Creating/allocating the new node.
2. Finding the previous node (`prev`).
3. Updating the relevant pointers (linking `new_node` to `prev->next`, then `prev` to `new_node`).

> [!tip]
> Almost all linked list optimizations (e.g., [[Rear Pointer for a Linked List]], [[Dummy Head Node]]) focus on making **Step 2** faster or easier to handle.

[[Inserting at the Tail of a Linked List]]

---
## **Related**