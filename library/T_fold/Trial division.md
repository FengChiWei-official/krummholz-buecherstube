---
tags:
  - type/permanent
  - attr/principle
  - topic/learning
  - status/evergreen
---

## define
``` cpp
//for (int i = 2; i<sqrt(n); i++){}
// change your min[[Trie Tree]]d and something will be simpler
// let result a map {base: exponent}
using pw = std::pair<int, int>;
using vec = std::vector<pw>;
vec result = vec();
for (int base = 2; base*base<(n); base++){
	if (n % base == 0){
		// exponent
		int exponent = 0;
		while(True){
			n = n / base;
			exponent++;
			if (n % base != 0) break;
		}
		result.
	}
		
}

```

---
## **related**：
