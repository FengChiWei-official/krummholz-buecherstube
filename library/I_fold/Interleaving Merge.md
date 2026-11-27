## Definition

两条链交替取结点、重新接成一条：`a1 → b1 → a2 → b2 → …`，只改 `next`，不申请新结点。

## 骨架

```c
while (a && b) {
    ListNode *an = a->next, *bn = b->next;
    a->next = b;  b->next = an;      // 先存后继，再改指针
    a = an;       b = bn;
}
```

「先存后继再改指针」是 [[Linked List]] §基本规范 第 2 条的直接应用；漏掉保存就把后半条链丢了。

## 前提

两条链长度相等，或前半段不比后半段短；不满足时先 [[Length Alignment]] 或 [[Reverse]] 补形。

## 复杂度

$O(n)$ 时间 / $O(1)$ 空间。

## 真题

2019·41：重排 $a_1,a_n,a_2,a_{n-1},\dots$ 的第三步（前两步是 [[Fast and Slow Pointers]] 找中点、[[Reverse]] 逆置后半段）。

## 相关

[[Linked List]] · [[408 数据结构-算法设计题考点地图]]
