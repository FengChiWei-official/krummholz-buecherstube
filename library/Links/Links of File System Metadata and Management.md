---
aliases:
---

## 定位

[[Links of File System Entities]] 讲实体与层间关系；这里讲**元数据**与**非文件空间**的管理。

## 1 地址系统

[[Sector|扇区]]头自带地址 + ECC：由**低级格式化**写入，OS 不可见。

```
盘面 H · [[Track|磁道]] · [[Cylinder|柱面]] C · 扇区 S
扇区地址 = (C, H, S)              ← CHS 三元组
块 = 2^k 连续扇区
块地址   = (C, H, B, o)           ← S 拆成 块起始扇区 B + 块内偏移 o
虚拟化   = (LBN, o)               ← 映射层（dm/LVM）替换前三元
```

- `0 ≤ o < blk`；前三元是物理几何，虚拟化后只剩 LBN。
- 换算（[[Logical Block Addressing|LBA]]）：`LBA = (C × heads + H) × SPT + (S − 1)`。
- 例：512 B 扇区 · 4 KiB 块 = 8 扇区；字节 9000 → `9000 / 4096 = 2`、余 808 ⇒ `(LBN 2, o 808)`。

## 2 fs 级全局元数据

| 元数据 | 内容 | 用途 |
|---|---|---|
| [[Boot Sector]] | 引导代码 + [[BIOS Parameter Block]]（BPB · 起始 LBA · 几何 · 跳转） | BIOS/UEFI 读入 → 引导加载器 → OS |
| [[Superblock]] | blk size · 块数 · inode 数 · 空闲计数 · magic · 状态 | fs 全局参数 · 挂载锚点 · EXT4 有备份 |
| [[Free Space Management]] | bitmap（1 bit/块）· 空闲链 · FAT 空闲项 | 分配器查询 |
| 分配区 | FAT（链）/ [[Inode Table]]（索引） | 块 ↔ 文件 |

- 引导扇区严格说属引导层，和 fs 一起布局，**不描述文件**。
- FAT：无 inode；文件元数据（名 · 大小 · 首簇）在目录项，链到 EOF。
- EXT4：inode table 与 bitmap 按块组分布；superblock 备份在若干块组。

## 3 文件级元数据

- [[Inode]]：属性 + 索引（extent tree / direct+indirect）+ 计数（`i_nlink` · `i_count`）。
- [[File Control Block|FCB]]（NTFS 的 [[Master File Table|MFT]] 记录）≈ inode；FAT 没有这一层。
- 目录项：`name → ino`；目录本身也是文件（有 inode、有数据块）。

## 4 文件间关系：目录

```
root ino → dentry → 目录块 → dirent → ino → inode
```

- 目录 = 记录型文件，内容 `名称 : inode 号码`；目录 + 文件 = DAG。
- 硬链接 = 同 ino 的第二个 dirent；`link(2)` 目录 ⇒ `EPERM`。
- 路径解析每一跳都是一次潜在盘读；[[Dentry|dentry 缓存]] + 内存 inode 摊掉重复。

## 5 空闲空间管理

| 方法 | 结构 | 查找 |
|---|---|---|
| bitmap | 1 bit/块 | 扫描 0 / 连续 run |
| 空闲链 | 链空闲块 | 取头 O(1) |
| FAT | 链上 0 = 空闲 | 顺序扫描 |
| 成组链接 | 组内 n 块 + 下一组指针 | 取组头 |

- 分配策略：首次适配 · 下次适配 · 最佳适配；优先同柱面 / 同块组以减少寻道。

## 算例

- 4 KiB 块 · 512 B 扇区 ⇒ 8 扇区/块；1 TiB ⇒ $2^{28}$ 块；bitmap = $2^{28}$ bit = 32 MiB。
- inode 256 B ⇒ 4 KiB 块存 16 个；$2^{20}$ 个 inode 的 table ≈ 256 MiB。

## 相关

- [[Links of File System Entities]] — 实体与层。
- [[CHS Address]] — 三元组 / 四元的卡片。
- [[Concept of Operating System]] — 元数据的上层使用者。
- [[408 文件管理-应试提纲]] — 空闲管理与分配的考点形式。
