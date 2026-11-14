---
aliases:
  - 转发
  - 旁路
  - 数据旁路
---

## Definition

Sending a result forward from a pipeline register to the stage that needs it instead of waiting for write-back; a load-use pair still costs one stall, because the datum exists only at the end of MEM.

---
## **Related**

[[Data Hazard]] — what it exists to remove.
[[Pipeline]] — the registers it reads from.
