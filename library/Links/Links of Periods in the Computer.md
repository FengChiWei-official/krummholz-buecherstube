---
aliases:
---

## Definition

Three nested time units, each answering a different question:

| 单位 | 回答 | 由谁定 |
|---|---|---|
| [[Instruction Cycle]] | 一条指令多久完成 | ISA —— 这条指令需要几次基本操作 |
| [[Machine Cycle]] | 一次基本操作（一次访存 / 一次总线事务）多久 | 微架构 —— 总线与时序 |
| [[Clock Cycle]] | 状态多久更新一次 | 组合路径延迟 |

A historical concept, in old time, there is a hierarchical structure: [[Instruction Cycle]] - [[Machine Cycle]]-[[Clock Pulse]]

$$T_{\text{指令}} = k \cdot T_{\text{机器}} = k \cdot m \cdot T_{\text{时钟}}$$

## Perspectives

**嵌套 = 把下一层数几次。** 拍数不是物理常数，是两个整数：这条指令需要几次基本操作（$k$），这次基本操作需要几拍（$m$）。所以“多周期”不是机器的属性，是 $(k, m)$ 这一对值。

**为什么单位是访存。** 访存是必须串行化的那件事：地址先出去，数据才回来。单总线机器上机器周期因此恰好等于总线周期，这也是这个词当年能当单位用的原因。

## Distinctions

- **machine cycle ≠ instruction cycle**：大量英文资料把 fetch–decode–execute 叫 “a machine cycle”，那是指令周期，高一层。跨语料查这个词必须先看层级。
- **machine cycle ≠ clock cycle**：一个机器周期含多个时钟周期；它存在的作用就是让“多周期”可数而不必点节拍。
- **定长 vs 变长**：定长取最慢基本操作，控制简单、浪费拍数；变长按操作给长度，快、控制复杂。
- **指令周期不是常数**：间址、中断各多一个机器周期，同一条指令在不同寻址方式下 $k$ 不同。

## Examples

- 主频 1 GHz（$T_{\text{时钟}}=1\,\text{ns}$），每机器周期 4 拍，某指令 3 个机器周期 → 指令周期 12 ns。
- Intel 8080：`MOV A,B` = 1 个机器周期（4 T），`MOV A,M` = 2 个机器周期（7 T）；`M1` 取操作码。

---
## **Related**

[[Machine Cycle]] — 中间那层，也是唯一已死的一层。
[[Instruction Cycle]] — 最外层；$k$ 由它定。
[[Clock Cycle]] — 最内层；$m$ 由它定。
[[Clock Beat]] — 历史上机器周期与脉冲之间的那层，死得最彻底。
[[CPU as a State Machine]] — 节拍是状态更新的边界，这三个单位就是它的刻度。
