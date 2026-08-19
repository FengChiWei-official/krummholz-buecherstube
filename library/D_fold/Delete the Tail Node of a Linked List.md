---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/technique
---
## Time Optimization

### [[Doubly Linked List]]

Allows finding the previous node (`prev`) in $O(1)$ time using backward pointers (`node->prev`).

`head <-> ... <-> prev <-> tail <-> head`

> [!note] 
> - **Singly Linked List + Rear Pointer:** A rear pointer alone **does not** allow $O(1)$ tail deletion, because finding `prev` still requires $O(N)$ traversal from `head`.
> - **Doubly Linked List + Rear Pointer:** Enables true $O(1)$ tail deletion, since `tail->prev` provides immediate access to the second-to-last node.

---
## **Related**