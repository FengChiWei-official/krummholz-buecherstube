---
aliases:
---

## Definition

The per-block-group array of inodes; the inode number selects a slot (`group = (ino - 1) / inodes_per_group`, then the index in that group's table). At 256 B per inode, a 4 KiB block holds 16.

---
## **Related**

[[Links of File System Entities]] — the array behind every inode number.
[[Inode]] — the record this table stores.
