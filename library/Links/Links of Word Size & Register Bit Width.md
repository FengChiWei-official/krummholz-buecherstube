---
aliases:
---

## Definition

Four "widths" that Chinese textbooks all call 宽 or 长 measure four different things:

- **Word** — the unit assembly language counts in. It is not a measurement but a vocabulary the ISA picks: Intel fixed BYTE = 8, WORD = 16, DWORD = 32, QWORD = 64 at the 8086 and never moved it, so `WORD PTR` still means 2 bytes on a 64-bit register.
- **Machine word size** — how many bits one integer operation handles, i.e. the width of the datapath, of the [[Arithmetic Logic Unit|ALU]], and of a [[General-Purpose Register|GPR]]. It is 64 on x86-64 and fixes the integer range (mod 2^64) and the largest alignment.
- **Address width** — how many bits of an address are meaningful. The pointer register is 64 bits on x86-64, but 4-level paging uses 48 (57 with 5 levels) and the upper bits must repeat bit 47 (canonical addresses) — so "64-bit register" does not mean "2^64 address space". What it constrains is the registers that hold addresses: [[Program Counter|PC]], [[Stack Pointer|SP]], [[Memory Address Register|MAR]].
- **Storage word length** — how many bits one memory read or write moves, i.e. the data bus (one row of the memory array); [[Memory Data Register|MDR]] is its model register. It is not the addressing granularity: x86 addresses bytes, one `mov` moves 1, 2, 4, 8 or 16 bytes, and one cache-line fill is 64 bytes.

A width constraint does not follow from "the machine is 64-bit"; it follows from **what the register means**. The same 64-bit physical cell gets a different constraint per semantic role:

| Semantic role | Typical member | Width set by | Constraint |
|---|---|---|---|
| Integer / data | [[General-Purpose Register]] | machine word size | width = ALU width; arithmetic closed mod 2^n |
| Address / pointer | [[Program Counter]], [[Stack Pointer]], [[Memory Address Register]] | address width | width ≥ address width; if wider, the high bits are a canonical extension |
| Physical address | [[Control Register]] (CR3) | physical address width | holds a page-table base; unrelated to the virtual address width |
| Linear address | [[Control Register]] (CR2) | address width | the faulting virtual address, written by hardware |
| Segment base | [[Segment Register]] | two widths at once | visible selector is 16 bits (historical); the hidden descriptor base is address width |
| Instruction | [[Instruction Register]] | longest instruction encoding | x86 allows 15 bytes, so IR is a buffer — not one word and not one machine word |
| State / control bits | [[Program Status Word]] | bits the ISA defines | each bit has its own meaning; no integer arithmetic, no "word size" |
| Float / vector | [[Floating-Point Register]] | format width × element count | chosen by the instruction's format, independent of the machine word |

## Perspectives

**"Word" is vocabulary; "word size" is measurement**: Intel's naming table froze in the 16-bit era while the textbook's machine word size follows the implementation. So on one machine "a word is 16 bits" and "the word size is 64" are both true — one describes the assembler's vocabulary, the other the datapath.

**Address width need not equal machine word size, and both directions occur**: the 8086 had 16-bit registers and 20-bit addresses (segment × 16 + offset), widening the address through segmentation; x86-64 has 64-bit registers and 48-bit effective addresses, the register wider than the address, the surplus bits a sign extension. A pointer therefore fills a whole machine word (`sizeof(void*) == 8`) — not waste, since a C address type must hold the address width and the machine word is the only unit moved as one piece.

**Storage word length sets the number of memory cycles, not the width of a type**: 32-bit registers on a 32-bit data bus move 4 bytes per access; the 8088 put its 16-bit registers on an 8-bit bus, so one word took two bus cycles. Storage word length is a throughput property, machine word size an arithmetic one; equality is a common design, not a law.

**The constraint belongs to the semantics; the register is only the container**: the same RAX as an integer obeys "= machine word size", as a pointer "≥ address width", and as a return value also the ABI's width rule (a narrow return value defines only the low bits). That is why memorising "64-bit" is not enough — the question is what this register stands for at this moment.

**Instruction length is a fourth width**: x86 is variable (1–15 bytes), RISC-V is fixed at 32. It sets the width of IR and of the fetch buffer, and the PC's step (+1 byte vs +4 bytes), with no relation to the machine word.

## Distinctions

- **Machine word size vs storage word length**: the first bounds the arithmetic range (mod 2^n), the second the bits per transfer (and therefore cycles per access). On the 8088 they are 16 and 8.
- **Address width vs register width**: x86-64 holds a 48-bit address in a 64-bit register, upper bits repeating bit 47; a non-canonical address raises #GP, so "it fits" is not "it is valid".
- **Physical vs virtual address width**: CR3 holds the page-table base as a physical address, CR2 the faulting linear address — one encoding style, one register group, two different width constraints.
- **Word vs byte**: a word is not addressable. x86 addresses bytes; `WORD PTR` / `DWORD PTR` only annotate operand size, the address stays a byte address.
- **Width vs numeric range**: the width fixes the modulus, signedness only picks a section (see [[Two's Complement]]); making a register wider does not make a number signed.
- **Fixed vs variable instruction length**: a fixed-length ISA can let IR equal one instruction; x86 must size IR for 15 bytes and still handle fetch across a boundary.

## Examples

- 8086 `mov ax, [bx+si]`: the operand is 16 bits (machine word size), the physical address 20 bits (segment base × 16 + offset) — two widths in one line of assembly.
- On x86-64 the same `mov eax, [rdi]` is a 4-byte access, `movzx eax, byte ptr [rdi]` a 1-byte one, `movdqu` 16 bytes — the storage word is a 64-byte cache line, but the operand width is chosen by the instruction.
- `mov cr3, rax` writes a physical address; `mov rax, cr2` reads a linear one: same register encoding, different constrained width.
- x87's 80-bit register and YMM's 256 bits: one instruction handles four doubles, so the register width is format width × element count, unrelated to the 64-bit machine word.

---
## **Related**

[[Links of Registers]] — the roles pinned on each register; this card explains where their widths come from.
[[Register]] — the storage cell itself; its bit width is its capacity.
[[Program Counter]] — where address width becomes tangible.
[[Two's Complement]] — what a fixed width does to arithmetic.
[[Arithmetic Logic Unit]] — the unit whose width is the machine word size.
[[Links of Data Representation in Computer]] — the readings a bit pattern can be given.
