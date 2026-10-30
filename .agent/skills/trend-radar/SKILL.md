---
name: trend-radar
description: "Daily trend radar for a geek/AI-scholar: fetch GitHub/HuggingFace/arXiv/Hacker News/Lobsters/Semantic Scholar/OpenAlex trending via API, keep the candidate pool in a /tmp snapshot (never in the vault), write a signal-sized two-layer report (精选 + 学术) with links and why-lines, roll reports up by ISO week → month → year, and index them under the todo tree. Use when the owner says 跑 trend radar / 今天的趋势 / 每日情报 / trend-radar."
---

# trend-radar

Owner-facing purpose: **每天一次调用，把该看的链接挑好并挂进 todo**，省掉自己刷榜的时间。

One call = one day. Nothing runs in the background; there is no daemon, no watcher, no cron.

## Single source of truth

Sources, academic layer, leaderboards and every threshold are listed by the tool itself:

```bash
python3 tools/trend_radar.py --help     # sources · leaderboards · thresholds · snapshot layout
python3 tools/trend_radar.py <cmd> -h   # per-command flags
```

Do not copy those lists into this file — they drift. The only thing to remember here is the shape of the flow.

## Artifacts

| Layer | Path | Nature |
|---|---|---|
| 候选池（当日快照） | `<snapshot-dir>/<date>/raw.md` + one `<sid>.raw` per source | machine-generated, zero AI rewriting, traceable to the day's API bytes; **never written into the vault, never merged, never kept** |
| 报告 | `archives/work/TR-D-<YYYY-MM-DD>.md` | two sections `## 精选` + `## 学术`; size follows the day's signal (sanity bounds in `--help`); each item = link + source + one why-line |
| 榜单快照 | `archives/work/TR-leaderboards.md` | **overwritten on every fetch**, current boards + Δ column; `TR-leaderboards.state.json` holds the previous copy to compute Δ (gitignored — Δ is per-machine, per-day) |
| 索引 | `a_sticker/todos/Trend Radar.md` | no frontmatter (tags retired); links only the artifacts that still exist |
| 滚动件 | `archives/work/TR-{W,M,Y}-*.md` | 7 dailies → weekly, ≥4 weeklies → monthly, ≥12 monthlies → yearly; **merged children are deleted, not kept** |

Tool: `tools/trend_radar.py` (stdlib only).

## Layer rules

- The academic layer is the set `--help` prints as `academic layer:`; the two report layers are **disjoint** — an item from an academic source belongs in `## 学术`, and `## 精选` never borrows one (web_search items may go in either).
- **Academic picks are ML-algorithms-first** (`BUCKET_QUOTA` in `--help`): `arxiv-ml` is the main line with a floor, the engineering and algorithms buckets are capped. When the quota fights the day's signal, stop and ask the owner — never pad the count, never silently drop a good item.
- arXiv is filtered by `cat:`, so cross-listed papers appear; the meta line carries the primary category the API returned. The same paper may land in two buckets — classify it by the `sid` it actually matched.
- `openalex` has a lower section floor than the rest (`SECTION_FLOOR` in `--help`); if a source comes in under its floor after filtering, widen the window rather than quietly lowering the threshold.

## Daily run

```bash
# 1. fetch + write the day's /tmp snapshot + print the candidate pool (your source of facts)
python3 tools/trend_radar.py fetch

# 2. read the pool, use web_search for what the APIs cannot see
#    (X/Twitter, Chinese sources, blogs, cross-source chatter), write /tmp/tr-items-<date>.json

# 3. report + rolling merge + index + self-check
python3 tools/trend_radar.py run --items /tmp/tr-items-<date>.json

# 4. report to the owner: how many items, the split, which sources, which ones to read first; then clean up
python3 tools/trend_radar.py fetch --purge
```

Rebuild a past day with `--date 2026-09-19` (`--vault` / `--snapshot-dir` work before or after the subcommand).

### items.json

```json
[{"url": "https://…", "title": "…", "source": "HF Models #1 (trendingScore 1217)",
  "from": "raw", "section": "精选", "why": "一句为什么值得看"},
 {"url": "https://…", "title": "…", "source": "OpenAlex（被引 2 · ACM TOSEM）",
  "from": "raw", "section": "学术", "why": "…"},
 {"url": "https://…", "title": "…", "source": "web_search（中文源）",
  "from": "websearch", "section": "精选", "query": "实际用过的搜索词", "why": "…"}]
```

Hard rules the tool enforces (non-zero exit, nothing written) are printed by `run -h` and stated in the failure output. In one line: size inside the sanity bounds, no duplicate URLs, `title`/`source`/`why` on every item, both sections non-empty, `from: raw` items must be verbatim in the day's snapshot, `from: websearch` items must carry their `query`, and the academic section must span ≥2 available academic sources while meeting the bucket quota.

Pick for signal, not coverage — **strong day, longer report; weak day, six items is fine, never pad**. Cross-source repetition (the same link on HN + Lobsters + GitHub) is the strongest signal; a source's #1 is next. In the academic section prefer ML algorithms and optimisation; systems/PL is a garnish, algorithms and complexity an extension. Low-score industrial items on a line the owner watches long-term (systems, compilers, math, efficient models) are still worth taking.

## Rolling

Runs inside `run` — nothing separate to call.

- A daily's ISO week decides its weekly label (`TR-W-2026-W38`); a weekly belongs to the month of its ISO week's Thursday.
- Weekly: 7 dailies in one ISO week → merge (dedupe by URL, cross-file repeats tagged `⟦YYYY-MM-DD⟧`), then delete the 7 dailies.
- Merged reports keep the layer: a folded academic item carries `⟦学术⟧` in its tail (same family as `⟦YYYY-MM-DD⟧`).
- Monthly: ≥4 weeklies in one calendar month → merge, delete them. Yearly: ≥12 monthlies → merge, delete them.
- The candidate pool lives only in `/tmp` and never merges — nothing in `archives/` can grow without bound.
- Re-merging keeps the previous merged file as the base (no loss), and the index is regenerated from the filesystem, so it never points at a deleted file.

## Failure handling

- **One source down / rate-limited / 403** → that section is written as `> [降级] 抓取失败：<reason>`, the other sources proceed, exit code stays 0, and the report carries a 降级 line. Never abort a run for one source.
- **`SEMANTIC_SCHOLAR_API_KEY` unset** → the `s2` section reads `> [未启用]` (`SourceSkipped`, not a failure, exit 0). The key is read from the environment only, sent as `x-api-key`, never written into a note.
- **`OPENALEX_API_KEY` unset** → only OpenAlex degrades; report it to the owner and deliver the rest. The key is env-only, never printed (the tool redacts `api_key=` on every path it writes).
- **`ARTIFICIAL_ANALYSIS_API_KEY` unset** → that leaderboard row reads 未启用 (not an error). Set but rejected → that board alone degrades (`HTTP 401`), the other boards keep their tables. Same rule: env only, `x-api-key` header, never written down.
- **No network** → all sections degrade; still write the files, tell the owner it was a network failure, and do not treat the day as covered.
- **`fetch` interrupted after writing the snapshot** → rerun `run`; `fetch` is safe to rerun (it overwrites and warns).

## Verify before reporting

```bash
python3 tools/trend_radar.py verify     # day's snapshot + report + index + leaderboards
python3 tools/vault.py check            # structural invariants (this flow must not add a finding)
```

`verify` asserts the day's snapshot exists and has a candidate pool, both report sections exist with sizes inside the sanity bounds, the `候选池 N / 入选 M` line matches the snapshot totals, every URL traces back to the day's snapshot (or carries `⟦ws⟧`), the academic/精选 split matches the source layers, the academic section spans ≥2 available sources and meets the bucket quota, index links resolve and cover every current artifact, every leaderboard table has ≥10 rows with a source line and a snapshot hash, the Δ state file parses, and no ISO week holds ≥7 unmerged dailies. Per-source floors and provenance hit rates are enforced by `fetch` at capture time (a short section degrades instead of failing later).

`vault.py check` under the two-tier doctrine: hard gates (root drain / material source / new dangling wikilinks) must stay clean; report-level rules give weekly increments and never block. The requirement here: no hard-gate finding, and no new finding mentioning `TR-` / `Trend Radar`.

旧契约日报（`date < LAYER_CUTOVER`，见 `--help`）不套两节/条数/候选池/配额规则。**不回填历史日报**：HF trending / HN 前排这类源只能取"此刻"，补跑过去的日子只会用今天的数据污染旧日期。

## Boundaries

Write: `archives/work/TR-*.md`（含 `TR-leaderboards.state.json`，已 gitignore）、`a_sticker/todos/Trend Radar.md`、`tools/trend_radar.py`、本 SKILL、以及 `/tmp` 快照目录。索引登记不再自动写入 `a_sticker/todos/Index of Todos.md`：`index` 只打印 `请登记: - [ ] [[Trend Radar]]`，由 owner/AI 决定是否登记。

Never: `zzz_output/` contents, `.obsidian/`, `library/`, `README.md`, `AGENTS.md`, any note this flow did not create; artifacts stay flat in `archives/work/`; no commit, no push. Deletion is limited to TR- files this flow merged away.

## Stop and ask the owner when

- A period threshold is reached but the files that would be deleted are not exclusively TR- artifacts.
- **配额与当日信号冲突**：值得看的条目只能来自被限额桶，或主偏好桶一天凑不出可读条目 —— 停下问 owner，不硬塞也不静默丢。
- The owner wants a new source, a different report size rule, a different bucket quota, or a different index location (contract change).
- OpenAlex key is missing/permission-denied and a second run also fails.
- Semantic Scholar answers 401/403 with a key set, and a second run also fails (key scope or endpoint change).
- Two consecutive runs degrade the same source for different reasons (likely a source API change, not a transient outage).
