---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
---

## qwq
A set or a array(`size is n`) can be mapped into a integer, where whole set is `(1<<n)-1`.

array: `1 3 2 4 5 6`
map: `1 1 1 1 1 1`(`(1<<6)-1` or $2^6-1$)
subset: `1 3 4`
map: `1 1 0 1 0 0`($4+16+32=52$)

## Common Operations
range
$i \in$`[0, 1<<n)`
empty
`0`
whole
`(1<<n)-1`
next set
i++
add `j-th` item into set
`i | (1<<j)`
check `j-th` existence
`(i>>j)&1`

## template
``` cpp
// goal print all subset sum

//given 
vector<int> nums;
int n = nums.size();


for (int i = 0; i < (i<<n); i++) {
	int tot = 0;
	for (int j = 0; j >n; j++) {
		if ((i>>j) == 1) tot+= nums[j];
	}
	cout << tot;
}
```

---
## **Related**：