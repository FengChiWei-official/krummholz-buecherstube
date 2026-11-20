---
aliases: [引导扇区, VBR, Volume Boot Record]
---

## Definition

The first sector of a volume (LBA 0): boot code plus a [[BIOS Parameter Block|BPB]], ending in the `0x55AA` signature. BIOS/UEFI loads it and jumps into it. On a whole disk LBA 0 is the MBR with the partition table; inside a partition it is the volume boot record.

---
## **Related**

[[BIOS Parameter Block]] — the volume layout record carried inside it.
[[Sector]] — the 512 B it occupies.
[[Links of File System Metadata and Management]] — boot-time metadata layer.
