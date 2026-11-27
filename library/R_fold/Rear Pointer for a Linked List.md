## Definition

pros: 
1. helps when inserting.
cons:
2. needs extra handling. [[Deleting Nodes from a Linked List]]

## 删除的波及

尾指针多存了一份「最后一个元素」的地址，删除就可能让它悬空。删除前先判断会不会波及 `rear`：删的是不是最后一个、删完表会不会变空（`head == rear`）。见 [[Deleting Nodes from a Linked List]] 的 Boundary Checks。

---
## **Related**