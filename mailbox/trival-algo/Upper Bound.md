## Templates

```cpp

// given
vector<int> nums;
int target;

//
int l = 0; r = nums.size();
while(l<r) {
	int m = l + (r-l)/2; // Attention! Out of Limit
	// int vm = nums[m]; no need, just one time.
	
	// get rid of this switch
	// nums[m], not m.
	// `<=` means if target is `5` and nums is 1 3 5 5 5 7, got 1 2 5 5 5 (7)
	if (nums[m] <= target) l = m+1; 
	// r is not include in this situation.
	// however, the end case is left meeting right, breaking the rule.
	// this situasion makes r become a possible solution.
	else r = m; 
}

return l;
```