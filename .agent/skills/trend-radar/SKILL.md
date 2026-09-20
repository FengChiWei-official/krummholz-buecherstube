---
name: trend-radar
description: "Daily trend radar for a geek/AI-scholar: fetch GitHub/HuggingFace/arXiv/Hacker News/Lobsters/OpenAlex trending via API, archive the raw lists, write a ~10-item curated report with links and why-lines, roll reports up by ISO week → month → year, and index them under the todo tree. Use when the owner says 跑 trend radar / 今天的趋势 / 每日情报 / trend-radar."
---

# trend-radar

Owner-facing purpose: **每天一次调用，把该看的链接挑好并挂进 todo**，省掉自己刷榜的时间。

One call = one day. Nothing runs in the background; there is no daemon, no watcher, no cron.

## Contract

| Layer | Path | Nature |
|---|---|---|
| 原始清单 | `archives/TR-raw-D-<YYYY-MM-DD>.md` | 机器生成，零 AI 改写，每条 = 源侧字段原样映射，逐条可回溯到 API 快照 |
| 精选报告 | `archives/TR-D-<YYYY-MM-DD>.md` | 8–12 条，每条 = 链接 + 来源 + 一句"为什么值得看" |
| 榜单快照 | `archives/TR-leaderboards.md` | **每次抓取整体覆盖**，只留当前榜单 + Δ 列；`TR-leaderboards.state.json` 存上一份用于算 Δ。两者都不参与滚动合并 |
| 索引 | `a_sticker/todos/Trend Radar.md` | 裸 `todo` 标签；只链当前仍在的件 |
| 滚动件 | `archives/TR-{W,M,Y}-*.md` 与 `TR-raw-{W,M,Y}-*.md` | 7 日报→周报、月内 ≥4 周报→月报、年内 ≥12 月报→年报；**被合并件删除，不保留** |

Tool: `tools/trend_radar.py`（stdlib only）。

## Leaderboards（`fetch` 自动抓，无需额外命令）

| 榜 | 取数方式 | 备注 |
|---|---|---|
| Arena AI 文本榜 / 代码榜（原 LMArena） | 每日镜像 `github.com/oolong-tea-2026/arena-ai-leaderboards` → `data/<date>/text.json`｜`code.json` | 官网无公开 API（`lmarena.ai/api/*` 403）。表头写明 `source_url=arena.ai/...` 与上游 `last_updated`；镜像当天没出就退回其 `latest.json` 指针 |
| SWE-bench Verified | 官方仓库 `swe-bench.github.io/data/leaderboards.json`，取 `Verified` 子榜，按 `resolved` 降序 | 表里给 Agent/组织/%Resolved/提交日期 |
| Artificial Analysis Intelligence Index | 官方 API v2 `data/llms/models`，`x-api-key` | 只在设置了 `ARTIFICIAL_ANALYSIS_API_KEY` 时才抓；没设写"未启用"，key 无效写"降级" |

- 每榜列前 10（`LB_TOP`），表头带来源、抓取时间、条目数、快照 sha256；`Δ` 列对比上一份快照（`▲n`/`▼n`/`NEW`），`ΔElo`/`Δ分数` 同源。
- 同一天重复跑 `fetch` 不会污染 Δ：状态文件只在日期变化时推进。
- 榜单**不写进原始清单的 URL 列表**（快照不是链接流，且会被合并去重规则吃掉），日报里只放一行指针。
- owner 想看新榜：改 `LEADERBOARDS` 加一个 `@leaderboard(...)` 函数即可；Terminal-Bench 这类只有 Next.js 页面的站点需要额外解析，别默认加。

## Daily run

```bash
# 1. 抓取 + 写原始清单 + 打印候选池（这是给你挑选用的事实来源）
python3 tools/trend_radar.py fetch

# 2. 读候选池，必要时用 web_search 补 API 抓不到的漏
#    （X/Twitter、中文源、博客、跨源在吵什么），写下 /tmp/tr-items-<date>.json

# 3. 写报告 + 滚动合并 + 更新索引 + 自校验
python3 tools/trend_radar.py run --items /tmp/tr-items-<date>.json

# 4. 向 owner 汇报：今天几条、覆盖哪些源、哪几条值得先看；然后清理快照
python3 tools/trend_radar.py fetch --purge
```

Override the date to rebuild a past day: `--date 2026-09-19`（`--vault` / `--snapshot-dir` 同理，写在子命令前后皆可）。

### items.json

```json
[{"url": "https://…", "title": "…", "source": "HF Models #1 (trendingScore 1217)",
  "from": "raw", "why": "一句为什么值得看"},
 {"url": "https://…", "title": "…", "source": "web_search（中文源）",
  "from": "websearch", "query": "实际用过的搜索词", "why": "…"}]
```

Hard rules enforced by the tool (non-zero exit, nothing written):

- 8–12 items; no duplicate URLs; every item needs `title`/`source`/`why`.
- `from: raw` → the URL must exist verbatim in today's raw list.
- `from: websearch` → `query` is required, and the report marks the item `⟦ws: …⟧` so the provenance gap is visible instead of implied.

Pick for signal, not coverage: cross-source repeats (same story on HN **and** Lobsters **and** GitHub) are the strongest signal; a single source's #1 is next; a low-score item is fine when it is on a line the owner tracks (compilers, systems, math).

## Rolling

Runs inside `run` — nothing separate to call.

- ISO week of a daily's date decides its weekly label (`TR-W-2026-W38`); a weekly belongs to the month of its ISO week's Thursday.
- Weekly: 7 dailies in one ISO week → merge (dedupe by URL, cross-file repeats tagged `⟦YYYY-MM-DD⟧`), delete the 7 dailies + their raw files.
- Monthly: ≥4 weeklies in one calendar month → merge, delete them. Yearly: ≥12 monthlies → merge, delete them.
- Raw merges on the same clock but keeps only the first `MERGE_RAW_CAP` (50) entries, so `archives/` cannot grow without bound; full snapshots are never kept.
- Re-merging preserves the previous merged file as the base (no loss), and the index is regenerated from the filesystem, so it never points at a deleted file.

## Failure handling

- **One source down / rate-limited / 403** → that section is written as `> [降级] 抓取失败：<reason>`, the other sources proceed, exit code stays 0, and the report carries a 降级 line. Never abort the run for one source.
- **`OPENALEX_API_KEY` unset** → only OpenAlex degrades; report it to the owner and deliver the rest. The key is read from the environment only — never written to a note, never printed (the tool redacts `api_key=` in every path it writes).
- **`ARTIFICIAL_ANALYSIS_API_KEY` unset** → the AA row reads 未启用 (not an error). Set but rejected → that board alone degrades (`HTTP 401`), other boards keep their tables. Same rule: key from env, `x-api-key` header only, never written down.
- **No network** → all sections degrade; still write the files, tell the owner it was a network failure, and do not treat the day as covered.
- **`fetch` interrupted after writing the raw list** → rerun `run`; `fetch` is safe to rerun (it overwrites and warns).

## Verify before reporting

```bash
python3 tools/trend_radar.py verify                     # 当天三层产出 + 滚动不变量
python3 tools/vault.py check                            # 结构不变量（本流程不得引入新 problem）
```

`verify` asserts: every non-degraded section ≥20 items, provenance hit rate N/N, report 8–12 items with no URL outside (raw ∪ `⟦ws⟧`-tagged), index links resolve and cover every current artifact (+ the leaderboard note), leaderboard tables each have ≥10 rows with a source line and snapshot hash, the Δ state file parses, and no ISO week holds ≥7 unmerged dailies.

`vault.py check` already fails on a **pre-existing** baseline (root-drain, legacy lit-without-source, 2 unresolved links). The requirement is only: no new finding mentioning `TR-`/`Trend Radar`.

## Boundaries

Write: `archives/TR-*.md` 与 `archives/TR-leaderboards.state.json`、`a_sticker/todos/Trend Radar.md`、`a_sticker/todos/Index of Todos.md`（一行登记）、`tools/trend_radar.py`。

Never: `zzz_output/` contents, `.obsidian/`, `library/`, `README.md`, `AGENTS.md`, any note this flow did not create; no new zone layers (artifacts stay flat in `archives/`); no commit, no push. Deletion is limited to TR- files this flow merged away.

## Stop and ask the owner when

- A period threshold is reached but the files that would be deleted are not exclusively TR- artifacts.
- The owner wants a new source, a different item count, or a different index location (contract change).
- OpenAlex key is missing/permission-denied and a second run also fails.
- Two consecutive runs degrade the same source for different reasons (likely a source API change, not a transient outage).
