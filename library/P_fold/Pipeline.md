---
aliases:
  - 流水线
  - 指令流水线
---

## Definition

Overlapping instructions by cutting the [[Datapath|datapath]] into stages separated by registers: one instruction issues per cycle, and each still takes as many cycles as there are stages.

---
## **Related**

[[Datapath]] — what gets cut; since the boundary is a register, the cycle time is the slowest stage, not the whole instruction.
[[Control Unit]] — cut with it: each stage carries its own slice of control signals forward alongside its data.
[[时空互换]] — the trade it makes: duplicate hardware to raise throughput, never to shorten one instruction's latency.
[[Structural Hazard]] — it stalls three ways; the first is a missing resource.
[[Data Hazard]] — the second: a value that has not arrived.
[[Control Hazard]] — the third: the next address is not yet known.
[[Superscalar]] — what it is when the width goes past one instruction per cycle.
[[Out-of-order Execution]] — what it becomes when the order stops being fixed.
