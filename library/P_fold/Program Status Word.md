---
aliases:
  - PSW
  - FLAGS
  - EFLAGS
  - RFLAGS
---

## Definition

Holds the [[Arithmetic Logic Unit|ALU]]'s result state and the CPU's control bits in one word. The result state is what conditional jumps read: ZF (result zero), CF (unsigned carry or borrow), SF (sign bit set), OF (signed overflow). The control bit that matters most is IF, the interrupt enable that `CLI`/`STI` clear and set. Because a branch depends on it, the word is part of the state a context switch saves.

---
## **Related**

[[Arithmetic Logic Unit]] — produces the flags.
[[Control Unit]] — consumes them for conditional branches.
[[Threads' Registers]] — the PSW as per-thread saved state.
