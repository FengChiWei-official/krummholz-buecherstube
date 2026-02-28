---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
aliases:
  - Four Boundaries Traversal Matrix
---

## qwq
``` cpp
//given
int cols; int rows;

// set up
int left = 0;
int right = cols-1;
int top = 0;
int bottom = rows -1;

while (left<=right&&top<=bottom) {
	// if (top <= bottom) {}
	// you can skip that
	for (int i = left; i <= right; i++) {
		// do sth
	}
	top++;
	
	for (int i = top; i<=bottom; i++) {
		// do sth
	}
	right--;
	
	if (top <= bottom) {
		for (int i = right; i>=left; i--) {
			// do sth
		}
		bottom--;
	}
	
	if (left <= right) {
		for (int i = bottom; i >= top; i--) {
			// do sth
		}
		left++;
	}
}
```


---
## **Related**：