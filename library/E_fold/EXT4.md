---
aliases:
---

## Definition

The default Linux filesystem in this stack: block sizes of 1, 2 or 4 KiB capped at the page size, a per-block-group inode table, and extent trees for block mapping. `bigalloc` adds a cluster above the block.

---
## **Related**

[[Links of File System Entities]] — the reference filesystem for the stack.
[[File System Block]] — EXT4 allocates in blocks.
[[Inode Table]] — the per-group array EXT4 uses.
[[Extent]] — the modern block map.
