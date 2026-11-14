---
aliases:
  - CS
  - DS
  - SS
  - ES
  - FS
  - GS
---

## Definition

Holds a segment selector, which in 16-bit code supplied a base address for every memory access. In 32- and 64-bit flat mode the code and data bases are zero, so CS, DS, SS and ES stop mattering — but FS and GS keep a base the OS sets, and that base is the one thing every thread and every CPU core needs to find without an argument:

- Linux x86-64: FS holds the thread's TLS pointer (`arch_prctl`), which is why the stack canary is `fs:[0x28]`; in kernel mode GS holds the per-CPU block, so the current task is reachable without a register argument.
- Windows: FS on 32-bit and GS on 64-bit point at the TEB, from which the PEB is reached — the first thing shellcode and anti-debug code resolve.

---
## **Related**

[[Threads' Registers]] — the TLS block the FS base points at is per thread.
[[Control Register]] — the other register that holds a privileged base.
[[Kernel Mode]] — where the GS base is swapped to per-CPU state.
