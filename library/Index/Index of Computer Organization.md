# Index of Computer Organization

## 时间轴

| 世代 | 年份 | 代表 | 这一代解决了什么 |
|---|---|---|---|
| 16 位 | 1978 | 8086 | 寄存器与 ALU 定在 16 位；段:偏移用 16 位寄存器给出 20 位地址（1 MiB）——字长与地址宽第一次分道 |
| 32 位 | 1985 | 80386 | 平坦 32 位 + 分页：段基址退化为 0，地址宽追平寄存器宽，虚存交给 MMU |
| 64 位 | 2003 | AMD64 | 寄存器扩到 64 位，新增 R8–R15 与 REX 前缀；地址只到 48 位规范地址——两种宽度再次分开 |
| 向量 | 1999–2017 | SSE → AVX-512 | 寄存器宽度脱离机器字：128/256/512 位的 XMM/YMM/ZMM 与 x87 的 80 位并存 |

## 地图

| 挂点 | 合同 / 部件 | 回答的张力 |
|---|---|---|
| [[Program Counter]] | 下一条指令的地址 | 控制流为何只是一次写 |
| [[Instruction Register]] | 当前指令字 | 译码器读的是谁 |
| [[Control Unit]] | 指令 → 控制信号 | 这一拍让哪条线动作 |
| [[How does PC system work]] | 取指–译码–执行 | 一条指令怎么穿过这些部件 |
| [[Arithmetic Logic Unit]] | 模 2^n 的加法器 + 选择 | 算术为何能归约成加法与移位 |
| [[Datapath]] | 寄存器堆 + ALU + 内部总线 | 操作数在哪里相遇 |
| [[Floating-Point Unit]] | 独立的浮点通路 | 浮点为何要另一套电路 |
| [[Register]] | CPU 内的存储格 | 存储分层的最内层为何不需要地址 |
| [[General-Purpose Register]] | 编码可寻址的 16 个格 | “通用”为何仍被指令与 ABI 钉死 |
| [[Stack Pointer]] | 栈顶指针 | 函数调用为何只是指针移动 |
| [[Program Status Word]] | 条件码 + 控制位 | 分支如何知道上一条指令的结果 |
| [[Floating-Point Register]] | x87 栈 / SIMD 平铺 | 非整数操作数放在哪 |
| [[Control Register]] | CR0–CR4 | 内核如何切换地址空间与特性 |
| [[Segment Register]] | FS/GS 基址 | 线程与 CPU 局部数据怎么被找到 |
| [[Threads' Registers]] | 一次切换要保存的寄存器集合 | 进程换下时到底保存什么 |
| [[Memory Address Register]] | 地址总线一侧 | 访存地址从哪来 |
| [[Memory Data Register]] | 数据总线一侧 | 一次访存搬多少位 |
| [[Storage Hierarchy as Distance]] | 层级 | 寄存器为何最快 |
| [[Physical Address as Global Identity]] | 物理地址 | 为何只有物理地址是全局身份 |
| [[Two's Complement]] | 有符号截面 | 同一串位如何表示负数 |
| [[Unsigned Integer]] | 无符号读法 | 位串的另一种解释 |
| [[Floating-Point Number IEEE 754]] | 指数 + 尾数 | 用范围换精度 |
| [[运算归约为加法与移位]] | 不变量 | 为什么所有算术都落到加法器 |
| [[快慢互联的统一解]] | 不变量 | 速度差如何被层次吸收 |
| [[控制即数据]] | 不变量 | 指令为何能与数据同存 |
| [[透明性即维护假象]] | 不变量 | 抽象为何要维护假象 |
| [[表示先于电路]] | 不变量 | 为何先定表示再谈电路 |
| [[时空互换]] | 不变量 | 何时用空间换时间 |
| [[CPU as a State Machine]] | 状态机 | 寄存器是状态，PC 与 PSW 是转移函数的输入 |
| [[Hardware]] | 硬件层 | 与 OS 的边界画在哪 |

## 卡片

[[Links of Registers]] — 每个寄存器被谁钉死：指令的隐式操作数与 ABI。
[[Links of Word Size & Register Bit Width]] — 字长、位宽、地址宽为何是三件事。
[[Links of ALU]] — ALU 的代数结构：商群与截面。
[[Links of Data Representation in Computer]] — 一台机器上共有几种读法。
[[Links of IEEE754]] — IEEE754 的边界情形。
