# Links of Registers 补写方案（D41 方案稿）

> 暂存稿（`a_sticker/or/`）。用途：把 2026-11-13 寄存器集群从「骨架」补成「卡 + 节点」，供 owner 逐条批准。
> 状态：**待批**。批准后这些正文才写进 `library/` 与根队列的目标笔记；未批前只在本文里。

## 一、现状（工具事实）

`vault.py place "Links of Registers"`：体裁 links、根队列、0 条登记边、出链 5、**入链 0**。

`## Definition` 现在是五个成员 + 一个空链接：

```
[[General-Purpose Register|GPR]]
[[Instruction Register|IR]]
[[Memory Address Register|MAR]]
[[Memory Data Register|MDR]]
[[Program Counter|PC]]/ [[Program Counter|IP]]
[[]]                     ← 空链接，删
```

缺的成员（owner 给的正文里出现、库里没有节点）：栈指针、标志寄存器、控制寄存器、段寄存器；并且 `[[Stack Pointer]]`、`[[Register]]` 两篇在 `library/` 里**登记了但正文全空**。

集群的节点全部还在根队列（G1「root drained」因此失败，23 篇里 9 篇属于本集群）。

同名冲突（`vault.py rename` 直接拒绝）：`Program Counter.md`（2026-11-13，带 `PC / Instruction Pointer / IP` 三条别名）与 `library/P_fold/Program Counter.md`（2026-10-26，空正文，挂着 `[[Raw Index of Computer Systems]]` 登记行）。两个同名文件 ⇒ `vault.py rename "Program Counter" …` 无法执行。

## 二、卡片成员表（本卡的骨架）

按「谁把职责焊死在它身上」分组，一组一类：

| 组 | 成员 | 硬编码的职责 |
|---|---|---|
| 指令流 | `Program Counter`、`Instruction Register` | 下一条指令的地址 / 正在译码的那条指令 |
| 访存 | `Memory Address Register`、`Memory Data Register` | 总线上的地址 / 总线上的数据 |
| 计算 | `General-Purpose Register`、`Floating-Point Register` | 整数与地址 / 浮点与向量 |
| 栈 | `Stack Pointer` | 栈顶；PUSH/POP/CALL/RET 隐式改它 |
| 状态 | `Program Status Word` | ZF/CF/SF/OF 与 IF；条件跳转读它 |
| 特权 | `Control Register`（新）、`Segment Register`（新） | 分页与模式开关 / FS·GS 的 TLS 与 per-CPU 基址 |

`General-Purpose Register` 的「专用化」（`RAX` 返回值与 syscall 号、`RCX`/`CL` 移位位数、`RDX` 乘除高位与端口号、`RSI`/`RDI` 串操作与 SysV 第 1/2 参数、`RBX` callee-saved）放进卡片的 **Perspectives**，不拆成节点 —— 一个想法一篇。

## 三、逐篇草案

### 1. `Links of Registers.md`（体裁 links → `library/Links/`）

```markdown
---
aliases:
---

## Definition

Members, grouped by what pins the job on them:

- [[Program Counter|PC · IP · RIP]] — the address of the next instruction; the register the fetch unit advances by itself.
- [[Instruction Register|IR]] — the instruction word currently being decoded.
- [[Memory Address Register|MAR]] — the address placed on the memory bus.
- [[Memory Data Register|MDR · MBR]] — the datum crossing the memory bus.
- [[General-Purpose Register|GPR · AX/BX/CX/DX/SI/DI/SP/BP]] — registers the encoding names by number with no reserved function; the ABI and a few instructions pin roles on them anyway.
- [[Stack Pointer|SP · ESP · RSP]] — the top of the stack; PUSH/POP/CALL/RET move it implicitly.
- [[Program Status Word|PSW · FLAGS · EFLAGS · RFLAGS]] — the ALU's result state; what conditional jumps read.
- [[Floating-Point Register|ST0–ST7 · XMM · YMM · ZMM]] — non-integer operands; XMM0 carries a float argument and the return value.
- [[Control Register|CR0–CR4]] — privileged mode and paging switches; CR3 is the page-table root.
- [[Segment Register|CS · DS · SS · ES · FS · GS]] — flat on x86-64 except FS/GS, which keep the TLS and per-CPU base.

## Perspectives

**One register file, four jobs**: carry data (GPR, XMM), carry addresses (PC, MAR, SP), carry state (PSW), carry mode (CR, segment base).

**Named by role, not by operand**: `MUL`/`DIV` read RAX and RDX implicitly, `REP` reads RCX, `SHL` reads CL, `syscall` reads RAX, `MOVS`/`STOS` read RSI and RDI. The instruction names the operation, not the operand.

**The ABI is a second, softer hardwiring**: RDI, RSI, RDX, RCX, R8, R9 are the first arguments in order, RAX the return value, RBX/RBP/R12–R15 callee-saved, RSP the stack. Same registers, roles fixed by convention instead of by circuit.

**Visibility is a third axis**: GPR, PC and PSW are readable in user mode; CR only at CPL0; the FS/GS base is swapped per thread (Linux `arch_prctl`) or per CPU (kernel GS), which is why it is the cheapest pointer to thread- and CPU-local state.

**Width is a historical stack, not a design**: AL/AH ⊂ AX ⊂ EAX ⊂ RAX is one register with nesting names, so 8/16/32/64-bit code shares one naming scheme — see [[Links of Word Size & Register Bit Width]].

## Distinctions

- **Register vs memory**: no address, no cache line, no bus; that is why [[Register]] is the general idea and this card is the individual jobs.
- **Architected vs internal**: RIP is the architected program counter; rename, reorder and reservation-station entries are the microarchitecture's own storage and have no name in the ISA.
- **PC vs IP**: the same register — `Program Counter` in architecture texts, `Instruction Pointer` in Intel's `IP`/`EIP`/`RIP`; `FS`/`GS` call it `RIP`-relative addressing when it appears in an operand.
- **PSW vs FLAGS**: PSW is the whole word including system bits (IOPL, VM, AC); FLAGS names the condition-code subset that arithmetic writes and jumps read.
- **Register class vs a thread's registers**: [[Threads' Registers]] is the same register set seen as the saved context of a context switch.
- **Other ISAs**: ARM's LR (x30) holds the return address instead of pushing it; RISC-V's x0 reads as zero and ignores writes. x86 has neither — every x86 register is mutable state.

## Examples

- `mov rax, qword ptr fs:[0x28]` — read the stack canary from the TLS block at function entry (Linux x86-64).
- `mov cr3, rax` — switch address spaces: new page-table root, TLB flushed (unless PCID).
- `shl eax, cl` — the shift amount can only come from CL.
- `div ecx` — divides EDX:EAX; quotient lands in EAX, remainder in EDX.

---
## **Related**

[[Register]] — the general idea this card instantiates.
[[CPU as a State Machine]] — the registers are the state; PC and PSW are what the transition function reads.
[[How does PC system work]] — where PC, IR, MAR and MDR sit on the fetch–execute path.
[[Threads' Registers]] — the same register set as per-thread saved context.
[[Process Control Block]] — the place PC, SP and PSW are stored when a process is switched out.
[[Links of Word Size & Register Bit Width]] — why one register carries 8/16/32/64-bit names.
```

### 2. `General-Purpose Register.md`（→ `library/G_fold/`）

```markdown
---
aliases:
  - GPR
---

## Definition

A register the instruction encoding addresses by number without reserving a function: on x86-64, RAX, RBX, RCX, RDX, RSI, RDI, RSP, RBP and R8–R15, each reachable under 8-, 16-, 32- and 64-bit names. "General" describes the encoding, not the use — `MUL`/`DIV` (RAX, RDX), `REP` (RCX), `SHL` (CL), string moves (RSI, RDI), `syscall` (RAX) and the SysV argument order all pin specific registers to specific jobs.

---
## **Related**

[[Register]] — GPR is the register class whose encoding reserves nothing.
[[Stack Pointer]] — the GPR whose role the hardware fixes.
[[Links of Registers]] — the roles pinned on each of the eight.
```

### 3. `Instruction Register.md`（→ `library/I_fold/`）

```markdown
---
aliases:
  - IR
---

## Definition

Holds the instruction word fetched from the address in [[Program Counter|PC]], so that the [[Control Unit|CU]] decodes one instruction at a time. IR has no user-visible name on x86: it is an implicit part of the fetch–decode–execute cycle, not an operand any instruction can name.

---
## **Related**

[[Program Counter]] — PC supplies the address, IR receives the word.
[[Control Unit]] — decodes the IR contents into control signals.
[[How does PC system work]] — the fetch half of the cycle this register sits in.
```

### 4. `Memory Address Register.md`（→ `library/M_fold/`）

```markdown
---
aliases:
  - MAR
---

## Definition

Holds the address currently placed on the memory bus: the [[Program Counter|PC]] value during an instruction fetch, the computed effective address during a data access. MAR is a teaching-model register of the von Neumann datapath — x86 has the role but no register name for it, because the address is an operand of the load/store micro-operation rather than of a visible register.

---
## **Related**

[[Memory Data Register]] — the datum that travels with the address.
[[Program Counter]] — the fetcher's source of addresses.
```

### 5. `Memory Data Register.md`（→ `library/M_fold/`）

```markdown
---
aliases:
  - MDR
  - MBR
---

## Definition

Holds the datum in transit between memory and the CPU, so that one memory port can serve both directions and both widths. A fetched instruction passes through MDR into the [[Instruction Register|IR]]; a loaded operand passes through it into a [[General-Purpose Register|GPR]].

---
## **Related**

[[Memory Address Register]] — the address half of the same bus cycle.
[[Instruction Register]] — the destination of an instruction fetch.
```

### 6. `Program Counter.md`（合并到 `library/P_fold/` 那一份）

> 2026-11-13 修订：`IP` 与 `IP (Protocol)` 的别名冲突，寄存器侧改成限定别名 `IP (Instruction Pointer)`，裸 `[[IP]]` 归协议。

```markdown
---
aliases:
  - PC
  - Instruction Pointer
  - IP (Instruction Pointer)
---

## Definition

Holds the address of the next instruction. Every fetch advances it by the length of the instruction just read, so a branch is simply a write to it. Intel calls it `IP`/`EIP`/`RIP`; x86-64 also reads it as an operand base, which is how `RIP`-relative addressing makes its own code position visible.

---
## **Related**

[[Instruction Register]] — the register the fetched word lands in.
[[Stack Pointer]] — the other register a `CALL` writes without naming it.
[[How does PC system work]] — the fetch loop PC drives.
[[Raw Index of Computer Systems]] — 登记主干
```

### 7. `Program Status Word.md`（→ `library/P_fold/`）

```markdown
---
aliases:
  - PSW
  - FLAGS
  - EFLAGS
  - RFLAGS
---

## Definition

Holds the [[Arithmetic Logic Unit|ALU]]'s result state and the CPU's control bits in one word. The result state is what conditional jumps read: ZF (result zero), CF (unsigned carry or borrow), SF (sign bit set), OF (signed overflow). The control bit that matters most is IF, the interrupt enable that `CLI`/`STI` clear and set; because a branch depends on it, the word is part of the state a context switch saves.

---
## **Related**

[[Arithmetic Logic Unit]] — produces the flags.
[[Control Unit]] — consumes them for conditional branches.
[[Threads' Registers]] — the PSW as per-thread saved state.
```

### 8. `Floating-Point Register.md`（→ `library/F_fold/`）

```markdown
---
aliases:
---

## Definition

The register class for non-integer operands, in two generations. The x87 stack (`ST0`–`ST7`) is a stack: every operation pushes or pops, and there is no random access by operand. The SSE/AVX registers (`XMM0`–`XMM15`, `YMM`, `ZMM`) are flat, and the three names are views of one register file at 128, 256 and 512 bits. `XMM0` is also the SysV channel for a float argument and for a float return value.

---
## **Related**

[[Floating-Point Unit]] — the unit that computes on them.
[[General-Purpose Register]] — the integer counterpart, and where addresses live.
[[Floating-Point Number IEEE 754]] — the encoding these registers hold.
```

### 9. `library/S_fold/Stack Pointer.md`（正文补写，登记行保留）

```markdown
## Definition

Holds the address of the top of the stack. On x86 the stack grows toward lower addresses, and `PUSH`, `POP`, `CALL` and `RET` change the pointer implicitly, so a frame is addressed as an offset from it rather than from an absolute address. The ABI does not treat RSP as a general register: a function must leave it exactly as it found it, which is what makes `RET` able to find the return address.

---
## **Related**

[[Register]] — the class it belongs to and the exception to its "general".
[[Program Counter]] — the other register a `CALL` writes without naming it.
[[Kernel Stack]] — the stack a syscall switches the pointer to.
[[Raw Index of Computer Systems]] — 登记主干
```

### 10. `library/R_fold/Register.md`（正文补写，登记行保留）

```markdown
## Definition

A small named storage cell inside the CPU, addressed by the instruction encoding instead of by a memory address. It is the near end of the storage hierarchy: no address translation, no cache lookup, and the only storage whose names appear in the instruction itself. Widths nest — AL and AH are halves of AX, which is the low half of EAX, which is the low half of RAX — so one physical register answers to several names.

---
## **Related**

[[Storage Hierarchy as Distance]] — registers as the nearest, smallest level.
[[Links of Registers]] — the individual registers and the jobs pinned on them.
[[General-Purpose Register]] — the class whose encoding reserves nothing.
[[Raw Index of Computer Systems]] — 登记主干
```

### 11. `Control Register.md`（新，→ `library/C_fold/`）

```markdown
---
aliases:
  - CR0
  - CR2
  - CR3
  - CR4
---

## Definition

Privileged registers that configure the CPU rather than hold computation state; only ring 0 can read or write them.

- `CR0` — processor mode: PE (bit 0) enters protected mode, PG (bit 31) turns paging on, WP (bit 16) makes the kernel respect read-only pages.
- `CR2` — the linear address that caused the last page fault; the fault handler reads it instead of decoding the faulting instruction.
- `CR3` — the physical base of the top-level page table (PML4 on x86-64). Writing it is what a process switch means: new address space, TLB flushed unless PCID tags the entries.
- `CR4` — feature switches: PAE, SMEP and SMAP (kernel may not execute or read user pages), OSXSAVE (AVX state).

---
## **Related**

[[Page Table]] — the structure CR3 points at the root of.
[[Kernel Mode]] — the only mode allowed to touch them.
[[Segment Register]] — the other privileged-base register, kept for TLS.
```

### 12. `Segment Register.md`（新，→ `library/S_fold/`）

```markdown
---
aliases:
  - CS
  - DS
  - SS
  - ES
  - FS
  - GS
---

## Definition

Holds a segment selector, which in 16-bit code supplied a base address for every memory access. In 32- and 64-bit flat mode the code and data bases are zero, so CS, DS, SS and ES stop mattering — but FS and GS keep a base the OS sets, and that base is the one thing every thread and every CPU core needs to find without an argument:

- Linux x86-64: FS holds the thread's TLS pointer (`arch_prctl`), which is why the stack canary is `fs:[0x28]`; in kernel mode GS holds the per-CPU block, so the current task is found without a register argument.
- Windows: FS on 32-bit and GS on 64-bit point at the TEB, from which the PEB is reached — the first thing shellcode and anti-debug code resolve.

---
## **Related**

[[Threads' Registers]] — the TLS block the FS base points at is per thread.
[[Control Register]] — the other register that holds a privileged base.
[[Kernel Mode]] — where the GS base is swapped to per-CPU state.
```

### 13.（可选）`Link Register.md`、`Zero Register.md`

只在 owner 勾选时新建，各一句话，作为 Distinctions 里「其他 ISA」那一行的落点：

- **Link Register**：ARM 的 x30，`BL` 把返回地址写进它而不是压栈；x86 的 `CALL` 只压栈。
- **Zero Register**：RISC-V 的 x0，读恒为 0、写被丢弃；x86 没有恒零寄存器，清零必须占一条指令。

## 四、结构动作（登记边是结构动作，AI 可直接做；移动/新建/删除按本方案逐条批准）

1. **登记**：在 `library/Raw/Raw Index of Computer Systems.md` 追加登记边 —— `General-Purpose Register`、`Instruction Register`、`Memory Address Register`、`Memory Data Register`、`Program Status Word`、`Floating-Point Register`、`Control Register`、`Segment Register`、`Links of Registers`。（`Register`、`Stack Pointer`、`Program Counter` 已有边，不重复追加，避免 I1b。）
2. **重名合并**：把根队列 `Program Counter.md` 的别名并入 `library/P_fold/Program Counter.md`，删除根队列那份 → `[[Program Counter]]` 唯一解析。
3. **出队**：本集群 9 篇移入 fold（`Links of Registers`、`Links of Word Size & Register Bit Width` → `library/Links/`，其余按名字归 fold），用 `git mv`，链接不会断。
4. **新建**：`python3 tools/vault.py new "Control Register" --zone library --apply`，`"Segment Register"` 同（可选再加两篇 ARM/RISC-V）。

## 五、不做的事

- 不给 `Index of Computer Organization` 加挂点（`Index → Node` 要逐条批准，并且它现在是空骨架，I7/I8 会先报）。因此本卡在 I2 里仍是「无区域（提示）」，不是违规。
- 不写任何数学符号与结论；本文里的数字（bit 0/31/16、`fs:0x28`）是 ISA 事实，不是推导。
- 不动 `.obsidian/`、`zzz_output/`、`doctrine/`、`tools/`，不 commit。

## 六、验收

```bash
python3 tools/vault.py check        # G1 里本集群 9 篇消失；G3 不新增悬空链接
python3 tools/vault.py place "Links of Registers"   # 登记边出现、入链不再为 0
python3 tools/vault.py place "Program Counter"      # 不再报同名
python3 tools/vault.py triage       # 本集群不再出现在 root/unhooked
```
