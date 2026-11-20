---
aliases:
---

## Definition

One `address_space` per inode (`i_mapping`) holding file pages in an xarray indexed by page index. Reads hit it, writes dirty it, writeback flushes it; `O_DIRECT` bypasses it.

---
## **Related**

[[Links of File System Entities]] — the cache between reads/writes and the device.
[[Inode]] — the object whose `i_mapping` owns the cache.
[[Struct File]] — the open session whose `f_mapping` reaches it.
