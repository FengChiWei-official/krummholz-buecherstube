## Definition

三个升序数组各持一个指针，每步算当前三元组的距离，然后**只移动当前值最小的那一路**——因为距离由 $\max-\min$ 决定，最小值不前进，距离不可能变小。

## 骨架

```c
int i = j = k = 0, best = INF;
while (i < na && j < nb && k < nc) {
    int mn = min3(a[i], b[j], c[k]);
    int mx = max3(a[i], b[j], c[k]);
    if (mx - mn < best) best = mx - mn;
    if      (mn == a[i]) i++;      // 只推进最小的一路
    else if (mn == b[j]) j++;
    else                 k++;
}
```

## 为什么不会漏解

设当前最小的是 $a[i]$：任何含 $a[i]$ 的三元组，距离都不小于当前这个（其余两路都已取到各自「最靠左」的位置），所以含 $a[i]$ 的其余组合可以整批剪掉，直接推进 $i$。这是「多路取小 + 剪一侧」的贪心，不是暴力三循环。

## 复杂度

$O(n_a+n_b+n_c)$ 时间 / $O(1)$ 空间。

## 真题

2020·41：三个升序数组的三元组最小距离。

## 相关

[[Read-Write Two Pointers]] · [[Merge Sorted Lists]] · [[408 数据结构-算法设计题考点地图]]
