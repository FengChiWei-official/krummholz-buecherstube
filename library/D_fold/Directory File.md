---
aliases:
---

## Definition

A file whose data blocks hold directory entries (`inode number + record length + name length + file type + name`). `x` permission means searchable, `r` listable; the name lives here, not in the inode.

---
## **Related**

[[Links of File System Entities]] — the namespace layer.
[[Inode]] — the target of a directory entry.
[[Dentry]] — the in-memory name-to-inode cache, distinct from the on-disk entry.
