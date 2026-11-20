---
aliases: [BPB]
---

## Definition

The volume layout record inside the [[Boot Sector|boot sector]]: bytes per sector, sectors per cluster, reserved sectors, number and size of FATs, root entries, total sectors, media descriptor, sectors per track, heads, hidden sectors. FAT/NTFS read it to locate the FAT, the root directory and the data region.

---
## **Related**

[[Boot Sector]] — where the BPB lives.
[[FAT]] — whose geometry the BPB fixes.
[[NTFS]] — also keeps a BPB in its volume boot record.
