---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/concept
---

## Definition
**Scan and Filter**.

## Concept

- **Fast pointer**: The **"Explorer"** that **traverses** all elements to find those that meet the criteria.
- **Slow pointer**: The **"Marker"** that tracks the next available position to **place** the valid elements.

## Template

```cpp
class Solution {
public:
	void moveZeroes(vector<int>& nums) {
		int slow = 0;
		for (int fast = 0; fast < nums.size(); fast++) {		
			if (nums[fast] != 0) {
			swap(nums[fast], nums[slow]);		
			slow++;	
			}
		}
	}
};
```
---
## **Related**