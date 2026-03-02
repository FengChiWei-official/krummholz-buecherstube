# PEFT: State-of-the-art Parameter-Efficient Fine-Tuning Methods

## 基本信息
- **库/论文**：PEFT: State-of-the-art Parameter-Efficient Fine-Tuning Methods
- **作者**：Sourab Mangrulkar, Sylvain Gugger, Lysandre Debut, et al. (Hugging Face Team)
- **发表**：GitHub / Hugging Face Blog 2022
- **代码链接**：[https://github.com/huggingface/peft](https://github.com/huggingface/peft)
- **文档链接**：[https://huggingface.co/docs/peft](https://huggingface.co/docs/peft)

## 核心问题
随着大语言模型（LLM）参数量的激增，全量微调（Full Fine-tuning）对显存和计算资源的要求过高，普通开发者难以负担。虽然学术界提出了 LoRA、Prefix Tuning 等多种参数高效微调方法，但缺乏一个统一、易用且与主流 Transformers 库无缝集成的框架。

## 主要贡献
1. **统一框架**：提供了一个统一的接口来使用各种 PEFT 方法（LoRA, Prefix Tuning, P-Tuning, Prompt Tuning, AdaLoRA 等）。
2. **无缝集成**：与 Hugging Face Transformers 和 Accelerate 深度集成，只需几行代码即可将预训练模型转换为 PEFT 模型。
3. **轻量级模型分享**：PEFT 训练后的模型权重非常小（仅保存微调部分的参数），便于存储和分享（例如在 Hugging Face Hub 上）。

## 技术要点
- **PeftModel & PeftConfig**：核心抽象类。`PeftConfig` 定义微调方法的超参数，`PeftModel` 包装基础 Transformer 模型并注入可训练参数。
- **支持的方法**：
    - **LoRA**: Low-Rank Adaptation
    - **Prefix Tuning**: P-Tuning v2
    - **P-Tuning**: v1
    - **Prompt Tuning**
    - **IA3**
    - **AdaLoRA**
- **Task Type 支持**：支持 Causal LM, Seq2Seq LM, Sequence Classification, Token Classification 等多种任务。

## 实验结果
- 使得在消费级 GPU（如 RTX 3090/4090）上微调百亿参数级模型（如 Llama-2-13b, Falcon-40b）成为可能（配合 4-bit/8-bit 量化）。
- 性能上，PEFT 方法通常能达到全量微调 95%-100% 的效果，但显存占用和存储空间大幅降低。

## 创新点
- 将学术界的离散算法工程化为通用的工业级工具。
- 极大地降低了 LLM 微调的门槛，推动了开源 LLM 社区的繁荣。

## 缺点与局限
- 作为一个库，它依赖于上游 Transformers 的更新，有时会有版本兼容性问题。
- 对某些极新的模型架构支持可能需要等待适配。

## 应用价值
- **工业界标准**：目前是开源社区进行 LLM 微调的事实标准工具。
- **资源优化**：节省训练成本和存储成本。

## 相关笔记
- [[reading/reading-notes/PEFT/LoRA-低秩适配]]
- [[02-QLoRA-量化微调]]
- [[11-Prefix-Tuning]]

## 个人总结
PEFT 库是 LLM 民主化的重要推手。它不仅是一个代码库，更定义了“基础模型 + 适配器（Adapter）”的开发范式。掌握 PEFT 库的使用是进行 LLM 应用开发的必备技能。
