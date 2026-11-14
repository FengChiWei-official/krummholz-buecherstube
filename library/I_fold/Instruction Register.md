---
aliases:
  - IR
---

## Definition

Holds the instruction word fetched from the address in [[Program Counter|PC]], so that the [[Control Unit|CU]] decodes one instruction at a time. IR has no user-visible name on x86: it is an implicit part of the fetch–decode–execute cycle, not an operand any instruction can name.

---
## **Related**

[[Program Counter]] — PC supplies the address, IR receives the word.
[[Control Unit]] — decodes the IR contents into control signals.
[[How does PC system work]] — the fetch half of the cycle this register sits in.
