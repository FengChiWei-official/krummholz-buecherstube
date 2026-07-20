---
tags:
  - type/permanent
  - topic/learning
  - attr/concept
  - status/evergreen
---

## Definition

idn

## Methods

>[!note]
>You might learn how do [[Interval]] operate as a [[Layered Directed Acyclic Graph]] first.  

### Method 1: Length-First
> It can be considered as [[Breadth-First Search|BFS]] of [[Interval|Intervals]] or [[Layered Directed Acyclic Graph]].

That is pretty trivial. You're supposed to traversal all intervals, layer by layer.
>[!note]
>
```
           ->(1,4)
        ->(1,3)->(2,4)
    ->(1,2)->(2,3)->(3,4)
```


### Methods 2: Index-First
> It can be considered as [[Depth First Search|DFS]]

Here is a table showing how do we traversal in a matrix.

|           | end j=0 | 1   | 2   | 3   | 4 //(m) |
| --------- | ------- | --- | --- | --- | ------- |
| begin i=0 | 0       | 7   | 8   | 9   | 10      |
| 1         |         | 0   | 4   | 5   | 6       |
| 2         |         |     | 0   | 2   | 3       |
| 3         |         |     |     | 0   | 1       |
| 4 //(n)   |         |     |     |     | 0       |
And it template.
``` cpp
for (i in [n-1, 0]) {
	for (j in [i+1, m]) {
		// pass
	}
}

```
>[!note]
> Raw Indexs:
>1. 3 -> [4]
>2. 2 -> [3, 4]
>3. 1 -> [2, 3, 4]
>4. 0 -> [1, 2, 3, 4]

---
## **Related**
