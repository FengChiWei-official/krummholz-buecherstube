---
name: trend-radar
description: "Daily trend radar for a geek/AI-scholar: fetch GitHub/HuggingFace/arXiv/Hacker News/Lobsters/Semantic Scholar/OpenAlex trending via API, archive the raw lists, write a signal-sized two-layer report (精选 + 学术) with links and why-lines, roll reports up by ISO week → month → year, and index them under the todo tree. Use when the owner says 跑 trend radar / 今天的趋势 / 每日情报 / trend-radar."
---

# trend-radar

Owner-facing purpose: **每天一次调用，把该看的链接挑好并挂进 todo**，省掉自己刷榜的时间。

One call = one day. Nothing runs in the background; there is no daemon, no watcher, no cron.

## Contract

| Layer | Path | Nature |
|---|---|---|
| 原始清单 | `archives/TR-raw-D-<YYYY-MM-DD>.md` | 机器生成，零 AI 改写，每条 = 源侧字段原样映射，逐条可回溯到 API 快照 |
| 报告 | `archives/TR-D-<YYYY-MM-DD>.md` | 两节：`## 精选`（工业/社区热点）+ `## 学术`（论文）。条数随当日信号浮动（sanity 界 4–24，无固定配额），每条 = 链接 + 来源 + 一句"为什么值得看" |
| 榜单快照 | `archives/TR-leaderboards.md` | **每次抓取整体覆盖**，只留当前榜单 + Δ 列；`TR-leaderboards.state.json` 存上一份用于算 Δ。两者都不参与滚动合并 |
| 索引 | `a_sticker/todos/Trend Radar.md` | 裸 `todo` 标签；只链当前仍在的件 |
| 滚动件 | `archives/TR-{W,M,Y}-*.md` 与 `TR-raw-{W,M,Y}-*.md` | 7 日报→周报、月内 ≥4 周报→月报、年内 ≥12 月报→年报；**被合并件删除，不保留** |

Tool: `tools/trend_radar.py`（stdlib only）。

## Sources

| 节 | 内容 | 分层 |
|---|---|---|
| `hf-models` / `hf-datasets` / `hf-spaces` | HF trendingScore | 精选 |
| `hf-papers` | HF Daily Papers（upvotes = 真人信号） | 学术 |
| `arxiv` | cs.AI·cs.LG·cs.CL，**按提交时间倒序**（谁新谁前，无质量信号） | 学术 |
| `arxiv-ml` | **stat.ML·math.OC·cs.NA**，同上（主偏好：ML 算法与优化） | 学术 |
| `arxiv-plse` | cs.SE·cs.PL·cs.AR·cs.OS，同上（工程向添头） | 学术 |
| `arxiv-ds` | cs.DS·cs.CG·cs.CC，同上（算法与复杂度拓展） | 学术 |
| `s2` | Semantic Scholar Graph API，近 7 天 CS 论文按 `citationCount` 降序（被引/影响力引用/venue） | 学术 |
| `openalex` | 近 7 天 **期刊/会议** CS 文章（`primary_location.source.type:journal|conference`，排掉 Zenodo/预印本存取库）按被引降序 | 学术 |
| `hackernews` / `lobsters` | 当日前排/热榜 | 精选 |
| `github` | 7 天内新建仓库按 stars 降序 | 精选 |

- 学术层＝`ACADEMIC_SIDS`（hf-papers / arxiv / arxiv-ml / arxiv-plse / arxiv-ds / s2 / openalex）。**两层互斥**：学术源出来的条目只能进 `## 学术`，`## 精选` 只收非学术源（web_search 条目两节都可以）。
- **学术节偏好＝ML 算法优先**（`BUCKET_QUOTA`，`cmd_report` 与 `verify` 都强制）：`arxiv-ml` **≥2 条**（主），`arxiv-plse` **≤2 条**（添头），`arxiv-ds` **≤2 条**（拓展）。配额与当天信号冲突时停下来问 owner，别为凑数硬塞、也别把好条目静默丢掉。
- arXiv 的类目是 `cat:` 过滤，所以会收到**交叉列表**论文（主类目不是桶内类目），meta 里写的是响应返回的 primary category；同一篇可能同时落进两个桶（选报告时按它实际命中的 `sid` 归类，配额按那个桶算）。
- `openalex` 的条目下限是 10（`SECTION_FLOOR`），其余节默认 20（`MIN_ITEMS`）；过滤后不够就放宽窗口，别把阈值偷偷降掉。

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

# 4. 向 owner 汇报：今天几条、两节各几条、覆盖哪些源、哪几条值得先看；然后清理快照
python3 tools/trend_radar.py fetch --purge
```

Override the date to rebuild a past day: `--date 2026-09-19`（`--vault` / `--snapshot-dir` 同理，写在子命令前后皆可）。

### items.json

```json
[{"url": "https://…", "title": "…", "source": "HF Models #1 (trendingScore 1217)",
  "from": "raw", "section": "精选", "why": "一句为什么值得看"},
 {"url": "https://…", "title": "…", "source": "OpenAlex（被引 2 · ACM TOSEM）",
  "from": "raw", "section": "学术", "why": "…"},
 {"url": "https://…", "title": "…", "source": "web_search（中文源）",
  "from": "websearch", "section": "精选", "query": "实际用过的搜索词", "why": "…"}]
```

Hard rules enforced by the tool (non-zero exit, nothing written):

- 条数落在 sanity 界 4–24（`REPORT_MIN`/`REPORT_MAX`）；无重复 URL；每条要有 `title`/`source`/`why`。
- `section` ∈ {`精选`, `学术`}，**两节都不能空**。
- `from: raw` → URL 必须逐字出现在当天原始清单里，且所属节决定它能不能进这一节：学术源 → 只能进 `学术`，非学术源 → 只能进 `精选`。
- `from: websearch` → 必须给 `query`，报告里标 `⟦ws: …⟧`，让来源缺口可见而不是被暗示。
- 学术节至少要覆盖 2 个不同的学术源（当天可用 ≥2 个时），且满足 `BUCKET_QUOTA`：`arxiv-ml` ≥2、`arxiv-plse` ≤2、`arxiv-ds` ≤2。

Pick for signal, not coverage — **强日多写、弱日少写，弱日宁可 6 条也不凑数**：跨源重复（同一条同时在 HN/Lobsters/GitHub）= 最强；某源 #1 次之。**学术节按 ML 算法与优化优先挑**（`arxiv-ml`：优化算法、学习理论、RL 算法），系统工程与 PL 只作添头（≤2），算法与复杂度作拓展（≤2）；工业/社区线里低分条目落在 owner 长期盯的线（systems、compilers、math、高效模型）也值得收。

## Rolling

Runs inside `run` — nothing separate to call.

- ISO week of a daily's date decides its weekly label (`TR-W-2026-W38`); a weekly belongs to the month of its ISO week's Thursday.
- Weekly: 7 dailies in one ISO week → merge (dedupe by URL, cross-file repeats tagged `⟦YYYY-MM-DD⟧`), delete the 7 dailies + their raw files.
- 报告滚动件保留分层：被折叠的学术条目在 tail 带 `⟦学术⟧` 标记（与 `⟦YYYY-MM-DD⟧` 同族），合并后仍看得出哪条来自学术节。
- Monthly: ≥4 weeklies in one calendar month → merge, delete them. Yearly: ≥12 monthlies → merge, delete them.
- Raw merges on the same clock but keeps only the first `MERGE_RAW_CAP` (50) entries, so `archives/` cannot grow without bound; full snapshots are never kept.
- Re-merging preserves the previous merged file as the base (no loss), and the index is regenerated from the filesystem, so it never points at a deleted file.

## Failure handling

- **One source down / rate-limited / 403** → that section is written as `> [降级] 抓取失败：<reason>`, the other sources proceed, exit code stays 0, and the report carries a 降级 line. Never abort the run for one source.
- **`SEMANTIC_SCHOLAR_API_KEY` unset** → the `s2` section is written as `> [未启用] 未设置 SEMANTIC_SCHOLAR_API_KEY`（`SourceSkipped`，不是失败，exit 0）。key 只从环境变量读、只走 `x-api-key` 头，绝不写进笔记。key 设了但被拒（401/RateLimit）→ 该节降级。
- **`OPENALEX_API_KEY` unset** → only OpenAlex degrades; report it to the owner and deliver the rest. The key is read from the environment only — never written to a note, never printed (the tool redacts `api_key=` in every path it writes).
- **`ARTIFICIAL_ANALYSIS_API_KEY` unset** → the AA row reads 未启用 (not an error). Set but rejected → that board alone degrades (`HTTP 401`), other boards keep their tables. Same rule: key from env, `x-api-key` header only, never written down.
- **No network** → all sections degrade; still write the files, tell the owner it was a network failure, and do not treat the day as covered.
- **`fetch` interrupted after writing the raw list** → rerun `run`; `fetch` is safe to rerun (it overwrites and warns).

## Verify before reporting

```bash
python3 tools/trend_radar.py verify                     # 当天三层产出 + 滚动不变量
python3 tools/vault.py check                            # 结构不变量（本流程不得引入新 problem）
```

`verify` asserts: every non-降级/未启用 section meets its floor (`MIN_ITEMS` 20，openalex 10), provenance hit rate N/N, 报告两节都存在且条数落在 sanity 界内，`候选池 N / 入选 M` 一行且 N 等于原始清单正常节合计、M ≤ N, 每条 URL 都能回溯到 raw（或带 `⟦ws⟧`），学术节的 raw 条目全部来自学术源、精选节的 raw 条目全不来自学术源，学术节覆盖 ≥2 个可用学术源**且满足 ML 算法优先的配额（`arxiv-ml` ≥2 / `arxiv-plse` ≤2 / `arxiv-ds` ≤2）**, index links resolve and cover every current artifact (+ the leaderboard note), leaderboard tables each have ≥10 rows with a source line and snapshot hash, the Δ state file parses, and no ISO week holds ≥7 unmerged dailies.

`vault.py check` already fails on a **pre-existing** baseline (root-drain, legacy lit-without-source, 2 unresolved links). The requirement is only: no new finding mentioning `TR-`/`Trend Radar`.

旧契约日报（`date < LAYER_CUTOVER` = 2026-09-21）不套两节/条数/候选池/配额规则，也不要求原始清单里存在新增的 arXiv 桶或 `s2`——那时它们还不存在。**不回填历史日报**：HF trending / HN 前排这类源只能取"此刻"，补跑过去的日子只会用今天的数据污染旧日期。

## Boundaries

Write: `archives/TR-*.md` 与 `archives/TR-leaderboards.state.json`、`a_sticker/todos/Trend Radar.md`、`a_sticker/todos/Index of Todos.md`（一行登记）、`tools/trend_radar.py`、本 SKILL。

Never: `zzz_output/` contents, `.obsidian/`, `library/`, `README.md`, `AGENTS.md`, any note this flow did not create; no new zone layers (artifacts stay flat in `archives/`); no commit, no push. Deletion is limited to TR- files this flow merged away.

## Stop and ask the owner when

- A period threshold is reached but the files that would be deleted are not exclusively TR- artifacts.
- **配额与当日信号冲突**：值得看的条目只能来自被限额桶（`arxiv-plse`/`arxiv-ds`），或 `arxiv-ml` 一天凑不出 2 条可读的 —— 停下问 owner，不硬塞也不静默丢。
- The owner wants a new source, a different report size rule, a different bucket quota, or a different index location (contract change).
- OpenAlex key is missing/permission-denied and a second run also fails.
- Semantic Scholar answers 401/403 with a key set, and a second run also fails (key scope or endpoint change).
- Two consecutive runs degrade the same source for different reasons (likely a source API change, not a transient outage).
