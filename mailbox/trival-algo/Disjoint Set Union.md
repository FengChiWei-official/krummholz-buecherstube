---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
aliases:
  - 并查集
  - DSU
  - Union Find
---
> disjoint means `不相交`
## define
> A `set` is a set of elements that represent as a `parent` node.
> ![[DSU_example.png]]
1. union: combine 2 sets
2. find: given a element, tell in which set it is(*return parent*).
3. (make_set): set up a set with new element `e`.


## Why I need DSU
It describes `having relationship`, if each elements have then same root, then they have relationship, else they dont.


---
## **related**：
[[Code Implement of Disjint Set Union]]