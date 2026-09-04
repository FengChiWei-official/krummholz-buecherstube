# x86 汇编阅读理解教程 (考试/应试方向)

## 目标

**不是学会手写汇编，而是学会「看到一段汇编能翻译回 C/逻辑」**。这是期末考试、考研、校招笔试里真正考的能力。

---

## 一、地基：历史与字长概念

### 1.1 Intel 的三次扩展

| CPU | 年份 | 寄存器宽度 | 命名 | 汇编里的 word 定义 |
|-----|------|-----------|------|-------------------|
| **8086** | 1978 | **16 位** | `ax, bx, cx, dx, si, di, sp, bp, ip` | **word = 16 位 (当时就是机器字长)** |
| 80386 | 1985 | **32 位** | `eax, ebx, ecx, edx, esi, edi, esp, ebp, eip` | **dword = 32 位** (word 不动，叠 dword) |
| x86-64 | 2003 | **64 位** | `rax, rbx, rcx, rdx, rsi, rdi, rsp, rbp, rip` | **qword = 64 位** (再叠 qword) |

**你只需要记住这一条规则：**

| 汇编术语 | 位宽 |
|---------|------|
| `byte` | 8 |
| `word` | **16** (8086 的原始字长，永久固定) |
| `dword` | **32** (double word) |
| `qword` | **64** (quad word) |

> `word` 不等于你当前 CPU 的机器字长。它是历史残留定义，考试只考它等于 **16 位**。

### 1.2 当前你用的 x86-64 的真实情况

- **机器字长** = 64 位 (你的 Ryzen 7 5800H 是 64 位 CPU)
- **寄存器** = 64 位 (rax, rbx, ...)
- **地址** = 64 位虚拟地址 (当前只用了低 48 位，但考试一般不深究)
- **但编译器在很多场景下仍选择 32 位操作数**（因为 `mov eax, 0` 比 `mov rax, 0` 短，且隐式清零高32位——这是 x86-64 的特性）

---

## 二、寄存器模型 (必须背下来)

### 2.1 通用寄存器 (x86-64)

```
64位     32位     16位     8位(低)   8位(高)
──────────────────────────────────────────────
rax      eax      ax       al        ah
rbx      ebx      bx       bl        bh
rcx      ecx      cx       cl        ch
rdx      edx      dx       dl        dh
rsi      esi      si       sil       —
rdi      edi      di       dil       —
rbp      ebp      bp       bpl       —
rsp      esp      sp       spl       —
r8       r8d      r8w      r8b       —
r9       r9d      r9w      r9b       —
...往下到 r15
```

**考试重点：**

- **rax (eax)** — 累加器，**函数返回值**存放处
- **rcx (ecx)** — 计数器 (循环计数、移位位数)
- **rdx (edx)** — 乘法/除法扩展，函数第 3 个参数 (x86-64)
- **rsi (esi)** — 源索引 (串操作、memcpy 的源)
- **rdi (edi)** — 目标索引 (串操作的目的)
- **rsp (esp)** — 栈指针 (永远指向栈顶)
- **rbp (ebp)** — 栈帧基址 (函数局部变量基地址)
- **rip (eip)** — 指令指针 (存当前正在执行的指令地址，**不能直接读写**)

### 2.2 标志寄存器 (rflags / eflags)

只记几个关键位：

| 标志 | 名字 | 含义 |
|------|------|------|
| **ZF** | Zero Flag | 上一条运算结果 == 0 |
| **SF** | Sign Flag | 上一条运算结果为负 (最高位为 1) |
| **CF** | Carry Flag | 无符号溢出 (加法进位/减法借位) |
| **OF** | Overflow Flag | 有符号溢出 |

```
cmp a, b       → 计算 a - b，设 ZF / SF / CF / OF
je label       → if (ZF == 1)  goto    (相等跳)
jne label      → if (ZF == 0)  goto    (不等跳)
jg label       → if (SF == OF && ZF == 0) goto   (有符号大于)
jge label      → if (SF == OF) goto            (有符号大于等于)
jl label       → if (SF != OF) goto            (有符号小于)
jle label      → if (SF != OF || ZF == 1) goto (有符号小于等于)
ja label       → if (CF == 0 && ZF == 0) goto  (无符号大于)
jb label       → if (CF == 1) goto             (无符号小于)
```

**记忆口诀**：`j` + `e`(qual) / `g`(reater) / `l`(ess) / `a`(bove) / `b`(elow)。有符号用 g/l，无符号用 a/b。

---

## 三、指令集 (覆盖考试 95%)

### 3.1 数据传送

```
mov  dst, src           ; dst = src
push src                ; 压栈: rsp -= 8; *rsp = src
pop  dst                ; 出栈: dst = *rsp; rsp += 8
xchg a, b               ; 交换 a 和 b 的值
lea  reg, [address]     ; reg = &address (只算地址，不访存)
```

**考试陷阱：** `mov` 的两个操作数不能同时是内存地址。必须 `mov eax, [addr]` 再 `mov [addr2], eax`。

### 3.2 算术运算

```
add  dst, src    ; dst += src
sub  dst, src    ; dst -= src
inc  dst         ; dst++
dec  dst         ; dst--
neg  dst         ; dst = -dst
imul dst, src    ; dst *= src  (有符号乘)
mul  src         ; rdx:rax = rax * src  (无符号乘，结果 128 位放 rdx|rax)
idiv src         ; rax = rdx:rax / src, rdx = 余数 (有符号除)
div  src         ; 同上，无符号
```

**特别记 `idiv`/`div`**：被除数隐含是 `rdx:rax`（即 128 位的拼接），所以除法前要先扩展。

```
cdq              ; 把 eax 的符号位扩展到 edx (32位版)
cqo              ; 把 rax 的符号位扩展到 rdx (64位版)
; 典型用法：
;   mov    eax, dividend
;   cdq
;   idiv   divisor       ; eax = 商, edx = 余数
```

### 3.3 逻辑/移位

```
and  dst, src    ; dst &= src
or   dst, src    ; dst |= src
xor  dst, src    ; dst ^= src
not  dst         ; dst = ~dst
test a, b        ; a & b (只设标志，不写结果)
shl  dst, cnt    ; dst <<= cnt   (逻辑左移)
shr  dst, cnt    ; dst >>= cnt   (逻辑右移)
sar  dst, cnt    ; dst >>= cnt   (算术右移，符号位扩展)
```

**高频模式：** `xor eax, eax` → 把 eax 清零。比 `mov eax, 0` 短一个字节。

### 3.4 控制流

```
cmp  a, b        ; a - b，设标志位
jmp  label       ; 无条件跳转
je/jz            ; 相等跳转 (ZF=1)
jne/jnz          ; 不相等跳转 (ZF=0)
jg/jge/jl/jle    ; 有符号比较跳转
ja/jae/jb/jbe    ; 无符号比较跳转
call func        ; 函数调用：push 返回地址; jmp func
ret              ; 返回：pop 返回地址 → rip
```

### 3.5 循环指令 (考试常考)

```
loop label      ; ecx--; if (ecx != 0) goto label
loope label     ; ecx--; if (ecx != 0 && ZF==1) goto
loopne label    ; ecx--; if (ecx != 0 && ZF==0) goto
```

注意：现代编译器生成的循环通常不用 `loop`，而是展开成 `cmp + jge/jl + jmp`。但考试(尤其是8086/80386试题)里 **loop 高频出现**。

### 3.6 串操作 (考 DMA/memcpy 类题目)

```
movsb            ; 从 [rsi] 复制 1 字节到 [rdi]，rsi++/rdi++
movsw            ; 2 字节
movsd            ; 4 字节 (32位下常见)
movsq            ; 8 字节 (64位)
cld              ; 清方向标志 (DF=0 → rsi/rdi 递增)
std              ; 置方向标志 (DF=1 → 递减)
rep              ; 前缀：重复执行后面的串指令 ecx 次
; 典型： rep movsb   → memcpy(rdi, rsi, ecx)
```

### 3.7 其他零碎

```
nop              ; 空操作 (常用于对齐)
int  0x80        ; 系统调用 (32位时代)
syscall          ; 系统调用 (64位时代)
pushf / popf     ; 压入/弹出 rflags
cbw / cwde      ; 字节→字扩展 / 字→双字扩展
```

---

## 四、内存寻址方式 (考试必考)

x86 寻址公式：

```
[ base + index * scale + displacement ]

base      = 寄存器 (通常是 rbp, rsp, 或通用寄存器)
index     = 寄存器 (通常是 rsi, rdi, 或不用)
scale     = 1, 2, 4, 8 (index 的乘数)
displacement = 立即数偏移

32位等效写法：[ebp + esi*4 + 0x10]
```

### 六种基本方式 (考试分解)

| 模式 | 例子 | 等效 C |
|------|------|--------|
| 寄存器间接 | `[eax]` | `*eax` |
| 基址+偏移 | `[ebp + 8]` | `*(ebp + 8)` |
| 基址+变址 | `[ebp + esi]` | `*(ebp + esi)` |
| 基址+变址*比例 | `[ebp + esi*4]` | `*(ebp + esi*4)` |
| 基址+变址*比例+偏移 | `[ebp + esi*4 + 8]` | `*(ebp + esi*4 + 8)` |
| 直接地址 | `[0x8048000]` | `*(0x8048000)` |

**禁用情况：** scale 不能跟 ebp/eip 相乘，index 不能是 esp。这些是硬件约束，考试填空题可能会考。

### 4.1 特别关注：栈帧上的局部变量寻址

```
push ebp
mov  ebp, esp
sub  esp, 16           ; 分配 16 字节局部变量

; 局部变量访问 (以 32 位为例)
mov  dword ptr [ebp-4], 10    ; 第一个局部变量 (int a = 10)
mov  eax, dword ptr [ebp-4]   ; 读 a

; 函数参数访问
mov  eax, dword ptr [ebp+8]   ; 第一个参数
mov  eax, dword ptr [ebp+12]  ; 第二个参数
```

栈帧布局（32位 cdecl）：

```
        ┌──────────────┐
ebp+12  │  参数2       │
ebp+8   │  参数1       │
ebp+4   │  返回地址    │
ebp     │  旧 ebp      │←── ebp 指向这里
ebp-4   │  局部变量1   │
ebp-8   │  局部变量2   │
        │  ...         │
        └──────────────┘←── esp
```

---

## 五、函数调用约定 (ABI)

### 5.1 32 位 cdecl (默认，考试最常见)

```
参数传递：从右到左压栈
返回值：  eax
调用者清理栈 (caller cleanup)
```

```
; C: int sum(int a, int b, int c);
; 调用：
push  c          ; 第三参数
push  b          ; 第二参数
push  a          ; 第一参数
call  sum
add   esp, 12    ; 调用者平衡栈 (3个参数 × 4字节)
```

### 5.2 32 位 stdcall (Windows API)

```
参数传递：从右到左压栈
返回值：  eax
被调用者清理栈 (利用 ret n 语法)
```

```
; 调用方只要 push 参数，不需要 add esp
push  c
push  b
push  a
call  sum
; 不用 add esp ← sum 内部会 ret 12
```

### 5.3 64 位 System V ABI (Linux, macOS — 你的环境)

```
参数传递：依次放入 rdi, rsi, rdx, rcx, r8, r9，其余压栈
返回值：  eax / rax
被调用者只负责清理自己分配的局部栈 (没有调用者清理的必要，因为参数大多数在寄存器)
```

```
; C: int sum(int a, int b, int c);
; 调用：
mov   edi, a
mov   esi, b
mov   edx, c
call  sum
; 没有 add esp 的事
```

**考试注意：** 很多教材默认讲 32 位 cdecl。如果是 x86-64 的题，题干会说清。如果没说不清，题目通常是 32 位。

---

## 六、从 C 到汇编的模式对照表 (最实用)

| C 构造 | 汇编模式 |
|---------|--------|
| **`a = b`** | `mov eax, [b_addr]; mov [a_addr], eax` |
| **`a + b`** | `mov eax, a; add eax, b` |
| **`return x`** | `mov eax, x; ret` |
| **`if (a == b)`** | `cmp a, b; je .L_then` |
| **`if (a > b)`** | `cmp a, b; jg .L_then` |
| **`while (i < n)`** | 顶部 `cmp i, n; jge .L_end`，底部 `jmp .L_check` |
| **`for (i=0; i<n; i++)`** | `mov i, 0; .L: cmp i,n; jge .L_end; ...; inc i; jmp .L` |
| **`a[i]`** | `mov eax, [array_base + i*4]` (4字节每元素) |
| **`&a[i]`** | `lea eax, [array_base + i*4]` |
| **`struct.field`** | `mov eax, [struct_base + offset_of_field]` |
| **`*p = v`** | `mov [p_reg], v` |
| **`switch`** | 跳转表 `jmp [jmp_table + index*4]` (特征明显) |
| **`memcpy(d,s,n)`** | `rep movsb` (或展开的循环) |
| **`a = 0`** | `xor eax, eax` (编译器优化,比 mov eax,0 短) |
| **`i++`** | `inc i` / `add i, 1` |
| **`if (!a)`** | `test a, a; je .L_then` (或 `cmp a,0; je`) |
| **调用函数** | `call 函数名` |
| **函数..开头** | `push ebp; mov ebp, esp; sub esp, N` |
| **函数..结尾** | `mov esp, ebp; pop ebp; ret` |

---

## 七、实战读汇编的策略

### 7.1 五步读函数法

看到一个汇编函数，按这 5 步走：

```
1. 找开头 → 确定是不是有栈帧 (push ebp; mov ebp, esp)，有的话画栈布局
2. 找返回值 → 函数结束前的 mov eax, xxx
3. 找参数 → 从 [ebp+8] 开始读，或在 64 位下看 rdi/rsi/rdx
4. 找控制流 → 所有 jmp/je/jg/... 构成的分支和循环
5. 还原 C → 按模式表反向翻译
```

### 7.2 示例：逐行翻译

```asm
; 猜这个函数做了什么 (32位 cdecl)
push   ebp
mov    ebp, esp
mov    eax, dword ptr [ebp+8]
mov    edx, dword ptr [ebp+12]
cmp    eax, edx
jle    .L2
mov    eax, dword ptr [ebp+8]
jmp    .L3
.L2:
mov    eax, dword ptr [ebp+12]
.L3:
pop    ebp
ret
```

**翻译方法：**

```
Step 1: 有栈帧 → 画栈布局
         参数2 (edx) ← [ebp+12]
         参数1 (eax) ← [ebp+8]
         返回地址
         旧 ebp   ← ebp

Step 2: 参数1 → eax, 参数2 → edx
Step 3: 比较 eax 和 edx
           if eax <= edx, 跳 .L2
Step 4: .L2 之前：返回 eax  (参数1)
         .L2 处：返回 edx  (参数2)

结论：
  int max(int a, int b) {
      if (a > b) return a;
      else       return b;
  }
```

### 7.3 示例：循环

```asm
; 猜这个函数？
push   ebp
mov    ebp, esp
sub    esp, 8             ; 两个局部变量
mov    dword ptr [ebp-4], 0    ; s = 0
mov    dword ptr [ebp-8], 0    ; i = 0
jmp    .L_check
.L_loop:
mov    eax, dword ptr [ebp-8]
add    dword ptr [ebp-4], eax  ; s += i
add    dword ptr [ebp-8], 1    ; i++
.L_check:
cmp    dword ptr [ebp-8], 10
jl     .L_loop                  ; i < 10 → 继续
mov    eax, dword ptr [ebp-4]   ; return s
mov    esp, ebp
pop    ebp
ret

→ int sum() {
      int s = 0, i = 0;
      while (i < 10) { s += i; i++; }
      return s;
  }
  // (其实是个从 0 加到 9 的求和 = 45)
```

注意：有 `jmp .L_check` 的是 while 结构的「先跳检查，底部循环」模式，编译器惯用。

---

## 八、看汇编的实用工具

### 8.1 Compiler Explorer (godbolt.org)

最快的学习路径：写 C → 秒出汇编，逐行对应。**上机实践比读任何教程都有效。**

### 8.2 本地命令

```bash
# 把你的 C 编译成汇编 (Intel 语法)
gcc -O0 -S -masm=intel foo.c        # 未优化版，容易对
gcc -O2 -S -masm=intel foo.c        # 优化版，更短更难但更真实
objdump -d -M intel foo.o           # 反编译 .o 文件
objdump -d -M intel foo             # 反编译可执行文件
```

### 8.3 考试准备推荐

| 练习内容 | 方法 |
|----------|------|
| 寄存器、指令基础 | 对照第三节列表，每天默写一次（连续 3 天） |
| 寻址方式 | 自己写出 6 种方式的例子（10 分钟） |
| 函数翻译练习 | 在 Godbolt 编译 10 个小函数，不看高亮，自行翻译后核对 |
| 栈帧布局 | 画 10 次栈图（每次参数/局部变量数不同） |
| 真实试卷 | 找近 3 年考研/期末汇编题，按五步法分析 |

---

## 九、常见考试陷阱清单

| 陷阱 | 正解 |
|------|------|
| `word` 等于当前机器字长？ | **错**。等于 16 位，历史定义 |
| `dword` 是 64 位？ | **错**。dword = 32, qword = 64 |
| `mov eax, 0` 和 `xor eax, eax` 哪个更优？ | 后者（机器码更短，但语义都是清 0） |
| `cmp a, b; je` 是 a == b 还是 b == a？ | `cmp` 做 `a - b`，所以是 `a == b` 时跳 |
| `call` 之后下一条指令是什么？ | 返回地址是 `call` 的下一条，`ret` 回到那里 |
| `push` / `pop` 改变哪个寄存器？ | `esp` / `rsp` |
| `lea` 和 `mov` 的区别？ | `lea` 算地址不访存，`mov` 访存 |
| 32位 cdecl 谁清栈？ | 调用者（调用后 `add esp, N`） |
| 32位 stdcall 谁清栈？ | 被调用者（`ret N`） |
| 64位 System V 参数放哪？ | `rdi, rsi, rdx, rcx, r8, r9`，然后压栈 |
| `je` 和 `jz` 的区别？ | 同一条指令的不同别名，`jz` 强调 ZF=1 |
| `div` 不指定被除数？ | 被除数隐含在 `edx:eax`，`div` 前要扩展 |
| 循环用 `loop` 还是 `cmp + jmp`？ | 教材题常用 `loop`，真实代码用 `cmp + jmp` |

---

## 十、最后建议

1. **不背指令表，用模式识别。** 看到 `cmp; jg` → 马上反应是 if 分支。
2. **用 Godbolt 做翻译练习。** 写 C 看汇编，遮住 C 倒推回去。
3. **8053/8086 的题集中在分段寻址、loop、INT、串操作，** 和上面 x86 通用部分稍有不同。如果你的考试考 8086 实模式，需要额外补段寄存器（cs/ds/es/ss）和分段寻址 `[段基址:偏移]` 那一套。告诉我我可以单独补充。
4. **遇到看不懂的汇编——先找跳转标号（分支/循环），再找 `call`（函数调用），剩下的就是赋值和计算。** 你不需要理解每个寄存器的每一次变化，只需要理解函数的行为。