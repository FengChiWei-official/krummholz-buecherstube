---
aliases:
---

## Definition

The allocation unit of a filesystem: $2^k$ sectors fixed at `mkfs` time. EXT4 uses 1, 2 or 4 KiB and never exceeds the page size; the bitmap, FAT/indirect pointers and `i_blocks` account in blocks.

---
## **Related**

[[Links of File System Entities]] — the unit stack this card lays out.
[[Sector]] — one block is $2^k$ sectors.
[[Cluster]] — the FAT/NTFS name for the same allocation layer.
