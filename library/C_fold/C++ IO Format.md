---
tags:
  - type/permanent
  - status/in-progress
  - topic/learning
  - attr/concept
---
## 省流

```
#include<iostream>
#include<iomanip>

cout << fixed << setprecision(6) << pi << '\n';

```
## Definition

To make quick reference easier during daily development, the C++ `iostream` formatting techniques, common pitfalls, and modern alternatives are summarized below:

### 1. 头文件分工（有无参数决定头文件）
* **`<iostream>`**：提供基础流和**无参数**的操纵符（如 `fixed`, `hex`, `boolalpha`, `endl`）。
* **`<iomanip>`**：提供**带参数**的格式化操纵符（如 `setw`, `setprecision`, `setfill`）。

---

### 2. Quick reference for common formatting scenarios

| Need | Manipulator | Example | Result |
| :--- | :--- | :--- | :--- |
| **Significant digits (N)** | `setprecision(N)` | `cout << setprecision(3) << 12.345;` | `12.3` (rounded) |
| **Fixed N decimal places** | `fixed << setprecision(N)` | `cout << fixed << setprecision(3) << 12.3;` | `12.300` (padded) |
| **Width and fill** | `setw(N) << setfill(C)` | `cout << setw(4) << setfill('0') << 5;` | `0005` (**`setw` applies only once**) |
| **Hex with prefix** | `hex << showbase` | `cout << hex << showbase << 42;` | `0x2a` |
| **Print `true`/`false`** | `boolalpha` | `cout << boolalpha << true;` | `true` |

---


### 3. Three common pitfalls

1. **`setw(n)` is one-shot**:
   Most manipulators persist, but **`std::setw` affects only the next output item**. For multiple aligned columns, call `setw` before each column.
2. **Global state pollution and restoring**:
   Manipulators like `fixed`, `hex`, or `boolalpha` change the stream's global state. Restore them when no longer needed, otherwise subsequent prints may be affected:
   ```cpp
   std::cout << std::defaultfloat; // 恢复默认浮点数格式
   std::cout << std::dec;          // 恢复十进制
   std::cout << std::noboolalpha;   // 恢复布尔值为 0/1
   ```
3. **字符/指针打印陷阱**：
   * **字符转 ASCII 码**：`char` 必须强转为整型才能输出数值（`static_cast<int>(ch)`）。
   * **`char*` 打印地址**：直接打印 `char*` 会输出其指向的字符串内容。如果想打印该指针本身的地址，必须将其强转为 `void*`（`static_cast<const void*>(ptr)`），否则容易因为找不到 `\0` 导致程序崩溃。

---

### 4. Modern C++ trends
Because `iostream` manipulators can modify global stream state and are sometimes verbose, modern C++ introduced safer and more concise formatting approaches:
* **C++20**：引入了 `<format>` 库（类似 Python 的格式化语法），如 `std::format("PI: {:.2f}", 3.1415)`。
* **C++23**：引入了 `<print>` 库，支持直接通过 `std::print` 或 `std::println` 打印，不再依赖传统的 `std::cout` 操纵符。

---
## **Related**