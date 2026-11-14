---
aliases:
  - MDR
  - MBR
---

## Definition

Holds the datum in transit between memory and the CPU, so one memory port serves both directions and both widths. A fetched instruction passes through MDR into the [[Instruction Register|IR]]; a loaded operand passes through it into a [[General-Purpose Register|GPR]]. Like [[Memory Address Register|MAR]], it is a datapath-model register with no name in the x86 ISA.

---
## **Related**

[[Memory Address Register]] — the address half of the same bus cycle.
[[Instruction Register]] — the destination of an instruction fetch.
