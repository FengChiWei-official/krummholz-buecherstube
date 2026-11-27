## Definition

A [[Linear List]] whose order lives in pointers instead of contiguous memory: each node carries the address of its successor.

## 基本规范

1. **改结构先取前序。** 工作区域：任何改变结构的操作，先拿到被操作节点的**直接前序**（`prev`），入口都落在 `prev` 上——插入见 [[Inserting Nodes into a Linked List]]，删除见 [[Deleting Nodes from a Linked List]]。
2. **改指针先存旧目标。** 所有节点的指针被修改前，都要先把旧目标缓存或转移：先 `next = prev->next`，再 `prev->next = new_node`。否则改一次就把后半条链丢在身后。

## 空判定

- 只有两条路：**首元为空**（有头结点：`dummy->next == NULL`）或**头指针为空**（无头结点）。没有第三种。

## 可选部分

[[Dummy Head Node]] · [[Rear Pointer for a Linked List]] · [[Circular Linked List]]

---
## **Related**

[[Linear List]] · [[Sequential List vs. Linked List]]