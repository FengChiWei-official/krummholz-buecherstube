## Definition

先访问根，再左子树，再右子树：`visit(u); dfs(u->lchild); dfs(u->rchild);`。

## 用途

- 复制/序列化一棵树（先序能唯一确定结构，配合中序可还原）。
- 带深度往下发的量：层数当递归参数传（WPL 的深度就是这样下来的，2014·41）。

## 复杂度

$O(n)$ 时间；递归栈 $O(h)$，退化树 $h=n$。

## 与其他遍历

[[Inorder Traversal]]（BST 出有序序列）· [[Postorder Traversal]]（自底向上聚合）· [[Level Order Traversal]]（队列驱动）

## 相关

[[Binary Tree]] · [[408 数据结构-算法设计题考点地图]]
