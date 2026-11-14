---
aliases:
  - 数据通路
---

## Definition

The part of the CPU that carries and transforms data: the register file, the [[Arithmetic Logic Unit|ALU]] and [[Floating-Point Unit|FPU]], the internal buses, and the muxes that choose between them. It holds the state and offers the operations, but every choice it makes — which input a mux passes, whether a register latches, whether memory is written — is delivered by the [[Control Unit|CU]]. On its own it is a fixed circuit: same adder, same muxes, no program.

---
## **Related**

[[Control Unit]]: **components / structures at the same hierarchical level**.
[[Register]] — the datapath's storage cells.
[[CPU as a State Machine]] — the datapath is the state side of the machine.
