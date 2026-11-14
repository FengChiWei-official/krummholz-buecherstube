---
aliases:
  - MAR
---

## Definition

Holds the address currently placed on the memory bus: the [[Program Counter|PC]] value during an instruction fetch, the computed effective address during a data access. MAR belongs to the classic von Neumann datapath model and x86 has no register of this name — the address is produced by operand decoding and handed to the load/store unit, never held in a register the ISA lets you name.

---
## **Related**

[[Memory Data Register]] — the datum that travels with the address.
[[Program Counter]] — the fetcher's source of addresses.
