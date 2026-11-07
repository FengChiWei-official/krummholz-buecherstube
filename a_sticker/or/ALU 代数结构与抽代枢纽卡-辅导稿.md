# ALU 代数结构与抽代枢纽卡 — 辅导稿

> 暂存稿（`a_sticker/or/`）。用途：把「从补码 → ALU 代数结构 → 抽代卡」这条线的结论固化，供逐卡补写时引用。
> 状态：**只讲不写** —— 卡片正文由 owner 落笔，本稿只提供讲解、骨架、已验证事实。

---

## 一、计划与顺序（枢纽优先）

| 序 | 卡 | 现状 | 为什么排这个位置 |
|---|---|---|---|
| 1 | [[Quotient Group]] | 只有记号 $G/H$ | 枢纽：机器数就是商群；缺它整条链（陪集→正规→商→核→同构定理）断 |
| 2 | [[Generator of Cyclic Group]] | 空 | 回答「生成元为什么 128 个」：$\gcd(k,m)=1$ + $\phi$ |
| 3 | [[Difference between Order of Group and Cyclic Group]] | 空 | 区分「群的阶（元素个数）」与「元素的阶（几步回原处）」 |
| 4 | [[Correspondence Theorem]] | 空 | 子群 ↔ 商群子群；对应滤链/位 |
| 5 | [[抽象代数 Todo]] 那批定义型 | 空 | Algebraic Structures / Closure / Law of Associative / Element / Bijective Functions / Cancellation Law / Characterization / Domain of Value / Class |
| — | [[Functor]] | 空 | **建议单列**：范畴论，不在抽代链上（与 [[Manifold]] 同被错放进 Index 的 "Algebraic Objects"） |

---

## 二、ALU 的代数结构（卡片要引用的骨架）

### 1. 两层表示，一条恒等式黏合

- 位层（电路）：$F_i=A_i\oplus B_i\oplus C_i$，$C_{i+1}=A_iB_i+C_i(A_i\oplus B_i)$
- 整数层（算术）：$f(x,y,c)=\big((x+y+c)\bmod 2^n,\ \lfloor (x+y+c)/2^n\rfloor\big)$
- **定义式**：$\tilde\nu(A)+\tilde\nu(B)+C_{in}=2^nC_{out}+\tilde\nu(F)$（唯一确定电路行为）

### 2. 唯一固有结构：位权

$$\varepsilon:\{0,1\}^n\to\mathbb{N},\qquad \varepsilon(w)=\sum_i2^iw_i\qquad(\text{双射到 }[0,2^n))$$

不是编码，是物理事实（第 $i$ 根线权 $2^i$）。**整个模型只需相信这一条。**

### 3. 由公理导出的定理（不是假设）

- $W$ 被赋予群结构：$\cong\mathbb{Z}/2^n$，同构映射就是 $\varepsilon$
- $C_{in}$ = **平移项**（仿射参数）：$\varepsilon(F(A,B,c))\equiv\varepsilon(F(A,B,0))+c$
- $C_{out}$ = **商** = 规范截面的 **2-上循环**：$\kappa(x,y)=2^nC_{out}$，取值 $\{0,2^n\}$
- 内部进位：$C_i=\lfloor s/2^i\rfloor-\lfloor s_1/2^i\rfloor-\lfloor s_2/2^i\rfloor$（截断的非可加性）
- 万有性质：$n$ 根输出线 ⇒ 输出必然穿过 $\mathbb{N}\twoheadrightarrow\mathbb{Z}/2^n$

### 4. 与 $\mathbb{Z}/2$、$(\mathbb{Z}/2)^n$ 的区别

$$\underbrace{\mathbb{Z}/2}_{\text{一层}}\qquad\underbrace{(\mathbb{Z}/2)^n}_{\text{层独立：硬件免费}}\qquad\underbrace{\mathbb{Z}/2^n}_{\text{层用进位粘起来}}$$

- 滤链 $\mathbb{Z}/2^n\supset2\mathbb{Z}/2^n\supset\cdots$，**逐层商都是 $\mathbb{Z}/2$**（一层 = 一位）
- 但不分裂：$(\mathbb{Z}/2)^n\not\cong\mathbb{Z}/2^n$（指数 2 vs 阶 $2^n$）
- 自同构群：$|(\mathbb{Z}/2^n)^\times|=2^{n-1}$（128）vs $|GL_8(\mathbb{F}_2)|\approx5.3\times10^{18}$
- **$C_{out}$ 不在 $\mathbb{Z}/2^n$ 里** —— 它是层的粘合数据

### 5. 四层阶梯（每下一步丢一样东西）

| 层 | 内容 | 丢了什么 |
|---|---|---|
| 位层 | 布尔 / $\mathbb{F}_2$ | — |
| 整数层 | $\mathbb{N}$ 带余除法，$C_{out}$ 保留 | — |
| 商层 | $\mathbb{Z}/2^n$ 加群 | 丢 $C_{out}$（丢商） |
| 读数层 | section / 编码 | 丢类（选代表元）⇒ 条件性 |

**判别四问**：只用 bit？→位层。用 $\tilde\nu$ 且没取模？→整数层。丢 $C_{out}$ 只留 $\equiv$？→商层。出现 $\sigma$/$\le$/"不溢出"？→读数层（唯一带条件的）。

---

## 三、逐卡辅导要点

### 卡 1：[[Quotient Group]]

**要回答**：把子群压成单位元之后，剩下的东西为什么还是个群？

要点：
1. 底集合 $G/H=\{aH\mid a\in G\}$ —— 元素是**陪集**（集合），不是元素
2. 运算 $(aH)(bH)=abH$
3. **良定义 ⟺ $H\vartriangleleft G$**。三步证明：
   - 换代表元 $a\mapsto ag,\ g\in H$
   - 凑共轭：$agbH=ab\,(b^{-1}gb)\,H$（插入 $bb^{-1}=e$）
   - 引理 $k\in H\Rightarrow kH=H$ ⇒ 需 $b^{-1}gb\in H\ \forall b,g$ ⟺ 正规
4. 单位元 $eH=H$（是陪集）；逆元 $(aH)^{-1}=a^{-1}H$；阶 $|G/H|=|G|/|H|$
5. 哑变量替换引理：$\varphi(X)=X$ 才可换（**单射不够**；反例 $\mathbb{Z}\to\mathbb{Z},x\mapsto2x$）
6. 视角：合法忽略 / 万有性质（$G/\ker\phi\cong\operatorname{Im}\phi$）/ 阿贝尔群商总存在 / 实例 $\mathbb{Z}/n\mathbb{Z}$

反例（已验）：$S_3$ 中 $H=\{e,(12)\}$ ⇒ **48** 组良定义反例；$H=A_3$ ⇒ **0** 组。

自检：$|\mathbb{Z}/256|=?$（256 = 8 位字总数）；$H$ 不正规时坏在哪一步；$G/H$ 与 $\operatorname{Im}\phi$ 关系。

### 卡 2：[[Generator of Cyclic Group]]

要点：
1. $g$ 是生成元 ⟺ $\langle g\rangle=G$
2. 在 $\mathbb{Z}/m$ 中：$k$ 是生成元 ⟺ $\gcd(k,m)=1$（因 $|k|=m/\gcd(k,m)$）
3. 生成元个数 $=\phi(m)$；$m=2^n\Rightarrow\phi=2^{n-1}$
4. **位层刻画**：$2^n$ 情形下生成元 = 奇数 = **最低位为 1**，占一半
5. 例：$1$（加 1）、$255$（加 255 = 减 1）、$3,5,\dots$；反例 $2$（阶 128，只走到偶数）

自检：$n=8$ 有几个生成元？（128）为什么 2 不是？

### 卡 3：[[Difference between Order of Group and Cyclic Group]]

要点：
1. **群的阶** $|G|$ = 元素个数（见 [[The Order of Group]]）
2. **元素的阶** $|x|$ = 最小 $n$ 使 $x^n=e$（见 [[order of cyclic subgroup]]）
3. 关系：$|x|=|\langle x\rangle|$；拉格朗日 ⇒ $|x|\mid|G|$
4. 阶 $d$ 的元素个数 $=\phi(d)$
5. $n=8$ 实例：$|1|=256$、$|2|=128$、$|128|=2$、$|0|=1$；阶分布 $1,1,2,4,8,16,32,64,128$
6. 口诀：$x=2^t\cdot$奇数 ⇒ 阶 $=2^{8-t}$

自检：「群的阶 256」与「元素 1 的阶 256」是两个不同陈述。

### 卡 4：[[Correspondence Theorem]]（别名：第四/格同构定理）

要点：
1. $N\vartriangleleft G$ ⇒ 双射
   $$\{H\mid N\le H\le G\}\ \longleftrightarrow\ \{K\mid K\le G/N\},\qquad H\mapsto H/N$$
2. 保持：包含关系、正规性、指数 $[G:H]=[G/N:H/N]$
3. 用途：商群的子群结构 = 原群中夹着 $N$ 的子群
4. 实例：$\mathbb{Z}$ 的子群 $m\mathbb{Z}$ ↔ $\mathbb{Z}/n\mathbb{Z}$ 的子群；滤链每层一位

自检：$\mathbb{Z}/256$ 有几个子群？（9 个，对应 256 的因子）

---

## 四、[[Normal Subgroup]] 的共轭段（已讲）

`## Trick` 段的 `[[Bijective Map]] $C(a) = $` 待补：

```
## Trick
[[Automorphism]] $C_a: G \to G$,  $C_a(x) = axa^{-1}$   （也写作 $x^a$）
1. $C_a \in \mathrm{Aut}(G)$;  $C_a^{-1} = C_{a^{-1}}$;  $C_{ab} = C_a \circ C_b$
2. $N \vartriangleleft G \iff C_a(N) = N\ \ \forall a \in G$   （只需证 $\subseteq$）
3. $N \vartriangleleft G \Rightarrow C_a|_N \in \mathrm{Aut}(N)$
4. $\ker(a \mapsto C_a) = Z(G)$
```

- **为什么是双射**：$C_a=\lambda_a\circ\rho_{a^{-1}}$（左乘 ∘ 右乘），平移是双射（逆元）⇒ 复合双射；或直接给逆 $C_{a^{-1}}$
- 记号警告：别写 $C(a)=axa^{-1}$（变量没绑定）；定义里用 $n\in N$ 避免与 $a\in G$ 撞名
- 例子：$S_3/A_3$ 上非平凡（$(012)\leftrightarrow(021)$）；$S_3/\{e,(12)\}$ 像跑出 $N$；**阿贝尔群 ⇒ $C_a=\mathrm{id}$**（机器数那一侧没有共轭问题）
- **链接问题（状态已变）**：[[Conjugate]] 现位于 **root 队列**（`Conjugate.md`，`aliases: Inner Automorphism`）—— owner 已在消歧，待 triage 归位；有理化那一路的兄弟卡是 Conjugate Radicals / Hyperbolic Conjugate Radical 等

---

## 五、已验证事实清单（可复现）

| 事实 | 验证 |
|---|---|
| 全加器布尔式 == 带余除法描述 | $n=4,8$ 穷举 |
| $\varepsilon$ 是同构；$\mathbb{Z}/2^n$ 循环 | 穷举 |
| $(\mathbb{Z}/2)^n\not\cong\mathbb{Z}/2^n$ | 指数 2 vs 阶 $2^n$ |
| $C_{out}\in\{0,1\}$，$\kappa=2^nC_{out}$ 满足 2-上循环恒等式 | 穷举 |
| 进位 = 截断非可加性；$C_{in}$ 是纯平移 | 穷举 |
| 两个 4 位单元串联 = 8 位加法器 | 穷举 |
| 生成元 = 奇数（128 个）；阶 $=2^{8-\text{尾随零}}$ | 穷举 |
| 子群 9 个，阶 = 256 的因子 | 穷举 |
| $A\mapsto F(A,B,0)$ 非 $\mathbb{F}_2$-仿射（$B\ne0$） | 穷举 |
| $S_3$：$A_3$ 良定义 0 反例 / $\{e,(12)\}$ 48 反例 | 穷举 |
| $C_a$ 是自同构、$C_{ab}=C_a\circ C_b$、$\ker=Z(G)$ | $S_3$ 穷举 |
| 哑变量替换需双射（单射不够） | $\mathbb{Z}\to\mathbb{Z},x\mapsto2x$ |

---

## 六、待办

- [ ] 四张枢纽卡正文（owner 落笔，按 §三 骨架）
- [ ] [[Normal Subgroup]] 的 `## Trick` 段补全（§四）
- [ ] [[Conjugate]]（现在 root 队列，别名 Inner Automorphism）待 triage 归位 library
- [ ] `check` 的 G1 未过：root 队列有 `Well Define.md`、`Conjugate.md` 待 triage（**非本轮改动造成**）
