---
aliases:
---

## Definition

The allocation unit in FAT and NTFS: $2^k$ sectors, with one FAT entry per cluster; NTFS allows 512 B to 2 MiB. In 408 terminology a disk block and a cluster are synonyms, and EXT4 `bigalloc` uses a cluster above the block.

---
## **Related**

[[Links of File System Entities]] — block/cluster naming in the storage stack.
[[File System Block]] — the EXT4 name for the same allocation layer.
