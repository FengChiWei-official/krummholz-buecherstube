---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/technique
---
## Definition

Deletion in a singly linked list generally involves 3 steps:
1. Find the previous node (`prev`).
2. Update the pointer (e.g., `prev->next = target->next`).
3. Free/deallocate the target node's memory.

> [!note]
> **Boundary Checks:**
> - Check if the list is **already empty** before attempting to delete.
> - Check if the list will become empty after deletion (to correctly update `head` and `rear` pointers).

`prev -> (target node) -> next`

## Related Features

- **[[Dummy Head Node]]**: Avoids special-case logic for deleting the first node, because `prev` will always exist. *(Note: You must still check if the list is empty via `dummy->next == NULL`).*
- **[[Delete the Tail Node of a Linked List]]**
- **[[Rear Pointer for a Linked List]]**: Requires extra handling.
  > *Example:* When deleting the first node, check if it is also the last node (`head == rear`). If so, set `rear = NULL`.
---
## **Related**