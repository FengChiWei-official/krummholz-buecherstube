## Definition

两个栈拼一个队列：`in` 只负责入队，`out` 只负责出队。

## 骨架

```
push(x):  in.push(x)
pop():    if (out.empty()) while (!in.empty()) out.push(in.pop());
          return out.pop()
empty():  in.empty() && out.empty()
```

**关键**：只有 `out` 空的时候才整批倒一次。每次元素最多被搬两次，所以摊还 $O(1)$；单次最坏 $O(n)$。

## 对称命题：两队列实现栈

```
push(x):  q2.push(x); while (!q1.empty()) q2.push(q1.pop()); swap(q1, q2)
pop():    q1.pop()
```
每次入栈要把整队搬一遍，$O(n)$ 单次；这是两栈实现队列**不**对称的地方——所以别顺手写成「摊还 $O(1)$」。

## 判据

题面给定了「只能用某种结构」的约束（如只能用栈实现队列）时，答案就是这种互转，不要另找算法。

## 真题

考纲第三章拓展题（未在大题出现）。

## 相关

[[Stack]] · [[Queue]] · [[Circular Queue]]
