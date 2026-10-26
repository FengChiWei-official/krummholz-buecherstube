# ISA 与 OS 的数据结构 + 内存分布（参考）

> **原材料（or/）**：AI 整理的参考表。用途：把「机制在 ISA / 内容在 OS」落到具体物。具体数值随平台/版本变，见文末边界。

## 一、分类轴：三层，不是两层

| 层 | 谁定义 | 例子 | 判据 |
|---|---|---|---|
| **A. 格式（ISA）** | 硬件定死 | PTE、IDT 项、段描述符、陷阱帧 | 软件**必须**按这个格式填，填错就是非法 |
| **B. 位置（OS）** | OS 决定 | 页表放哪、IDT 放哪、几级页表 | ISA 只要求"基址写进某个寄存器" |
| **C. 内容与上层结构（OS）** | OS 自由定义 | PCB、VMA、页框分配器、文件系统 | 硬件完全不知道它们存在 |

## 二、表 A：ISA 定义的格式

### x86-64（4 级分页）

**PTE（8 字节/项，512 项 = 4 KiB 表）**：`P(0) R/W(1) U/S(2) PWT(3) PCD(4) A(5) D(6) PS(7) G(8) 可用(9–11) 物理地址(12–51) 可用(52–62) NX(63)`
四级：PML4 → PDPT → PD → PT，每级 9 位索引 + 12 位页内偏移（48 位虚拟地址）。

**段描述符（GDT 项，8 字节）**：`limit(20) base(32) type(4) S DPL(2) P AVL L D/B G`。64 位下基本平坦（base=0，limit 全）。

**中断门 / 陷阱门（IDT 项，16 字节）**：`offset(64) selector(16) IST(3) type(4) DPL(2) P(1)`。type `0xE`=中断门（清 IF）、`0xF`=陷阱门。

**陷阱帧（硬件压栈的最小现场）**：特权级切换时压 `SS, RSP, RFLAGS, CS, RIP`（5×8=40 字节）+ 某些异常的错误码。**其余现场由 OS 压。**

**控制寄存器**：CR0（PG/PE/WP）、CR2（缺页地址）、CR3（页表根 = OS 的改名机手柄）、CR4（PAE/PGE）、CR8（优先级）；MSR：EFER（长模式）、APIC base、TSC 相关。

**TSS**：RSP0——特权级切换时内核栈从哪来。

### RISC-V（Sv39）

**PTE（8 字节）**：`V(0) R(1) W(2) X(3) U(4) G(5) A(6) D(7) RSW(8–9) PPN(10–53) 保留(54–60) N(63)`
三级：VPN[2]/VPN[1]/VPN[0] 各 9 位 + 12 位偏移。

**satp**：`MODE(4) ASID(16) PPN(44)` —— 对应 x86 的 CR3（含 ASID，切换进程不必刷 TLB）。

**陷阱 CSR**：`sepc`（返回地址）、`scause`、`stval`、`sstatus`（SPP=前一模式，SIE/SPIE）、`stvec`（入口）、**`sscratch`**——存内核栈指针：用户态时它是内核 sp，陷入后第一条指令交换 sp 与 sscratch，**这是"从用户栈切到内核栈"的唯一依靠**。

**无 GDT / 无段**；物理内存保护用 PMP。

## 三、表 B：OS 定义的数据结构

### 概念必需（任何 OS 都要有）

| 结构 | 内容 | 为什么必需 |
|---|---|---|
| **PCB / 进程控制块** | 状态、寄存器上下文、页表根、内核栈指针、调度信息、打开文件表指针 | CPU 里没有"进程表"，上下文只存在内存 |
| **页表树** | 逐级 PTE（ISA 格式）+ OS 选的组织 | 地址手柄的落点 |
| **就绪/等待队列** | 调度所需的全部状态 | "下一个跑谁"没有任何地方由硬件决定 |
| **打开文件表** | 文件描述符 → 文件对象 | 名字空间与持久性 |
| **中断向量表内容** | 每个向量 → 处理程序地址 | 控制权移交的去处 |
| **页框分配器** | 物理页的账本 | 物理内存要有人记账 |
| **内核栈** | 每主体一份，特权级切换时用 | 陷阱帧只压最小现场 |

### Linux 的具体实现（记住即可，不必当通则）

`task_struct`、`mm_struct`（pgd、VMA 树、start_brk/brk/start_stack）、**`vm_area_struct`（VMA：一段虚拟地址区间的属性——硬件只知 PTE，OS 用它管理"还没映射的地址"）**、`struct page` 数组（vmemmap，每物理页一个描述符）、`zone`（DMA/DMA32/NORMAL）、buddy 的 `free_area[]`（MAX_ORDER=11）、`kmem_cache`（slab/slub）、`files_struct`/`fdtable`/`file`/`inode`/`dentry`/`super_block`（VFS）、页缓存（xarray 按 inode+offset 索引）、`sys_call_table[]`、`idt_table`、`gdt_page`、`swapper_pg_dir`（内核页表根）、`init_task`。

## 四、内存分布

### 图 1 · 物理地址空间（x86-64 PC，简化）

```
0x00000000 ┌──────────────────────────┐
           │ 实模式 IVT (1 KiB)        │ ← 自举遗留
0x00000400 │ BIOS 数据区 (BDA)         │
0x00000500 │ 可用低内存（MBR 曾载入 0x7C00）│
0x0009FC00 │ EBDA                     │
0x000A0000 ├──────────────────────────┤ 640 KiB 传统内存上限
           │ 显存 / VGA (128 KiB)      │ 设备，不是内存
0x000C0000 │ 显卡 / BIOS ROM           │ 映射到 ROM
0x00100000 ├──────────────────────────┤ 1 MiB
           │ 内核镜像 + 可用 RAM       │ ← 内核加载/解压处
           │ ……（RAM 顶端）            │
           ├──────────────────────────┤
           │ PCIe MMIO 空洞            │ 设备寄存器映射区
           │ LAPIC / IOAPIC / HPET     │ 中断控制器
0xFFF00000 │ 固件 ROM                  │
0xFFFFFFF0 │ 复位矢量                  │ ← 上电第一条指令
0xFFFFFFFF └──────────────────────────┘
           （4 GiB 之上继续放 RAM：PCI 空洞之后）
```

**关键**：物理地址空间不是"内存"，而是**内存 + 设备 + 固件共用的一张地址表**。OS 从固件拿到的 **e820 / boot_params** 表，就是这张图。

### 图 2 · 进程虚拟地址空间（Linux x86-64 经典）

```
0x0000000000000000  不可映射（NULL 陷阱页）
0x0000000000400000  .text（ELF 典型入口）→ .data / .bss
                    ↓ brk
                    堆（向高增长）
                    未映射空洞（VMA 之间的洞）
                    ↑ mmap 区（共享库、文件映射，向低增长）
                    栈（向低增长）
0x00007fffffffffff  ← 用户空间顶（TASK_SIZE）
══════════════════ 边界：用户态不可见
0xffff800000000000  内核直接映射 physmap（物理内存的线性映射）
                    内核文本 / vmalloc / 模块
0xffffffffffffffff  内核空间顶
```

### 图 3 · 内核自己的三个视图（为什么内核能"看穿"）

| 视图 | 含义 |
|---|---|
| **physmap（直接映射）** | 物理内存线性映射进内核空间，`virt = phys + PAGE_OFFSET`——内核随手能碰任何物理页 |
| **vmemmap** | `struct page` 数组本身占物理内存，也被映射进来 |
| **每进程页表含内核映射** | 陷入内核不必换页表（KPTI 例外：现在要切 CR3）|

Linux x86-64 典型分带（KASLR 随机化基址）：physmap 64 TB / vmalloc 32 TB / vmemmap / cpu_entry_area / 内核文本。

## 五、边界

1. **格式是 ISA 的，位置与大小是 OS 与平台的**：48 位 vs 57 位、KASLR/ASLR、x86 vs RISC-V、UEFI vs BIOS 都会改数值。
2. **表 B 的"Linux 实现"不是通则**：`struct page`/slab/VMA 是 Linux 的选择；微内核/RTOS 完全不同。区分"概念必需"与"某实现"。
3. **两张内存图不可混**：物理地址空间图**机器唯一**；虚拟地址空间图**每进程一份**。
4. **408 用简化模型**：一级/两级页表、固定地址、Cache 行结构——别把真机地址套进考题。
5. **考纲对照**：ch3 = 图 2 + PTE + TLB；ch4 = 指令格式与寻址；ch5 = 陷阱帧 + 控制寄存器 + IDT；ch7 = 图 1 里的设备寄存器与 DMA 描述符（第二套约定）。

---

## Related

- [[What the CPU Promises and What the OS Defines]] — 本表是那条结论的具体化：A 层=CPU 承诺，B/C 层=OS 定义。
- [[Physical Address as Global Identity]] — 图 1 与 CR3/satp 的位置。
- [[Storage Hierarchy as Distance]] — 图 3 的 physmap 是"距离"在 OS 侧的体现。
