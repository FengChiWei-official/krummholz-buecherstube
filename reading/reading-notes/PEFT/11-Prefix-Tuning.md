# Prefix-Tuning

## 基本信息
- 作者：Xiang Lisa Li, Percy Liang
- 发表：ACL 2021
- 论文链接：[https://arxiv.org/abs/2101.00190](https://arxiv.org/abs/2101.00190)
- 代码链接：[https://github.com/XiangLi1999/PrefixTuning](https://github.com/XiangLi1999/PrefixTuning)

## 核心问题
如何在保留大模型固有知识的情况下，通过极小量的可训练参数对模型进行下游任务适配，以减少计算与存储开销，同时避免微调导致的灾难性遗忘？

## 主要贡献
1. 提出 Prefix-Tuning（或 Prompt Tuning/Prefix-based methods）思路：冻结模型大部分参数，仅在输入/隐藏层前加入一小段可训练的前缀（prefix）或提示向量进行微调。
2. 展示在若干下游任务上仅训练很少参数仍能达到与完整微调可比的性能。
3. 分析了 prefix 的长度、位置、参数量与性能之间的权衡。

## 技术要点
- **Deep Prefix (深层前缀)**：不同于仅在 Embedding 层加入 Prompt（如 P-Tuning v1 的部分做法），Prefix-Tuning 在 Transformer 的**每一层**的 Multi-head Attention 模块中都加入了可训练的前缀。具体来说，它将可训练的 prefix 向量 $P_K, P_V$ 分别拼接在原本的 Key 和 Value 矩阵之前。
- **Reparameterization (重参数化)**：直接优化高维的 Prefix 参数 $P$ 往往不稳定且难以收敛。作者提出使用一个较小的矩阵 $P'$ 配合一个 MLP（通常是两层，含 Tanh 激活）来生成最终的 $P$。
  - 训练时：$P = \text{MLP}(P')$
  - 推理时：丢弃 MLP，只保留计算好的 $P$，因此推理时没有额外的网络结构开销（仅序列变长）。
- **Virtual Tokens (虚拟 Token)**：模型将这些 Prefix 视为一系列“虚拟 Token”的激活值，它们不对应实际的词表单词，而是作为连续的自由参数存在，充当了“上下文”的角色。
- **冻结模型主体**：仅优化 prefix 参数，从而显著降低训练成本和存储开销（每个任务只需存储 prefix）。

## 实验结果（典型）
- 在若干自然语言生成和理解任务上，使用较短的 prefix（例如几十到几百个向量）即可实现与微调全部参数接近的效果（取决于任务与基模型规模）。
- 对比 LoRA / SFT 等方法，prefix-tuning 在参数效率与切换灵活性上有优势，但在某些任务上可能略逊色于 LoRA 等方法。

## 创新点
- **连续空间的 Prompt**：将 Prompt 从离散的文本 token 扩展为连续的可微向量，解除了 Prompt 必须由自然语言组成的限制。
- **Deep Prompting**：证明了仅在输入层加 Prompt 效果有限，而在所有层加入 Prefix (Deep Prompting) 才能达到与全量微调媲美的效果。
- **轻量化适配**：每个任务仅需存储极少量的参数（~0.1%），实现了极高的参数效率。

## 缺点与局限
- 对某些复杂任务或需要深度语义改变的任务，prefix 的表现可能不如对模型内部权重进行适当修改的技术（例如 LoRA 或完整微调）。
- 需要仔细选择 prefix 长度与注入位置，超参数敏感。

## 应用价值
- 适合在资源受限的场景中为多个下游任务提供轻量的适配方案（每个任务只保存小量 prefix 参数）。
- 便于在模型供应方共享基础模型并只分发各任务的 prefix，从而降低隐私或模型再发行成本。

## 相关笔记
- [[reading/reading-notes/PEFT/LoRA-低秩适配]]
- [[02-QLoRA-量化LoRA]]
- [[10-PEFT-参数高效微调框架]]

## 关键公式（如有）
- **激活值计算**：
  设 $P_{idx}$ 为前缀索引集合，$\phi$ 为冻结的 LM 参数，$\theta$ 为可训练的 Prefix 参数。
  $$ h_i = \begin{cases} P_\theta[i], & \text{if } i \in P_{idx} \\ \text{LM}(z_i, h_{<i}, \phi), & \text{otherwise} \end{cases} $$
- **Attention 修改**：
  在每一层注意力头中，拼接 Prefix 到 Key 和 Value：
  $$ K' = [P_K ; K_{text}], \quad V' = [P_V ; V_{text}] $$
  其中 $P_K, P_V$ 是该层特定的可训练参数。
- **重参数化**：
  $$ P_\theta[i,:] = \text{MLP}(P'[i,:]) $$

## 个人总结
Prefix-Tuning 是一种非常实用的参数高效适配思路，适合需要快速切换或低存储开销的场景。与 LoRA 等参数高效方法相比，它更强调模块化与推理时的轻量切换，但在某些任务上可能需要与其他方法复合使用以获得最佳效果。

---

*笔记模板来源：`LLM微调论文阅读笔记-INDEX.md`*
