---
aliases:
---

## Definition

### Index

When we talk about an element$a_{i,j}$ of Matrix, it follows the math rule  - the index starts at 1.
When we talk about its storage, it usually starts at 0, unless, it was written like `B[1...n][1...m]`.

### Compress of Special Matrices

Always compress into a `1D` Linear List. Follow the `line-first` rule.

**The Storage of Triangle Matrices** store the constant value at the end .

#### ie.

--对称矩阵的例子--
--三角矩阵的例子--
--三对角矩阵的例子--

### Index converter function design

[[]]



---
## **Related**

[[Linear List]] — 稀疏/特殊矩阵的存储（三元组表、十字链表）挂在线性表的存储结构下
[[Sequential List]] — 顺序压缩：特殊矩阵的一维数组、稀疏矩阵的三元组表
[[Linked List]] — 链式压缩：稀疏矩阵的十字链表

[[ADT Graph]] 内容类似Graph的存储