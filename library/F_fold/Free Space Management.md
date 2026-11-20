---
aliases: [空闲空间管理]
---

## Definition

The structures that record which blocks are free plus the policy that picks among them: bitmap (1 bit per block), free list, grouped free list, FAT free entries. Policies: first fit, next fit, best fit; clustering by cylinder or block group cuts seeks.

---
## **Related**

[[File System Block]] — the unit being tracked.
[[FAT]] — its free entries double as the free list.
[[Links of File System Metadata and Management]] — where the management table lives.
