---
tags:
  - todo
---

## Aim

Trend Radar 每日情报流的索引：原始清单与精选报告一律落 `archives/`（`TR-raw-*` / `TR-*`），本笔记只挂载当前仍在的件。报告按 ISO 周 → 自然月 → 自然年滚动合并（7/4/12），被合并件删除。

## Items

- [ ] [[TR-D-2026-09-27]]（日报，20 条） — 原始 [[TR-raw-D-2026-09-27]]
- [ ] [[TR-D-2026-09-23]]（日报，23 条） — 原始 [[TR-raw-D-2026-09-23]]
- [ ] [[TR-D-2026-09-22]]（日报，22 条） — 原始 [[TR-raw-D-2026-09-22]]
- [ ] [[TR-D-2026-09-21]]（日报，22 条） — 原始 [[TR-raw-D-2026-09-21]]
- [ ] [[TR-D-2026-09-20]]（日报，11 条） — 原始 [[TR-raw-D-2026-09-20]]
- [ ] [[TR-leaderboards]]（当前榜单快照：Arena AI 文本榜、Arena AI 代码榜、SWE-bench Verified、Artificial Analysis Intelligence Index；每日覆盖）

## Key Methods

- 调用：让 AI 跑 skill `trend-radar`（`.agent/skills/trend-radar/SKILL.md`）
- 抓取层：HuggingFace（模型/数据集/Space/日报论文）/ arXiv（AI 桶 cs.AI·LG·CL + ML 算法桶 stat.ML·math.OC·cs.NA + 工程桶 cs.SE·PL·AR·OS + 算法桶 cs.DS·CG·CC）/ Semantic Scholar / OpenAlex（期刊会议）/ Hacker News / Lobsters / GitHub，原始清单零 AI 改写、逐条可回溯到 API 快照
- 精选层：分「精选 + 学术」两节，条数随当日信号浮动（不设固定配额）；学术节以 ML 算法/优化为主（≥2 条），工程桶与算法桶各 ≤2；每条一句为什么值得看，空白处用 web_search 补漏

## Applications

---
## **Related**

- [[Index of Todos]]
- [[TR-leaderboards]]
- [[AI 报告挂载 Todo]]
