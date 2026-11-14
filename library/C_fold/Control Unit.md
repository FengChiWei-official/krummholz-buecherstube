---
aliases:
  - CU
---

## Definition

Decodes the instruction held in the [[Instruction Register|IR]] and emits the control signals the datapath needs for this cycle: which mux input to select, which register to write, which ALU operation to run, whether memory is read or written. It carries no data — its outputs are single-bit enables and short select fields, never an operand — and it is the part of the CPU whose job is to decide rather than to compute or store. Branches make it read the flags, so its inputs are instruction encoding, flags and clock.

---
## **Related**

[[Datapath]]: **components / structures at the same hierarchical level**.
[[Instruction Register]] — the register it decodes.
[[CPU as a State Machine]] — CU is the transition function, built out of gates.
