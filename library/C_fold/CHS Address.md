---
aliases: [CHS, Cylinder-Head-Sector]
---

## Definition

硬盘的物理地址三元组 `(C, H, S)`：柱面 C（同半径磁道集合）· 磁头 H（盘面号）· 扇区 S（磁道内序号）。**低级格式化**写入每个扇区的 header。

块存在后，S 拆成 `(块起始扇区 B, 块内偏移 o)` ⇒ 四元 `(C, H, B, o)`。
虚拟化替换前三元：`(C, H, B) → LBN`，偏移 `o` 保留。

```
LBA = (C × heads + H) × sectors_per_track + (S − 1)
```

---
## **Related**

[[Sector]] — 三元组直接指向的对象。
[[Logical Block]] — 虚拟化后的块地址。
[[File System Block]] — 连续扇区绑定的块。
[[Links of File System Metadata and Management]] — 地址系统在元数据笔记中的位置。
