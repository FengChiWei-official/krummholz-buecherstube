---
aliases: [MFT, $MFT]
---

## Definition

NTFS's metadata file `$MFT`: an array of records (1 KiB by default), one per file; the record number is the file ID. Each record is a set of attributes — Standard Information, File Name, Data, … — and small data is resident inside the record while large data is non-resident and points at clusters.

---
## **Related**

[[NTFS]] — the filesystem that owns the MFT.
[[File Control Block]] — the MFT record is NTFS's FCB.
[[Inode]] — the equivalent index record in UNIX filesystems.
