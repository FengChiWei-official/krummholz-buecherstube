# Prompt Tuning

## 基本信息
- 作者：Brian Lester, Rami Al-Rfou, Noah Constant
- 发表：EMNLP 2021
- 论文链接：[https://arxiv.org/abs/2104.08691](https://arxiv.org/abs/2104.08691)
- 代码链接：[https://github.com/google-research/prompt-tuning](https://github.com/google-research/prompt-tuning)

## 核心问题
随着预训练语言模型（PLM）参数量的爆炸式增长（如 GPT-3 达到 175B），为每个下游任务进行全量微调（Fine-tuning）变得极其昂贵且存储不便。如何在不修改模型主体参数的前提下，高效地适配下游任务？

## 主要贡献
1. 提出了 **Prompt Tuning**：一种简化的参数高效微调方法，仅在输入层添加可训练的连续向量（Soft Prompts），冻结整个预训练模型。
2. 证明了随着模型规模的增加（Scale），Prompt Tuning 的性能逐渐逼近全量微调，并在百亿参数规模上几乎持平。
3. 展示了 Prompt Tuning 在域外泛化（Domain Generalization）和抗干扰性上的优势。

## 技术要点
- **Soft Prompts**：在输入序列的 Embedding 层之前拼接一组可训练的向量 $P \in \mathbb{R}^{p \times e}$（$p$ 为 prompt 长度，$e$ 为 embedding 维度）。
- **冻结骨干网络**：训练过程中，仅更新 Soft Prompts 的参数，Transformer 主体的所有权重保持不变。
- **Prompt Ensembling**：通过训练多个不同的 prompt 并集成它们的预测结果，进一步提升性能。
- **初始化策略**：探讨了随机初始化、采样词汇表初始化和类标签初始化对性能的影响，发现使用类标签含义初始化收敛更快。

## 实验结果
- **规模效应**：在 T5 模型上实验，发现当模型参数达到 10B 级别时，Prompt Tuning 的表现与全量 Model Tuning 差距极小。
- **任务性能**：在 SuperGLUE 等基准测试上取得了有竞争力的结果。
- **参数效率**：每个任务仅需存储极少量的 Prompt 参数（通常几百个 token 的 embedding），相比全量微调节省了几个数量级的空间。

## 创新点
- **极简主义**：相比 Prefix-Tuning 在每一层都加入参数，Prompt Tuning 仅在输入层加入参数，结构更为简单。
- **规模验证**：强有力地证明了“模型越大，Prompt Tuning 越有效”的趋势，为大模型时代的轻量化适配提供了理论支持。

## 缺点与局限
- **小模型表现不佳**：在参数量较小（如 BERT-base, T5-base）的模型上，Prompt Tuning 的效果显著低于全量微调。
- **收敛速度**：相比全量微调，Soft Prompt 的训练可能需要更多的 epoch 才能收敛。
- **超参敏感**：Prompt 的长度和初始化方式对最终性能有较大影响。

## 应用价值
- **多任务服务**：在一个共享的大模型底座上，通过切换不同的 Prompt 向量即可服务于不同的下游任务，极大地降低了部署成本。
- **隐私保护**：由于不修改模型权重，更适合在多租户场景下保护基础模型的知识产权或隐私。

## 相关笔记
- [[11-Prefix-Tuning]]
- [[13-P-Tuning]]
- [[reading/reading-notes/PEFT/LoRA-低秩适配]]

## 关键公式
$$ P(y|x) = P(y| [P; E(x)], \theta_{frozen}) $$
其中 $P$ 是可训练的 Prompt 向量，$E(x)$ 是输入的 Embedding，$\theta_{frozen}$ 是冻结的模型参数。

## 个人总结
Prompt Tuning 是 Soft Prompt 方法的极简代表。它揭示了大模型的一个重要特性：随着参数规模增加，模型对上下文（Prompt）的理解和适应能力变强，使得仅调整输入层就能达到很好的适配效果。它是 Prompt Engineering 的连续化、自动化版本。
