---
aliases:
---

## Definition

The register class for non-integer operands, in two generations. The x87 registers (`ST0`–`ST7`) form a stack: most arithmetic reads the top two entries and leaves the result on top, so operands are implied by position. The SSE/AVX registers (`XMM0`–`XMM15`, `YMM`, `ZMM`) are flat, and the three names are views of one register file at 128, 256 and 512 bits. `XMM0` is also the SysV channel for a float argument and for a float return value.

---
## **Related**

[[Floating-Point Unit]] — the unit that computes on them.
[[General-Purpose Register]] — the integer counterpart, and where addresses live.
[[Floating-Point Number IEEE 754]] — the encoding these registers hold.
