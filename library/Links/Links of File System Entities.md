---
aliases:
---

## 三层

```
设备 → 块层 → fs        （OS 在最上层，把 fs 当文件用）
```

## 实体图

| 层 | 实体 | 单位 |
|---|---|---|
| 设备 | 扇区 | [[Sector]] |
| 块层 | 逻辑块 · LBA | [[Logical Block]] · [[Logical Block Addressing]] |
| fs | fs block · 簇 · inode · dirent | [[File System Block]] · [[Cluster]] · [[Inode]] |
| OS | dentry · struct file · fd | [[Dentry]] · [[Struct File]] · [[File Descriptor]] |

## 1 设备

- 硬盘看见 [[Sector|扇区]]：**扇区 → [[Track|磁道]] → [[Cylinder|柱面]] → 硬盘**。

- 扇区 = 最小可寻址 · 最小传输 · 最小 ECC 单位。
- 512e：逻辑 512 B / 物理 4 KiB（盘内 RMW）；4Kn：逻辑 = 物理。

## 2 块层（block layer）

- 设备 → 块层：暴露**逻辑块设备**，I/O 单位 = logical block（512 B / 4 KiB），地址 = [[Logical Block Addressing|LBA]]。
- 块层**不**把扇区绑成更大的块：bio + 队列 + 调度器只做合并/排序，不拆到逻辑块以下。
- 映射（分区表 · dm · LVM）在 LBA 之上：虚拟块空间 → 物理块，底层实现留灵活度。
- “连续扇区绑定成块”发生在 **fs**：`mkfs` 定 blk size = $2^k$ 扇区（[[File System Block|fs block]] / [[Cluster|簇]]）。

```
 物理盘                              fs 块空间（mkfs 定）
 ┌────┬────┬────┬────┬────┬────┐    ┌───────────────┬───────────────┐
 │ s0 │ s1 │ s2 │ s3 │ s4 │ s5 │ ─▶ │ blk0 = s0..s1 │ blk1 = s2..s3 │ …
 └────┴────┴────┴────┴────┴────┘    └───────────────┴───────────────┘
       └──────── 连续扇区 = 一个块 ────────┘

 虚拟块空间（dm/LVM）                 物理块（LBA）
 ┌───────┬───────┬───────┐          ┌───────┬───────┬───────┐
 │ LBN 0 │ LBN 1 │ LBN 2 │ ──映射──▶ │ blk 7 │ blk 3 │ blk 9 │
 └───────┴───────┴───────┘          └───────┴───────┴───────┘
```

## 3 fs：文件概念

- 文件 = 被分配的若干块 / [[Cluster|簇]]（小文件可内联，占 0 块）。
- 块之间的关系 = 文件的分配方式（物理实现方式）；主流 = 索引分配 + 额外一个 [[Inode|inode]] 作元数据。
- 目录 = 记录型文件：`名称 : inode 号码`；目录 + 文件 = [[Directed Acyclic Graph|DAG]]，用来整理文件空间。

实现视角下的文件空间：

```
 裸块空间：只有块，没有名字，彼此不可区分
 ┌───────────┬──────────┬────────┬──────┬────────┐
 │ inode tbl │ 根目录块 │ 数据块 │ 空块 │ 数据块 │
 └───────────┴──────────┴────────┴──────┴────────┘
        ▲           │
        │           └── dirent：name → ino
        │
        └── inode ──▶ 数据块（extent / 索引）

 无法识别的：inode table、根目录、其他被索引的块 —— 混在空块里，索引空间内看不见名字。
```

## OS：文件是绝对主角

- 文件被抽象成**打开事件**。
- 内存 inode = 文件本身的代理人；`i_count` = 指向它的 struct file 数（二次 `open` 才 +1，`dup`/`fork` 不加）。
- open 本身由 [[Struct File|struct file]] 表征；同一 superblock 的 sf 由 `f_list` 侵入式链表串起 = [[System-Wide Open File Table|系统打开文件表]]。
- 每个进程一个指针数组，记录自己用到的 sf = 系统表的一个切片；下标 = [[File Descriptor|fd]]。
- `dup`：进程添加新项，内容是指向原有 struct file 的指针。
- `fork`：新进程拷贝一份数组 —— fork 之后的 open 子进程看不见；fork 之前的 open，两边指针指向同一对象。

```
          进程 A                          系统打开文件表
     fd ┌────┬──────────────┐
      0 │ ●──┼──▶ file#1  ──┼──┐  f_count=2  f_pos=4096
      3 │ ●──┼──▶ file#2  ──┼─┐│  f_count=1  f_pos=0
        └────┴──────────────┘ ││
                               │└──▶ inode#42  i_count=2
          进程 B               │
     fd ┌────┬──────────────┐ │
      3 │ ●──┼──▶ file#1  ──┼─┘   （fork 拷贝数组，同对象）
        └────┴──────────────┘

 dup(0) ⇒ 再加一项指向 file#1，f_count=3，无新会话
```


### OS中作为元数据的目录文件


os以路径为检索的关键词，加载文件之前要逐级访问目录文件， 系统中专门保存着目录项和根据inode生成的内存中的inode。

## 相关

[[Concept of Operating System]] · [[Index of Operating System]] · [[408 文件管理-应试提纲]] · [[ISA 与 OS 的数据结构与内存分布]]

## 节点

[[Sector]] · [[File System Block]] · [[Cluster]] · [[Logical Block]] · [[Inode]] · [[Inode Table]] · [[Directory File]] · [[Dentry]] · [[Superblock]] · [[File Descriptor]] · [[Process-Level File Descriptor Table]] · [[Struct File]] · [[System-Wide Open File Table]] · [[Page Cache]] · [[Extent]] · [[Indirect Block]] · [[VFS (Virtual File System)]]
