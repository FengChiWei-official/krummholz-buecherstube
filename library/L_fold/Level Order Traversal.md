## Definition

按层从左到右访问：队列驱动，出队一个就把它的孩子入队。

## 骨架（层边界）

```c
queue q; push(q, root);
while (!empty(q)) {
    int sz = size(q);              // 本层结点数，卡住层的边界
    while (sz--) {
        u = pop(q);
        visit(u);
        if (u->lchild) push(q, u->lchild);
        if (u->rchild) push(q, u->rchild);
    }
    // 这一层处理完：层数 +1 / 本层和结算
}
```

`sz` 是层序题的全部技巧：不记它，层与层就粘在一起。

## 用途

树的宽、高、按层输出、右视图、判断完全二叉树（遇到空结点后不该再有结点）。

## 复杂度

$O(n)$ 时间 / $O(w)$ 队列空间（$w$ = 最大宽度）。

## 相关

[[Breadth-First Search]] · [[Binary Tree]] · [[408 数据结构-算法设计题考点地图]]
