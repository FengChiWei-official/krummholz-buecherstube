---
tags:
  - type/permanent
  - attr/concept
  - status/in-progress
---

## Definition

I would like to name it as **Merge DP**. [[Interval]]

## States
DP [[State Space]] in shape $\text{Begin} \times \text{End}$. The basis of the Space is formed by trivial cases of intervals $[i, i]$. 

|     | end j=0 | 1    | 2          | 3          |            |
| --- | ------- | ---- | ---------- | ---------- | ---------- |
| i=0 | 1       | 1+2  | 1+5 \| 3+3 | 3 cases    | 4cases     |
| 1   | Null    | 2    | 2+3        | 2+4 \| 5+1 | 3cases     |
| 2   | Null    | Null | 3          | 3+1        | 3+3 \| 4+2 |
| 3   | Null    | Null | Null       | 1          | 1+2        |
| 4   | Null    | Null | Null       | Null       | 2          |

### Transition Logic

1. How do you [[Diagonal Traversal]] the Table? 


---
## **Related**
[[Floyd Warshall Algorithm]]
