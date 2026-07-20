---
tags:
  - type/permanent
  - status/in-progress
  - topic/learning
  - attr/concept
---

## Definition
Pre-condition check
Pattern: before entering any local, high-risk pattern decomposition/matching, perform a coarse boundary check first.
Code example (C++):
code
```C++
// Bad practice: checking bounds while matching
for (int i = 0; i < text.size(); ++i) {
  if (text[i] == 'A' && text[i+1] == 'B' && text[i+2] == 'C') { ... } // prone to out-of-bounds at the end
}

// Good practice: prune first, then match safely
int limit = (int)text.size() - 3;
for (int i = 0; i <= limit; ++i) {
  if (text[i] == 'A' && text[i+1] == 'B' && text[i+2] == 'C') { ... } // guaranteed safe
}
```

---
## **Related**
