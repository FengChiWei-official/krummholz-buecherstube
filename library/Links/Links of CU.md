---
aliases:
---

## Definition

[[Control Unit|CU]] 的两种实现，按控制向量怎么产生而分：

- **Hardwired** — the control vector is computed by gates or a PLA from the instruction encoding and the flags. Common on [[RISC]].
- **Microprogrammed** — the control vector is *stored*: one [[Microinstruction|microinstruction]] is the control word for one beat, held in a [[Control Store|control store]] (CM). Common on [[CISC]].

"Common on" is a tendency, not a law: x86 is microprogrammed from the 8086 on, early RISC was pure hardwiring, and exceptions run both ways. What the two share is the input surface: the ISA. An instruction is an [[Operation Code|operation code]] plus address fields (and the addressing mode that says how to read them). The CU's other inputs are the flags (for branches) and interrupt requests; the clock decides **when** the transition is evaluated, not **what** it is. Its output is not one signal but a **sequence of control signals**, one per beat: instruction in, control vectors out.

### [[Operation Code|Operation code]]

- **Fixed-length** — the field sits at a fixed position; decoding is a mask over a known slice, and the encoding space is spent uniformly.
- **[[Expanding Opcode|Expanding (variable-length)]]** — short codes for the common instructions, longer codes for the rare ones. The one rule that keeps it decodable: **no short code may be a prefix of a longer one**. This is the scheme the exam asks for.

### [[Microinstruction|Microinstruction]] format

Horizontal and vertical describe the **microinstruction**, not the opcode and not the instruction layout:

- **[[Horizontal Microinstruction|Horizontal]]** — one microinstruction carries many [[Microcommand|micro-commands]] that fire in parallel. Long word, high parallelism, short [[Microprogram|microprogram]].
- **[[Vertical Microinstruction|Vertical]]** — one microinstruction carries one [[Microcommand|micro-command]], or very few; its control field is a short opcode that a decoder turns into one command. Short word, no parallelism, long microprogram; it looks like an ordinary instruction.

### Encoding of the horizontal control field

| Scheme | How | Cost |
|---|---|---|
| [[Direct Encoding]] (direct control) | one micro-command per bit, no decoder; several bits may be set at once (multi-hot) | longest word, fastest |
| [[Field-direct Encoding]] | mutually exclusive micro-commands share a field; a decoder on that field emits one of them | shorter word, one decoder level of delay |
| [[Field-indirect Encoding]] | a field's meaning is read from another field (second-level decoding) | shortest, more delay, rarely used |

What decides who may share a field: **only mutually exclusive micro-commands can be packed together**. Compatible ones must stay apart, or they cannot fire in the same beat.

## Perspectives

**[[Microprogram|Microprogramming]] is control-as-data made hardware**: the control word sits in [[Control Store|memory]], is fetched by an address, and travels on a bus like any datum. A microprogrammed CU is a small von Neumann machine steering a large one.

**Why the split tracks RISC/CISC**: a microprogrammed CU wins when instructions are many and irregular — pay once for the control store, then write microcode. A hardwired CU wins when instructions are few and regular — the control is a small PLA, and a control-store read would only add a level to the critical path.

**The price of microprogramming is a memory access in the control path**: every beat starts by reading the [[Control Store|CM]], so CM must keep up with the clock; a word wide enough to hold all the parallel micro-commands is what makes that memory expensive.

**[[Pipeline|Pipelining]] cuts both halves, not just the datapath**: the datapath is cut into stages by registers, and the control is cut with it — each stage carries its own slice of the control vector forward alongside its data, and the control side grows hazard detection and flush. That is why a pipeline register is always wider than the data it carries.

## Distinctions

- **[[Microcommand|Micro-command]] ≠ [[Microoperation|micro-operation]]**: the command is a signal; the operation is what gets done. One micro-operation may need several micro-commands.
- **[[Microinstruction|Microinstruction]] ≠ machine instruction**: one machine instruction is a [[Microprogram|microprogram]] of many microinstructions. The layers are control-stored-as-data, not two instruction sets on one level.
- **Horizontal/vertical describe the microinstruction, not the opcode**: the opcode is fixed vs expanding; the microinstruction is horizontal vs vertical. Mixing the two is the usual error.
- **[[Direct Encoding|Direct encoding]] ≠ [[Field-direct Encoding|field-direct]]**: direct spends one bit per command and needs no decoder; field-direct compresses mutually exclusive commands and pays a decoder.
- **[[Field-direct Encoding|Field-direct]] vs [[Field-indirect Encoding|field-indirect]]**: the first decodes inside one field; the second needs another field to say what this field means.

## Examples

- [[Horizontal Microinstruction|Horizontal]], [[Field-direct Encoding|field-direct]], `add` in one microinstruction: field A = ALU op (3 bits, one of 8), field B = source select (2 bits), field C = write enable (1 bit) — six bits, one beat.
- [[Vertical Microinstruction|Vertical]]: the same `add` needs one microinstruction for the ALU op and another for the write-back; short word, long microprogram.
- x86 from the 8086 on is microprogrammed; MIPS is hardwired — the two anchors the exam uses.

---
## **Related**

[[Control Unit]] — the unit being classified.
[[Control and Payload]] — the criterion that separates control from data.
[[控制即数据]] — why the microprogrammed case is a machine inside the machine.
[[Datapath]] — what the sequence of control signals drives.
[[Pipeline]] — where the control is cut alongside the datapath, stage by stage.
