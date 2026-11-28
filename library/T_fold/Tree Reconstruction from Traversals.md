## Definition

由两种遍历序列还原唯一的二叉树。可用的组合只有两种：**前序 + 中序**、**后序 + 中序**；前序 + 后序还原不出唯一树。

## 递归骨架（前序 + 中序）

```
build(preL, preR, inL, inR):
    root = pre[preL]                       // 前序首元素是根
    k = pos[root]                          // 根在中序里的位置
    leftSize = k - inL
    root->lchild = build(preL+1, preL+leftSize, inL, k-1)
    root->rchild = build(preL+leftSize+1, preR, k+1, inR)
```

后序版把「取根」换成 `post[postR]`，左子树大小同样从中序算。

## 两条判据

- **中序必须在场**：只有中序能把「左子树有哪些」和「右子树有哪些」切开。
- **前序 + 后序不够**：单子树时无法判断是左还是右，还原出多棵树。

## 复杂度

朴素按位置线性查找根是 $O(n^2)$；用哈希表存中序下标降到 $O(n)$。

## 相关

[[Preorder Traversal]] · [[Inorder Traversal]] · [[Postorder Traversal]] · [[Binary Tree]]
