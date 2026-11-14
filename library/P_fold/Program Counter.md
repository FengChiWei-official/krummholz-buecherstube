---
aliases:
  - Instruction Pointer
  - IP (Instruction Pointer)
  - PC(Register)
---

## Definition

Holds the address of the next instruction. Every fetch advances it by the length of the instruction just read, so a branch is simply a write to it. Intel calls it `IP`/`EIP`/`RIP`; x86-64 also reads it as an operand base, which is how `RIP`-relative addressing makes the code's own position visible.

---
## **Related**

[[Instruction Register]] — the register the fetched word lands in.
[[Stack Pointer]] — the other register a `CALL` writes without naming it.
[[How does PC system work]] — the fetch loop PC drives.
[[Raw Index of Computer Systems]] — 登记主干
