## Definition

分治：把序列对半分，两侧各自排好，再 [[Merge Sorted Lists|归并]] 成一条。

## 骨架

```
mergeSort(l, r):
    if (l >= r) return
    m = (l + r) / 2
    mergeSort(l, m); mergeSort(m+1, r)
    merge(l, m, r)            // 两边取小，需要一个 O(n) 辅助数组
```

## 性质

- **稳定**：合并时 `<=` 取左边。
- **比较次数的下界**：$n$ 个元素排好序至少要 $\lceil \log_2 n! \rceil$ 次比较，归并在最坏情况下达到同阶——这是 2012·41 考「归并比较次数」的落点。
- 空间 $O(n)$：唯一需要额外阵列的比较排序。

## 复杂度

时间 $O(n\log n)$（最好、最坏、平均同阶）；空间 $O(n)$。

## 真题

2012·41（归并的比较次数）、2021·42（读计数排序式算法: 比较次数、稳定性）。

## 相关

[[Merge Sorted Lists]] · [[Sorting and Priority Queue]] · [[408 数据结构-算法设计题考点地图]]
