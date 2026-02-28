---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
---

## State shifting
if you have a state i, and you want to traversal all available state, use this pattern.
```
const int initial_state = 233;
const int final_state = 466;

for (int state = initial_state; state < final_state; f(state))
```
And **ENSURE** end_point be **static**, to satisfy [[Loop Invariant Principle]].

**Common Pitfall**: As you noted, confusing `initial_state`with the current `state`can break the invariant. For example:

- If `f(state)`accidentally modifies `initial_state`, the loop bounds become dynamic, violating the invariant.
    
- Solution: Use `const`declarations (as in your code) and ensure `f`only alters the current `state`, not the initial or final values. This is analogous to state transitions in systems like Prefect, where states (e.g., `Pending`→ `Running`→ `Success`) are managed with explicit boundaries to avoid unintended side effects .

## dummy node (`哨兵` or `虚拟头节点`)

---
## **Related**：