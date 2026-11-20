---
aliases: [FCB]
---

## Definition

The OS structure holding one file's metadata and the location of its data — the Windows name. FAT: the directory entry is the FCB; NTFS: one [[Master File Table|MFT]] record; UNIX: the [[Inode|inode]] is the equivalent. It carries attributes and block pointers, never the path.

---
## **Related**

[[Inode]] — the UNIX equivalent.
[[Master File Table]] — where NTFS keeps FCBs.
[[Directory File]] — FAT's name-to-FCB mapping.
