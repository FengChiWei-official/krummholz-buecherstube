# P-Tuning (v1 & v2)

## 基本信息
- **P-Tuning v1**:
    - 论文：GPT Understands, Too
    - 作者：Xiao Liu, Yanan Zheng, Zhengxiao Du, et al.
    - 发表：arXiv 2021
    - 链接：[https://arxiv.org/abs/2103.10385](https://arxiv.org/abs/2103.10385)
- **P-Tuning v2**:
    - 论文：P-Tuning v2: Prompt Tuning Can Be Comparable to Fine-tuning Universally Across Scales and Tasks
    - 作者：Xiao Liu, Kaixuan Ji, Yicheng Fu, et al.
    - 发表：ACL 2022
    - 链接：[https://arxiv.org/abs/2110.07602](https://arxiv.org/abs/2110.07602)
- 代码链接：[https://github.com/THUDM/P-tuning](https://github.com/THUDM/P-tuning) / [https://github.com/THUDM/P-tuning-v2](https://github.com/THUDM/P-tuning-v2)

## 核心问题
- **v1**: 离散的 Prompt（人工设计）极其不稳定且难以优化。如何让 GPT 等生成式模型在 NLU（自然语言理解）任务上也表现出色？
- **v2**: Prompt Tuning 和 P-Tuning v1 在小模型（<10B）和困难序列标注任务上表现不佳。如何打破“只有大模型才适合 Prompt Tuning”的局限？

## 主要贡献
### P-Tuning v1
1. 提出了 **P-Tuning**，将自然语言 Prompt 替换为可训练的连续 Embedding 向量。
2. 引入了 **Prompt Encoder**（通常是 LSTM 或 MLP），通过建模 Prompt token 之间的依赖关系来解决独立优化 Embedding 导致的训练不稳定问题。
3. 证明了 GPT 模型在 P-Tuning 下可以获得与 BERT 相当的 NLU 能力。

### P-Tuning v2
1. 提出了 **Deep Prompt Tuning** 策略，类似于 Prefix-Tuning，将可训练的 Prompt 向量加入到 Transformer 的**每一层**，而不仅仅是输入层。
2. 移除了 v1 中的复杂 Encoder（如 LSTM），直接优化 Prompt 参数，简化了流程。
3. 验证了 v2 在不同规模模型（从 300M 到 100B）和不同任务（包括序列标注等难任务）上都能媲美全量微调。

## 技术要点
- **连续空间映射 (v1)**：
  使用一个轻量级神经网络（Prompt Encoder）$f$ 来生成 Prompt Embedding $h_i$：
  $$ h_i = f(e_i) $$
  这样可以保持 Prompt 向量间的相关性，避免陷入局部最优。
- **Deep Prompting (v2)**：
  在每一层 $l$ 的输入前都拼接可训练的前缀向量 $P_l$。
  $$ [P_l; h_{l-1}] $$
  这增加了可训练参数的数量（0.1% -> 1%~3%），并提供了更直接的层间控制能力。
- **多任务与多尺度适应 (v2)**：
  通过多层 Prompt，模型能够更好地捕捉深层语义，解决了 v1 在序列标注等精细任务上表现差的问题。

## 实验结果
- **v1**: 在 LAMA 和 SuperGLUE 上，P-Tuning 显著优于人工离散 Prompt，并且让 GPT-2 等生成模型在理解任务上追平了 BERT。
- **v2**: 在 SuperGLUE 和序列标注任务（NER, SRL）上，P-Tuning v2 在各种规模的模型上都达到了与全量 Fine-tuning 几乎一致的性能，尤其是在小模型上显著优于 Prompt Tuning 和 P-Tuning v1。

## 创新点
- **v1**: 解决了离散 Prompt 优化的不连续性问题，利用 Encoder 建模 Prompt 内部依赖。
- **v2**: 将 Prefix-Tuning 的“深层注入”思想引入到 NLU 任务的 Prompt Tuning 中，打破了 Prompt Tuning 仅适用于超大模型的刻板印象。

## 缺点与局限
- **v1**: 仅在输入层加入 Prompt，对深层语义的引导能力有限，且在小模型上效果不如全量微调。
- **v2**: 虽然参数量依然很少，但相比 v1 和 Prompt Tuning，参数量有所增加；且实现上需要侵入模型每一层，不如仅修改输入层方便。

## 应用价值
- **ChatGLM 的微调**：P-Tuning v2 是 ChatGLM 系列模型官方推荐的高效微调方法之一，广泛应用于中文大模型的下游适配。
- **全能适配**：v2 提供了一种通用的、跨规模、跨任务的解决方案，适合资源受限但追求高性能的场景。

## 相关笔记
- [[11-Prefix-Tuning]]
- [[12-Prompt-Tuning]]
- [[reading/reading-notes/PEFT/LoRA-低秩适配]]

## 个人总结
P-Tuning 系列展示了 Soft Prompt 方法的进化。v1 解决了“怎么把 Prompt 变成可微的”，v2 解决了“怎么让 Soft Prompt 在小模型和难任务上也管用”。v2 本质上是 Prefix-Tuning 在 NLU 任务上的优化和验证，证明了 Deep Prompting 是提升参数高效微调上限的关键。
