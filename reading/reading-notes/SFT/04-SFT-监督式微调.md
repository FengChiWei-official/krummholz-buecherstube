# Supervised Fine-Tuning (SFT)

## 基本信息
- **概念**：监督式微调（Supervised Fine-Tuning）
- **相关论文**：无单一特定论文，广泛应用于 NLP 和 CV 领域。在 LLM 语境下，常指 InstructGPT 或 Llama-2 中的 SFT 阶段。

## 核心问题
预训练语言模型（Pre-trained LLM）虽然拥有海量的知识和语言能力，但它们本质上是“文本补全机”（Next Token Predictor），并不一定能很好地遵循人类的指令（Instruction Following）或以对话的形式交互。SFT 的目的是教会模型“如何说话”以及“如何完成任务”。

## 主要流程
1. **数据准备**：收集或构造高质量的“指令-回复”对（Instruction-Response Pairs）。
   - 格式：`{ "instruction": "...", "input": "...", "output": "..." }`
2. **模型训练**：在预训练模型的基础上，使用标准语言模型损失函数（Cross-Entropy Loss）在这些数据上进行微调。
   - 通常只计算 Output 部分的 Loss（User 的指令部分不计算 Loss）。

## 技术要点
- **Data Quality vs. Quantity**：LIMA (Less Is More for Alignment) 论文指出，少量（如 1000 条）高质量、多样化的 SFT 数据比大量低质量数据更有效。
- **Prompt Template**：训练时需要将对话格式化为特定的模板（如 ChatML, Alpaca 格式），推理时必须使用相同的模板。
- **Packing**：为了提高训练效率，通常将多个短样本拼接成一个长序列（Sequence Packing），并使用 Attention Mask 隔离不同样本。

## 实验结果
- 经过 SFT 的模型（如 Vicuna, Alpaca）在对话质量和指令遵循能力上显著优于 Base 模型。
- SFT 是 RLHF（强化学习人类反馈）的前置步骤，为 RLHF 提供一个较好的初始策略模型（Policy Model）。

## 创新点
- 将“无监督预训练”的能力通过“有监督微调”引导到特定的人类交互模式上。

## 缺点与局限
- **幻觉（Hallucination）**：SFT 可能会导致模型产生幻觉，因为它被迫回答它可能不知道的问题。
- **对齐税（Alignment Tax）**：过度微调可能会导致模型在某些通用能力上退化。
- **数据依赖**：模型的效果高度依赖于 SFT 数据的质量和分布。

## 应用价值
- 构建聊天机器人（Chatbot）、特定领域的问答系统、Copilot 辅助工具等。

## 相关笔记
- [[05-InstructGPT]]
- [[06-Llama-2]]
- [[reading/reading-notes/PEFT/LoRA-低秩适配]]

## 个人总结
SFT 是将“读万卷书”的 Base 模型变成“行万里路”的 Chat 模型的关键一步。目前的趋势是追求更高质量、更少量的 SFT 数据（Data-Centric AI），以及使用合成数据（Synthetic Data）来提升 SFT 的效果。
