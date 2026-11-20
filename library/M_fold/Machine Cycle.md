---
aliases:
---

## Definition

The time to complete **one basic operation**; in practice, one memory access — one bus transaction. Its length is set for the whole machine by the slowest basic operation (fixed-length machine cycle), or per kind of operation (variable-length).

Chinese textbooks call it 机器周期 or CPU 周期. The canonical hardware instance is the Intel 8080/Z80 **M cycle**: `M1` is the opcode fetch, and every memory or I/O access is one M cycle of 3–6 T states.

It died with the pipeline: once the datapath was cut into stages, the unit that decides everything became the stage — one clock period — and "one basic operation" stopped being an integer number of them. A load is one cycle on a hit and several on a miss.

---
## **Related**

[[Links of Periods in the Computer]]: where this unit is compared with the two around it.
[[Instruction Cycle]]: one level up — a sequence of machine cycles.
[[Clock Beat]]: the beat inside a machine cycle; dead with it.
