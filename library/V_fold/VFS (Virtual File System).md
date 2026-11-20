---
aliases:
---

## Definition

The kernel's filesystem-independent interface: `super_block`, `inode`, `dentry` and `file` objects plus operation tables (`file_operations`, `inode_operations`, …). It lets one `open/read/write` API cover ext4, FAT, procfs, pipes and sockets.

---
## **Related**

[[Links of File System Entities]] — the interface that binds the layers.
[[Inode]] — one VFS object.
[[Dentry]] — one VFS object.
[[Superblock]] — one VFS object.
[[Struct File]] — one VFS object.
