---
tags:
  - type/permanent
  - status/archive
  - topic/ai
created: 2026-09-27
data-date: 2026-09-27
source:
  - "Arena AI 文本榜（Chatbot Arena）：https://arena.ai/leaderboard/text（30 条，2026-09-27T07:02:57Z，快照 sha256 e5329fdeffb8）"
  - "Arena AI 代码榜：https://arena.ai/leaderboard/code（30 条，2026-09-27T07:02:57Z，快照 sha256 604848bed170）"
  - "SWE-bench Verified（官方榜单）：https://www.swebench.com/（173 条，2026-09-27T07:34:54Z，快照 sha256 83cd949a9582）"
  - "Artificial Analysis Intelligence Index：https://artificialanalysis.ai/leaderboards/models（462 条，2026-09-27T07:34:56Z，快照 sha256 5dd180c99228）"
---

# Trend Radar 榜单 2026-09-27

> 每次抓取整体覆盖，只保留当前快照；变化由 Δ 列给出（对比上一份快照）。
> Arena AI（原 LMArena）无公开 API，数据经非官方每日镜像（MIT 许可）；官方口径以表头 `来源` 为准。SWE-bench 取官方仓库 JSON。

## arena-text — Arena AI 文本榜（Chatbot Arena）

> 来源 https://arena.ai/leaderboard/text · 2026-09-27 · 2026-09-27T07:02:57Z · 共 30 条，此处列前 10 · 上游更新 Sep 25, 2026 · 快照 sha256 e5329fdeffb8

| # | Δ | 模型 | 厂商 | Elo | ΔElo | 票数 · 许可 |
|---|----|------|------|------|------|------|
| 1 | NEW | claude-opus-5.5-high | Anthropic | 1509 | — | 2307 · proprietary |
| 2 | — | claude-opus-4-6-high | Anthropic | 1505 | — | 76518 · proprietary |
| 3 | ▼2 | claude-fable-5-high | Anthropic | 1504 | -2 | 36462 · proprietary |
| 4 | ▼1 | claude-opus-4-7-high | Anthropic | 1502 | — | 64007 · proprietary |
| 5 | — | claude-fable-5.1-max | Anthropic | 1501 | +3 | 9942 · proprietary |
| 6 | — | claude-opus-4-6 | Anthropic | 1498 | +1 | 80836 · proprietary |
| 7 | ▼3 | muse-spark-1.2 (xHigh) | Meta | 1496 | -4 | 3422 · proprietary |
| 8 | ▼1 | claude-opus-4-7 | Anthropic | 1495 | +1 | 65051 · proprietary |
| 9 | ▼1 | muse-spark-1.3-max | Meta | 1494 | +1 | 10036 · proprietary |
| 10 | ▼1 | gemini-3.8-flash-high | Google | 1492 | -1 | 21728 · proprietary |

## arena-code — Arena AI 代码榜

> 来源 https://arena.ai/leaderboard/code · 2026-09-27 · 2026-09-27T07:02:57Z · 共 30 条，此处列前 10 · 上游更新 Sep 25, 2026 · 快照 sha256 604848bed170

| # | Δ | 模型 | 厂商 | Elo | ΔElo | 票数 · 许可 |
|---|----|------|------|------|------|------|
| 1 | NEW | claude-opus-5.5-max | Anthropic | 1827 | — | 1607 · proprietary |
| 2 | ▼1 | gpt-6-astra-max | OpenAI | 1792 | -8 | 4908 · proprietary |
| 3 | ▼1 | claude-fable-5.1-max | Anthropic | 1751 | -7 | 5313 · proprietary |
| 4 | ▼1 | claude-opus-5-max | Anthropic | 1693 | +6 | 15627 · proprietary |
| 5 | NEW | gpt-6-sol-max | OpenAI | 1681 | — | 2019 · proprietary |
| 6 | — | qwen3.8-max | Alibaba | 1672 | +1 | 3469 · proprietary |
| 7 | — | claude-opus-5-high | Anthropic | 1662 | +2 | 18930 · proprietary |
| 8 | ▼4 | qwen3.8-max-0902 | Alibaba | 1662 | -19 | 6203 · proprietary |
| 9 | ▼4 | kimi-k3-max | Moonshot | 1660 | -14 | 14739 · proprietary |
| 10 | ▼2 | muse-spark-1.3-max | Meta | 1656 | +4 | 5945 · proprietary |

## swebench-verified — SWE-bench Verified（官方榜单）

> 来源 https://www.swebench.com/ · 官方仓库 main · 2026-09-27T07:34:54Z · 共 173 条，此处列前 10 · 快照 sha256 83cd949a9582

| # | Δ | Agent / 模型 | 组织 | %Resolved | Δ%Resolved | 提交日期 · 版本 |
|---|----|------|------|------|------|------|
| 1 | — | Sonar Foundation Agent + Claude 4.5 Opus | Anthropic | 79.2 | — | 2025-12-05 · Sonar |
| 2 | — | live-SWE-agent + Claude 4.5 Opus medium (20251101) | Anthropic | 79.2 | — | 2025-12-15 · UIUC |
| 3 | — | TRAE + Doubao-Seed-Code | ByteDance | 78.8 | — | 2025-09-28 · ByteDance |
| 4 | — | live-SWE-agent + Gemini 3 Pro Preview (2025-11-18) | Google DeepMind | 77.4 | — | 2025-11-20 · UIUC |
| 5 | — | EPAM AI/Run Developer Agent v20250719 + Claude 4 Sonnet | Anthropic | 76.8 | — | 2025-08-04 · EPAM Systems, Inc. |
| 6 | — | Atlassian Rovo Dev (2025-09-02) | Anthropic | 76.8 | — | 2025-09-02 · Atlassian |
| 7 | — | Claude 4.5 Opus (high) | Anthropic | 76.8 | — | 2026-02-17 · SWE-agent |
| 8 | — | ACoder | Anthropic | 76.4 | — | 2025-08-19 · ACoder |
| 9 | — | Gemini 3 Flash (high) | Google DeepMind | 75.8 | — | 2026-02-17 · SWE-agent |
| 10 | — | MiniMax M2.5 (high) | Minimax | 75.8 | — | 2026-02-17 · SWE-agent |

## artificial-analysis — Artificial Analysis Intelligence Index

> 来源 https://artificialanalysis.ai/leaderboards/models · 官方 API v2（keyed，同模型多变体取最优） · 2026-09-27T07:34:56Z · 共 462 条，此处列前 10 · 快照 sha256 5dd180c99228

| # | Δ | 模型 | 厂商 | Intelligence | ΔIntelligence | Coding / Agentic · 价格 · 速度 |
|---|----|------|------|------|------|------|
| 1 | — | Claude Opus 5.5 | Anthropic | 57.6 | — | $8/Mtok · 98.588 tok/s |
| 2 | — | Claude Fable 5.1 | Anthropic | 53.4 | — | Coding 81.6 · $20/Mtok · 71.375 tok/s |
| 3 | — | GPT-6 Astra | OpenAI | 52.7 | — | Coding 76.9 · $20/Mtok · 59.6 tok/s |
| 4 | — | Claude Opus 5 | Anthropic | 50.8 | — | Coding 78 · $10/Mtok · 0 tok/s |
| 5 | — | Claude Fable 5 | Anthropic | 49.6 | — | Coding 76.5 · $20/Mtok · 0 tok/s |
| 6 | — | Muse Spark 1.3 | Meta | 48.1 | — | Coding 75.8 · $2/Mtok · 161.149 tok/s |
| 7 | — | GPT-6 Sol | OpenAI | 47.5 | — | $4/Mtok · 86.998 tok/s |
| 8 | — | GPT-5.6 Sol | OpenAI | 47 | — | Coding 77.4 · $8/Mtok · 0 tok/s |
| 9 | — | Grok 4.7 | SpaceXAI | 46.4 | — | $3/Mtok · 70.989 tok/s |
| 10 | — | MiMo-V2.6-Pro | Xiaomi | 46.3 | — | $0.544/Mtok · 39.452 tok/s |

---
## Related

- [[Trend Radar]]
- [[AI 报告挂载 Todo]]
