---
aliases:
---

## Definition

The textbook name for the set of `struct file` objects; Linux keeps no single global array, and `f_count` counts every fd-table reference. Many fds can share one entry (`dup`, `fork`); a second `open` creates a new one.

---
## **Related**

[[Links of File System Entities]] — the shared-session layer.
[[Struct File]] — one entry in this set.
[[Process-Level File Descriptor Table]] — the per-process references.
