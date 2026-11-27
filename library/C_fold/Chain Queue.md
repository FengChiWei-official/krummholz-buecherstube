## Definition

队列用链表实现。

## 规范

- **默认没有头结点**。
- **默认循环链表**：尾节点的后继指回头部，见 [[Circular Linked List]]。
- **队尾一般在链表头部**（`head`，不是 `front`）。

尾指针在删除时的波及判断见 [[Rear Pointer for a Linked List]]。

## 相关

[[Queue]]
