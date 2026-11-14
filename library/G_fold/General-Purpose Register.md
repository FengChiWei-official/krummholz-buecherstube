---
aliases:
  - GPR
---

## Definition

A register the instruction encoding addresses by number without reserving a function: on x86-64, RAX, RBX, RCX, RDX, RSI, RDI, RSP, RBP and R8–R15, each reachable under 8-, 16-, 32- and 64-bit names. "General" describes the encoding, not the use — `MUL`/`DIV` (RAX, RDX), `REP` (RCX), `SHL` (CL), string moves (RSI, RDI), `syscall` (RAX) and the SysV argument order all pin specific registers to specific jobs.

---
## **Related**

[[Register]] — GPR is the register class whose encoding reserves nothing.
[[Stack Pointer]] — the GPR whose role the hardware fixes.
[[Links of Registers]] — the roles pinned on each of the eight.
