---
aliases:
---

## Definition

The per-process array of `struct file *` (Linux `files_struct` → `fdtable`) plus the `open_fds` and `close_on_exec` bitmaps. `fork` copies the table and takes a reference on each entry.

---
## **Related**

[[Links of File System Entities]] — the per-process side of the open-file model.
[[File Descriptor]] — an index into this table.
[[System-Wide Open File Table]] — the sessions the entries point to.
