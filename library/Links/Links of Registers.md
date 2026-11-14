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
- [[Stack Pointer|SP · ESP · RSP]] — the top of the stack; `PUSH`/`POP`/`CALL`/`RET` move it implicitly.
- [[Program Status Word|PSW · FLAGS · EFLAGS · RFLAGS]] — the ALU's result state; what conditional jumps read.
- [[Floating-Point Register|ST0–ST7 · XMM · YMM · ZMM]] — non-integer operands; `XMM0` carries a float argument and the return value.
- [[Control Register|CR0–CR4]] — privileged mode and paging switches; `CR3` is the page-table root.
- [[Segment Register|CS · DS · SS · ES · FS · GS]] — flat on x86-64 except FS and GS, which keep the TLS and per-CPU base.

## Perspectives

**One register file, four jobs**: carry data (GPR, XMM), carry addresses (PC, MAR, SP), carry state (PSW), carry mode (CR, segment base).

**Named by role, not by operand**: `MUL`/`DIV` read RAX and RDX implicitly, `REP` reads RCX, `SHL` reads CL, `syscall` reads RAX, `MOVS`/`STOS` read RSI and RDI. The instruction names the operation, not the operand.

**The ABI is a second, softer hardwiring**: RDI, RSI, RDX, RCX, R8, R9 are the first arguments in order, RAX the return value, RBX/RBP/R12–R15 callee-saved, RSP the stack. The same registers, with roles fixed by convention instead of by circuit.

**Visibility is a third axis**: GPR, PC and PSW are readable in user mode, CR only at CPL0, and the FS/GS base is swapped per thread (Linux `arch_prctl`) or per CPU (kernel `swapgs`) — which is why it is the cheapest pointer to thread-local and CPU-local state.

**Width is a historical stack, not a design**: AL/AH ⊂ AX ⊂ EAX ⊂ RAX is one register under nesting names, so 8/16/32/64-bit code shares one naming scheme — see [[Links of Word Size & Register Bit Width]].

## Distinctions

- **Register vs memory**: no address, no cache line, no bus; that is why [[Register]] is the general idea and this card is the individual jobs.
- **Architected vs internal**: RIP is the architected program counter; rename registers, reorder buffers and reservation stations are the microarchitecture's own storage and have no name in the ISA.
- **PC vs IP**: the same register — `Program Counter` in architecture texts, `Instruction Pointer` in Intel's `IP`/`EIP`/`RIP`; x86-64 also exposes it as an addressing base, which is what `RIP`-relative operands use. In this vault bare `[[IP]]` is [[IP (Protocol)|Internet Protocol]], so the register carries the qualified alias `IP (Instruction Pointer)`.
- **PSW vs FLAGS**: PSW is the whole word including system bits (IOPL, VM, AC); FLAGS names the condition-code subset that arithmetic writes and jumps read.
- **Register class vs a thread's registers**: [[Threads' Registers]] is the same register set seen as the saved context of a context switch.
- **Other ISAs**: ARM's LR (x30) holds the return address instead of pushing it; RISC-V's x0 reads as zero and ignores writes. x86 has neither — every x86 register is mutable state.

## Examples

- `mov rax, qword ptr fs:[0x28]` — read the stack canary from the TLS block at function entry (Linux x86-64).
- `mov cr3, rax` — switch address spaces: new page-table root, TLB flushed unless PCID tags the entries.
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
