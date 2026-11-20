---
aliases:
---

## Definition

An EXT4 block-map entry describing a contiguous run: logical start, length, physical start (12 B inline; `i_block[15]` holds four, then a tree). One extent covers many blocks.

---
## **Related**

[[Links of File System Entities]] — the modern block map.
[[Inode]] — the record that holds the extent tree.
[[Logical Block]] — what an extent maps.
