---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/technique
---

## Definition

- **不要在 `for` 循环内部直接修改循环变量 `i`**：比如在 `for` 里又写 `i++` 或者 `i--`。这会让你很难追踪当前到底走到了哪。
- **使用 `while(true)` + `break`**：这比写复杂的 `while` 条件更不容易出 Bug。
- **状态标志位（Flag）**：每一轮循环开始，**第一件事**就是把 `found` 设为 `false`。
- **局部变量初始化**：永远不要写 `int count;` 然后就开始 `count++`。

---
## **Related**