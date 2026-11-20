---
aliases:
---

## Definition

The block number a file offset maps to before the inode translates it to a physical block: `offset / block_size`. Extents and indirect pointers perform that translation.

---
## **Related**

[[Links of File System Entities]] — the mapping layer between a file and its blocks.
[[File System Block]] — the unit a logical block is counted in.
[[Extent]] — one way to map a logical block to a physical one.
