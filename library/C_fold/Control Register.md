---
aliases:
  - CR0
  - CR2
  - CR3
  - CR4
---

## Definition

Privileged registers that configure the CPU rather than hold computation state; only ring 0 can read or write them.

- `CR0` — processor mode: PE (bit 0) enters protected mode, PG (bit 31) turns paging on, WP (bit 16) makes the kernel respect read-only pages.
- `CR2` — the linear address that caused the last page fault; the fault handler reads it instead of decoding the faulting instruction.
- `CR3` — the physical base of the top-level page table (PML4 on x86-64). Writing it is what a process switch means: new address space, TLB flushed unless PCID tags the entries.
- `CR4` — feature switches: PAE, SMEP and SMAP (kernel may not execute or read user pages), OSXSAVE (AVX state).

---
## **Related**

[[Page Table]] — the structure CR3 points at the root of.
[[Kernel Mode]] — the only mode allowed to touch them.
[[Segment Register]] — the other register that holds a privileged base.
