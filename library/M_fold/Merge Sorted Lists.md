## Definition

两条有序链合并成一条有序链：每次取较小的头结点接到结果尾部。

## 骨架

```c
struct Node dummy, *t = &dummy;      // 哑结点省掉「结果还空着」的分支
while (a && b) {
    if (a->data <= b->data) { t->next = a; a = a->next; }
    else                    { t->next = b; b = b->next; }
    t = t->next;
}
t->next = a ? a : b;                 // 剩下的一整段直接接上
```

## 要点

- **哑结点**把「空结果」这一个分支消掉，与 [[Dummy Head Node]] 是同一条统一逻辑。
- 剩余段一条 `next` 接上即可，不要逐个结点搬。
- 取等号的方向决定稳定性：`<=` 取前者，原序保持。

## 复杂度

$O(n+m)$ 时间 / $O(1)$ 空间（结点复用，不新建）。

## 相关

[[Linked List]] · [[Dummy Head Node]] · [[Merge Sort]]
