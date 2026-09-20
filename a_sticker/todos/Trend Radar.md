---
tags:
  - todo
---

## Aim

Trend Radar 每日情报流的索引：原始清单与精选报告一律落 `archives/`（`TR-raw-*` / `TR-*`），本笔记只挂载当前仍在的件。报告按 ISO 周 → 自然月 → 自然年滚动合并（7/4/12），被合并件删除。

## Items

- [ ] [[TR-D-2026-09-20]]（日报，11 条精选） — 原始 [[TR-raw-D-2026-09-20]]
- [ ] [[TR-leaderboards]]（当前榜单快照：Arena AI 文本/代码 + SWE-bench Verified；每日覆盖）

## Key Methods

- 调用：让 AI 跑 skill `trend-radar`（`.agent/skills/trend-radar/SKILL.md`）
- 抓取层：HuggingFace / arXiv / Hacker News / Lobsters / GitHub / OpenAlex，原始清单零 AI 改写、逐条可回溯到 API 快照
- 精选层：~10 条，每条一句为什么值得看；空白处用 web_search 补漏

## Applications

---
## **Related**

- [[Index of Todos]]
- [[TR-leaderboards]]
- [[AI 报告挂载 Todo]]
