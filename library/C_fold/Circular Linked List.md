## Definition

尾节点的后继指回链表头部，遍历不会撞到空指针，收口靠回到起点或计数。

## 规范

- **循环只改「哪里算结尾」**：空判定仍按 [[Linked List]] §空判定 的两条路走。
- **默认有无头结点是未定项**：原文带问号，取默认值时再裁决；环上插入删除同样先取前序，见 [[Linked List]] §基本规范。

## 用例

[[Chain Queue]] 默认循环链表，队尾落在链表头部。

---
## **Related**

[[Linked List]] · [[Features of Linked List]]