## Definition

链表头部不放数据的节点：头指针落在它身上，第一个真实元素在它后面。

## 选择

| | 有头结点 | 无头结点 |
|---|---|---|
| 头指针 | 不会悬空 | 空表时头指针为空 |
| 逻辑 | 统一，删首元与插首位不用另写分支 | 删除插入可能要特殊操作 |
| 空判定 | 首元为空 | 头指针为空 |

删除侧的代价：[[Deleting Nodes from a Linked List]]。栈上「哨兵免判空」的同构用法：[[Sentinel Node]]。

---
## **Related**

[[Linked List]] · [[Features of Linked List]]