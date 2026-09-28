#!/usr/bin/env python3
"""Trend Radar — daily trending fetch → archive → curated report → rolling merge.

Daily flow (see .agent/skills/trend-radar/SKILL.md):

    python3 tools/trend_radar.py fetch                  # 抓取 + 写原始清单 + 打印候选池
    python3 tools/trend_radar.py run --items items.json # 写精选报告 + 滚动合并 + 更新索引 + 校验
    python3 tools/trend_radar.py verify                 # 离线复核当天三层产出
    python3 tools/trend_radar.py fetch --purge          # 删掉 /tmp 快照

Artifacts (all under archives/, flat, no new zone layers):

    TR-raw-D-YYYY-MM-DD.md  原始清单（零 AI 改写，逐条可回溯到 API 快照）
    TR-D-YYYY-MM-DD.md      当日报告：精选 + 学术两节，条数随当日信号浮动
    TR-W-<ISOyear>-W<week>.md / TR-M-YYYY-MM.md / TR-Y-YYYY.md   滚动合并件
    a_sticker/todos/Trend Radar.md   索引（只链当前仍在的件）

Academic layer: hf-papers / arxiv (cs.AI·LG·CL) / arxiv-ml (stat.ML·math.OC·cs.NA) /
arxiv-plse (cs.SE·PL·AR·OS) / arxiv-ds (cs.DS·CG·CC) / s2 / openalex.
The two report layers are disjoint: a pick from an academic source belongs to 学术, never to 精选.
Academic picks are ML-algorithms-first: BUCKET_QUOTA caps the engineering and algorithms buckets.

Rolling: 7 日报 → 周报；自然月内 ≥4 周报 → 月报；年 ≥12 月报 → 年报。被合并件删除。
Raw merges on the same clock, capped per section (MERGE_RAW_CAP) so the archive stays bounded.

Stdlib only. Vault root = parent of tools/ (override with --vault for sandbox runs).
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MIN_ITEMS = 20          # default per section floor in the raw list
SECTION_FLOOR = {"openalex": 10}   # sections whose source is narrower than MIN_ITEMS
OPENALEX_WINDOW = 7     # days back for the OpenAlex citation-velocity window
S2_WINDOW = 7           # days back for the Semantic Scholar publication window
GITHUB_WINDOW = 7       # days back for "new repositories" window
MERGE_RAW_CAP = 50      # per-section cap inside merged raw files

# Report size is adaptive — the day decides. These are sanity bounds, not targets.
REPORT_MIN, REPORT_MAX = 4, 24
# Academic layer + floating size landed on this date; dailies before it keep the old
# contract (single 精选 section, 8–12 items) and are verified for provenance only.
LAYER_CUTOVER = date(2026, 9, 21)
# Sources that feed the report's 学术 section (curated 精选 may not borrow from them,
# and academic items may not borrow outside them — keeping the two layers disjoint).
ACADEMIC_SIDS = ("hf-papers", "arxiv", "arxiv-ml", "arxiv-plse", "arxiv-ds", "s2", "openalex")
ARXIV_AI_CATS = ("cs.AI", "cs.LG", "cs.CL")
ARXIV_ML_CATS = ("stat.ML", "math.OC", "cs.NA")          # 主偏好：ML 算法与优化
ARXIV_PLSE_CATS = ("cs.SE", "cs.PL", "cs.AR", "cs.OS")   # 添头：工程向
ARXIV_DS_CATS = ("cs.DS", "cs.CG", "cs.CC")              # 拓展：算法与复杂度
ARXIV_MAX = 40
# Report-level bias, enforced by cmd_report and verify: the academic section is
# ML-algorithms-first, with the engineering bucket and the algorithms bucket capped.
BUCKET_QUOTA = {"arxiv-ml": ("min", 2), "arxiv-plse": ("max", 2), "arxiv-ds": ("max", 2)}
S2_FIELDS = ("title,venue,publicationDate,citationCount,influentialCitationCount,"
             "externalIds,fieldsOfStudy")
INDEX_NAME = "Trend Radar"
INDEX_REL = Path("a_sticker/todos") / f"{INDEX_NAME}.md"
TODOS_INDEX_REL = Path("a_sticker/todos/Index of Todos.md")
TEMPLATES = ("template/", "a_sticker/todos/")
UA = {"User-Agent": "trend-radar/1.0 (obsidian vault archive; +krummholz)"}

# section id → (label, fetch function)
SOURCES = []


def source(sid, label):
    def deco(fn):
        SOURCES.append((sid, label, fn))
        return fn
    return deco


# ---------------------------------------------------------------- http


def http_get(url: str, timeout: int = 45, tries: int = 3, headers=None) -> bytes:
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={**UA, **(headers or {})})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except Exception as exc:                      # noqa: BLE001 — retried below
            last = exc
            if attempt + 1 < tries:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{type(last).__name__}: {last}")


def json_get(url: str):
    raw = http_get(url)
    return json.loads(raw.decode("utf-8", "replace")), raw


class SourceSkipped(RuntimeError):
    """Source is intentionally not enabled (missing credential) — not a failure."""


def item(url, prov, title, meta, score=None, when=None):
    return {"url": url, "prov": prov, "title": " ".join(str(title).split()),
            "meta": meta, "score": score, "when": when}


def url_tail(value: str) -> str:
    return str(value).strip().rstrip("/").split("/")[-1]


# ---------------------------------------------------------------- sources


@source("hf-models", "HuggingFace Models（trendingScore 降序）")
def fetch_hf_models(day):
    api = "https://huggingface.co/api/models?sort=trendingScore&direction=-1&limit=25"
    data, raw = json_get(api)
    items = [item(f"https://huggingface.co/{m['id']}", m["id"], m["id"],
                  f"trendingScore {m.get('trendingScore')} · likes {m.get('likes')} · "
                  f"downloads {m.get('downloads')} · {str(m.get('createdAt'))[:10]}",
                  m.get("trendingScore"), str(m.get("createdAt"))[:10])
             for m in data if m.get("id")]
    return items, raw, api


@source("hf-datasets", "HuggingFace Datasets（trendingScore 降序）")
def fetch_hf_datasets(day):
    api = "https://huggingface.co/api/datasets?sort=trendingScore&direction=-1&limit=25"
    data, raw = json_get(api)
    items = [item(f"https://huggingface.co/datasets/{d['id']}", d["id"], d["id"],
                  f"trendingScore {d.get('trendingScore')} · likes {d.get('likes')} · "
                  f"downloads {d.get('downloads')} · {str(d.get('createdAt'))[:10]}",
                  d.get("trendingScore"), str(d.get("createdAt"))[:10])
             for d in data if d.get("id")]
    return items, raw, api


@source("hf-spaces", "HuggingFace Spaces（trendingScore 降序）")
def fetch_hf_spaces(day):
    api = "https://huggingface.co/api/spaces?sort=trendingScore&direction=-1&limit=25"
    data, raw = json_get(api)
    items = [item(f"https://huggingface.co/spaces/{s['id']}", s["id"], s["id"],
                  f"trendingScore {s.get('trendingScore')} · likes {s.get('likes')} · "
                  f"{str(s.get('createdAt'))[:10]}",
                  s.get("trendingScore"), str(s.get("createdAt"))[:10])
             for s in data if s.get("id")]
    return items, raw, api


@source("hf-papers", "HuggingFace Daily Papers（当日精选，按 upvotes）")
def fetch_hf_papers(day):
    api = "https://huggingface.co/api/daily_papers?limit=30"
    data, raw = json_get(api)
    out = []
    for entry in data:
        paper = entry.get("paper") or {}
        pid = paper.get("id")
        if not pid:
            continue
        out.append(item(f"https://huggingface.co/papers/{pid}", pid,
                        paper.get("title") or entry.get("title") or pid,
                        f"upvotes {paper.get('upvotes')} · {paper.get('submittedOnDailyAt', '')[:10]} · arXiv {pid}",
                        paper.get("upvotes"), str(paper.get("submittedOnDailyAt"))[:10]))
    out.sort(key=lambda i: i["score"] or 0, reverse=True)
    return out, raw, api


def arxiv_fetch(day, cats):
    api = ("https://export.arxiv.org/api/query?search_query="
           + "+OR+".join(f"cat:{c}" for c in cats)
           + f"&sortBy=submittedDate&sortOrder=descending&max_results={ARXIV_MAX}")
    raw = http_get(api)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(raw)
    out = []
    for entry in root.findall("a:entry", ns):
        raw_id = (entry.findtext("a:id", default="", namespaces=ns) or "").strip()
        aid = url_tail(raw_id).split("v")[0]
        if not aid:
            continue
        primary = entry.find("{http://arxiv.org/schemas/atom}primary_category")
        cats = [c.get("term") for c in entry.findall("a:category", ns)]
        title = " ".join((entry.findtext("a:title", default="", namespaces=ns) or "").split())
        published = entry.findtext("a:published", default="", namespaces=ns) or ""
        out.append(item(f"https://arxiv.org/abs/{aid}", f"/abs/{aid}", title,
                        f"{(primary.get('term') if primary is not None else cats[0] if cats else '?')} · "
                        f"{published[:16].replace('T', ' ')}Z · arXiv:{aid}",
                        None, published[:10]))
    return out, raw, api


@source("arxiv", f"arXiv {' | '.join(ARXIV_AI_CATS)}（按提交时间倒序）")
def fetch_arxiv(day):
    return arxiv_fetch(day, ARXIV_AI_CATS)


@source("arxiv-ml", f"arXiv {' | '.join(ARXIV_ML_CATS)}（ML 算法与优化，按提交时间倒序）")
def fetch_arxiv_ml(day):
    return arxiv_fetch(day, ARXIV_ML_CATS)


@source("arxiv-plse", f"arXiv {' | '.join(ARXIV_PLSE_CATS)}（工程向添头，按提交时间倒序）")
def fetch_arxiv_plse(day):
    return arxiv_fetch(day, ARXIV_PLSE_CATS)


@source("arxiv-ds", f"arXiv {' | '.join(ARXIV_DS_CATS)}（算法与复杂度拓展，按提交时间倒序）")
def fetch_arxiv_ds(day):
    return arxiv_fetch(day, ARXIV_DS_CATS)


@source("s2", f"Semantic Scholar 近 {S2_WINDOW} 天 CS 论文（被引降序）")
def fetch_s2(day):
    """Keyed (x-api-key); unset key → 未启用 section, never a failure."""
    key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "").strip()
    if not key:
        raise SourceSkipped("未设置 SEMANTIC_SCHOLAR_API_KEY")
    since = day - timedelta(days=S2_WINDOW)
    api = ("https://api.semanticscholar.org/graph/v1/paper/search/bulk"
           "?query=*&fieldsOfStudy=Computer%20Science"
           f"&publicationDateOrYear={since.isoformat()}:"
           "&sort=citationCount:desc"
           f"&fields={S2_FIELDS}")
    raw = http_get(api, headers={"x-api-key": key})
    data = json.loads(raw.decode("utf-8", "replace"))
    out = []
    for paper in data.get("data", []):
        title = str(paper.get("title") or "").strip()
        pid = paper.get("paperId")
        if not title or not pid:
            continue
        ext = paper.get("externalIds") or {}
        arxiv_id, doi = ext.get("ArXiv"), ext.get("DOI")
        if arxiv_id:
            url, prov = f"https://arxiv.org/abs/{arxiv_id}", arxiv_id
        elif doi:
            url, prov = f"https://doi.org/{doi}", doi
        else:
            url, prov = f"https://www.semanticscholar.org/paper/{pid}", pid
        pub = str(paper.get("publicationDate") or "")
        out.append(item(url, prov, title,
                        f"被引 {paper.get('citationCount')} · 影响力引用 "
                        f"{paper.get('influentialCitationCount')} · {pub} · "
                        f"{paper.get('venue') or 'n/a'}",
                        paper.get("citationCount"), pub))
    if not out:
        raise RuntimeError("响应里没有可用的论文行（字段名可能已改，见快照）")
    return out[:25], raw, api


@source("openalex", f"OpenAlex 近 {OPENALEX_WINDOW} 天高被引 CS 论文（期刊/会议，被引降序）")
def fetch_openalex(day):
    key = os.environ.get("OPENALEX_API_KEY", "").strip()
    if not key:
        raise RuntimeError("环境变量 OPENALEX_API_KEY 未设置")
    since = day - timedelta(days=OPENALEX_WINDOW)
    api = ("https://api.openalex.org/works?filter="
           f"from_publication_date:{since.isoformat()},to_publication_date:{day.isoformat()},"
           "type:article,has_abstract:true,"
           "primary_location.source.type:journal|conference,"
           "primary_topic.field.id:fields/17"
           "&sort=cited_by_count:desc&per-page=200"
           f"&api_key={key}")
    data, raw = json_get(api)
    out, seen = [], set()
    for work in data.get("results", []):
        if not work.get("authorships") or not work.get("title"):
            continue
        doi = work.get("doi") or ""
        prov = doi or work.get("id") or ""
        key_ = (doi or work.get("id") or "").lower()
        title_key = re.sub(r"[^a-z0-9]", "", work["title"].lower())[:80]
        if key_ in seen or title_key in seen:
            continue
        seen.update({key_, title_key})
        source = ((work.get("primary_location") or {}).get("source") or {})
        venue = source.get("display_name")
        kind = source.get("type")
        out.append(item(doi or work["id"], prov, work["title"],
                        f"被引 {work.get('cited_by_count')} · {work.get('publication_date')} · "
                        f"{venue or 'n/a'}{f'（{kind}）' if kind else ''}",
                        work.get("cited_by_count"), work.get("publication_date")))
    return out[:25], raw, api


@source("hackernews", "Hacker News Front Page（points 降序）")
def fetch_hackernews(day):
    api = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30"
    data, raw = json_get(api)
    out = []
    for hit in data.get("hits", []):
        oid = hit.get("objectID")
        url = hit.get("url") or f"https://news.ycombinator.com/item?id={oid}"
        out.append(item(url, url if hit.get("url") else f"item?id={oid}",
                        hit.get("title") or "(untitled)",
                        f"{hit.get('points')} points · {hit.get('num_comments')} comments · "
                        f"{str(hit.get('created_at'))[:10]} · https://news.ycombinator.com/item?id={oid}",
                        hit.get("points"), str(hit.get("created_at"))[:10]))
    out.sort(key=lambda i: i["score"] or 0, reverse=True)
    return out, raw, api


@source("lobsters", "Lobsters Hottest（score 降序）")
def fetch_lobsters(day):
    api = "https://lobste.rs/hottest.json"
    raw = http_get(api)
    data = json.loads(raw.decode("utf-8", "replace"))
    out, seen = [], set()
    for story in data:
        url = story.get("url") or story.get("short_id_url")
        if not url or url in seen:
            continue
        seen.add(url)
        out.append(item(url, url, story.get("title") or url_tail(url),
                        f"score {story.get('score')} · {story.get('comment_count')} comments · "
                        f"{str(story.get('created_at'))[:10]} · {story.get('short_id_url')}",
                        story.get("score"), str(story.get("created_at"))[:10]))
    if len(out) < MIN_ITEMS:                      # hottest caps at 25; top up from active
        extra_raw = http_get("https://lobste.rs/active.json")
        raw = raw + b"\n" + extra_raw
        for story in json.loads(extra_raw.decode("utf-8", "replace")):
            url = story.get("url") or story.get("short_id_url")
            if not url or url in seen:
                continue
            seen.add(url)
            out.append(item(url, url, story.get("title") or url_tail(url),
                            f"score {story.get('score')} · {story.get('comment_count')} comments · "
                            f"{str(story.get('created_at'))[:10]} · {story.get('short_id_url')} (active)",
                            story.get("score"), str(story.get("created_at"))[:10]))
    out.sort(key=lambda i: i["score"] or 0, reverse=True)
    return out, raw, api


@source("github", f"GitHub 新建仓库（{GITHUB_WINDOW} 天窗口，stars 降序）")
def fetch_github(day):
    since = day - timedelta(days=GITHUB_WINDOW)
    api = (f"https://api.github.com/search/repositories?q=created:%3E{since.isoformat()}"
           f"+stars:%3E50&sort=stars&order=desc&per_page=30")
    data, raw = json_get(api)
    out = []
    for repo in data.get("items", []):
        name = repo.get("full_name")
        html = repo.get("html_url")
        if not (name and html):
            continue
        out.append(item(html, html, name,
                        f"★{repo.get('stargazers_count')} · {repo.get('language') or 'n/a'} · "
                        f"created {str(repo.get('created_at'))[:10]} · "
                        f"{(repo.get('description') or '')[:110]}",
                        repo.get("stargazers_count"), str(repo.get("created_at"))[:10]))
    return out, raw, api


# ---------------------------------------------------------------- provenance


def provenance_check(sid, items, raw_bytes):
    """Keep only items whose source-side field appears verbatim in the API bytes."""
    kept, dropped = [], []
    for it in items:
        if it["prov"] and it["prov"].encode("utf-8") in raw_bytes:
            kept.append(it)
        else:
            dropped.append(it)
    return kept, dropped


def snapshot_dir(date_str: str, override: Path | None = None) -> Path:
    base = override or Path("/tmp/trend-radar")
    return base / date_str


# ---------------------------------------------------------------- frontmatter / markdown


def md_link(title: str, url: str) -> str:
    text = str(title).replace("\\", "").replace("[", "(").replace("]", ")")
    dest = str(url).replace(" ", "%20")
    if "(" in dest or ")" in dest:
        dest = f"<{dest}>"
    return f"[{text}]({dest})"


def fm_block(lines) -> str:
    return "---\n" + "".join(f"{line}\n" for line in lines) + "---\n"


def section_header(sid: str, label: str, count: int, degraded: str | None,
                   skipped: bool = False) -> str:
    head = f"\n## {sid} — {label}\n"
    if skipped:
        return head + f"\n> [未启用] {degraded}\n"
    if degraded:
        return head + f"\n> [降级] 抓取失败：{degraded}\n"
    return head + f"\n> 共 {count} 条\n"


def iso_week(d: date):
    y, w, _ = d.isocalendar()
    return y, w


def week_label(d: date) -> str:
    y, w = iso_week(d)
    return f"{y}-W{w:02d}"


def week_month(d: date) -> str:
    """Month a weekly file belongs to = month of its ISO week's Thursday."""
    y, w = iso_week(d)
    thursday = date.fromisocalendar(y, w, 4)
    return f"{thursday.year:04d}-{thursday.month:02d}"


# ---------------------------------------------------------------- leaderboards
#
# A leaderboard is a *snapshot*, not a link stream: it is overwritten daily into
# one note and never merged (merged TR-{D,W,M,Y}-* globs do not match it).
# Δ is computed against the previous snapshot kept in LB_STATE_REL.
#
# Arena AI (formerly LMSYS Chatbot Arena) has no public API (lmarena.ai/api → 403),
# so its numbers come through a third-party daily mirror (MIT). The official page
# is recorded as source_url in every table header; the mirror is named as such.

LB_NOTE_REL = Path("archives/TR-leaderboards.md")
LB_STATE_REL = Path("archives/TR-leaderboards.state.json")
LB_TOP = 10
ARENA_MIRROR = ("https://raw.githubusercontent.com/oolong-tea-2026/"
                "arena-ai-leaderboards/main/data")
SWEBENCH_JSON = ("https://raw.githubusercontent.com/swe-bench/swe-bench.github.io/"
                 "master/data/leaderboards.json")

LEADERBOARDS = []


def leaderboard(bid, label, name_col, vendor_col, score_col, note_col):
    def deco(fn):
        LEADERBOARDS.append({"id": bid, "label": label, "name": name_col,
                             "vendor": vendor_col, "score": score_col,
                             "note": note_col, "fn": fn})
        return fn
    return deco


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def lb_arena(category: str, day: date):
    """Arena AI snapshot via the daily mirror; falls back to its `latest` pointer."""
    failures = []
    for stamp in (day.isoformat(), None):
        if stamp is None:
            pointer, _raw = json_get(f"{ARENA_MIRROR}/latest.json")
            stamp = str(pointer.get("path", "")).rstrip("/").split("/")[-1]
            if not stamp:
                raise RuntimeError("镜像 latest.json 未给出快照目录")
        url = f"{ARENA_MIRROR}/{stamp}/{category}.json"
        try:
            data, raw = json_get(url)
        except Exception as exc:                      # noqa: BLE001 — try the pointer
            failures.append(f"{stamp}: {type(exc).__name__}: {exc}")
            continue
        rows = []
        for m in data.get("models", []):
            name = str(m.get("model") or "").strip()
            if not name:
                continue
            note = " · ".join(str(x) for x in (m.get("votes"), m.get("license")) if x)
            rows.append({"name": name, "vendor": m.get("vendor"),
                         "score": m.get("score"), "note": note})
        if not rows:
            raise RuntimeError(f"{url} 无模型行")
        meta = data.get("meta") or {}
        return rows, {"url": url, "raw": raw, "items": len(rows),
                      "source_url": meta.get("source_url") or "https://arena.ai/leaderboard",
                      "upstream_updated": meta.get("last_updated"),
                      "snapshot": stamp, "fetched_at": meta.get("fetched_at") or _utcnow()}
    raise RuntimeError("；".join(failures))


@leaderboard("arena-text", "Arena AI 文本榜（Chatbot Arena）", "模型", "厂商", "Elo", "票数 · 许可")
def fetch_lb_arena_text(day):
    return lb_arena("text", day)


@leaderboard("arena-code", "Arena AI 代码榜", "模型", "厂商", "Elo", "票数 · 许可")
def fetch_lb_arena_code(day):
    return lb_arena("code", day)


@leaderboard("swebench-verified", "SWE-bench Verified（官方榜单）", "Agent / 模型",
             "组织", "%Resolved", "提交日期 · 版本")
def fetch_lb_swebench(day):
    data, raw = json_get(SWEBENCH_JSON)
    board = next((b for b in data.get("leaderboards", []) if b.get("name") == "Verified"), None)
    if board is None:
        raise RuntimeError("leaderboards.json 中没有 Verified 榜")
    seen, rows = set(), []
    for r in sorted(board.get("results", []), key=lambda x: -(x.get("resolved") or 0)):
        name = " ".join(str(r.get("name") or "").split())
        if not name or name in seen:
            continue
        seen.add(name)
        note = " · ".join(str(x) for x in (r.get("date"), r.get("agent_org")) if x)
        rows.append({"name": name, "vendor": r.get("model_org") or r.get("agent_org"),
                     "score": r.get("resolved"), "note": note})
    if not rows:
        raise RuntimeError("Verified 榜无条目")
    return rows, {"url": SWEBENCH_JSON, "raw": raw, "items": len(rows),
                  "source_url": "https://www.swebench.com/", "snapshot": "官方仓库 main",
                  "fetched_at": _utcnow()}


@leaderboard("artificial-analysis", "Artificial Analysis Intelligence Index", "模型",
             "厂商", "Intelligence", "Coding / Agentic · 价格 · 速度")
def fetch_lb_aa(day):
    """Needs ARTIFICIAL_ANALYSIS_API_KEY (free tier covers headline indices).

    Real shape (2026-09, API v2): {status, prompt_options, data:[{name, slug,
    model_creator{name}, evaluations{artificial_analysis_{intelligence,coding,
    math}_index, ...}, pricing{price_1m_blended_3_to_1}, median_output_tokens_per_second}]}.
    Variants of one model (effort / fallback settings) collapse into one row — the best
    config wins — so the board reads as "which model is first", not "which config".
    """
    key = os.environ.get("ARTIFICIAL_ANALYSIS_API_KEY", "").strip()
    if not key:
        return None, {"skipped": "未启用：未设置 ARTIFICIAL_ANALYSIS_API_KEY"}
    url = "https://artificialanalysis.ai/api/v2/data/llms/models"
    raw = http_get(url, headers={"x-api-key": key}, timeout=90)
    data = json.loads(raw.decode("utf-8", "replace"))
    items = data.get("data") if isinstance(data, dict) else data
    best = {}
    for m in items or []:
        evals = m.get("evaluations") or {}
        index = {}
        for name, value in evals.items():
            if not isinstance(value, (int, float)):
                continue
            for label in ("intelligence", "coding", "agentic", "math"):
                if label in name.lower():
                    index.setdefault(label, value)
        name, slug = m.get("name"), m.get("slug") or m.get("id")
        score = index.get("intelligence")
        if score is None or not (name and slug):
            continue
        base = re.sub(r"\s*\([^)]*\)", "", str(name)).strip() or str(name)
        vendor = (m.get("model_creator") or {}).get("name")
        pricing = m.get("pricing") or {}
        price = pricing.get("price_1m_blended_3_to_1")
        if not isinstance(price, (int, float)):
            price = next((v for k, v in pricing.items() if isinstance(v, (int, float))), None)
        speed = m.get("median_output_tokens_per_second")
        note = " · ".join(str(x) for x in
                          (f"Coding {num(index['coding'])}" if "coding" in index else None,
                           f"Agentic {num(index['agentic'])}" if "agentic" in index else None,
                           f"${num(price)}/Mtok" if isinstance(price, (int, float)) else None,
                           f"{num(speed)} tok/s" if isinstance(speed, (int, float)) else None) if x)
        row = {"name": base, "vendor": vendor, "score": score, "note": note}
        key_ = f"{(vendor or '').lower()}|{base.lower()}"
        if key_ not in best or score > best[key_]["score"]:
            best[key_] = row
    rows = sorted(best.values(), key=lambda r: -(r["score"] or 0))
    if not rows:
        raise RuntimeError("响应里没有可解析的 intelligence 指数（字段名可能已改，见快照）")
    return rows, {"url": url, "raw": raw, "items": len(rows),
                  "source_url": "https://artificialanalysis.ai/leaderboards/models",
                  "snapshot": "官方 API v2（keyed，同模型多变体取最优）", "fetched_at": _utcnow()}


def load_lb_state(root: Path) -> dict:
    path = root / LB_STATE_REL
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}


def delta_marks(prev: dict, rank: int, score):
    """(rank mark, score mark) versus the previous snapshot."""
    if not prev:
        return "NEW", "—"
    prank, pscore = prev.get("rank"), prev.get("score")
    rank_mark = "—" if prank == rank else (f"▲{prank - rank}" if prank > rank else f"▼{rank - prank}")
    if isinstance(score, (int, float)) and isinstance(pscore, (int, float)):
        diff = round(score - pscore, 2)
        score_mark = "—" if abs(diff) < 1e-9 else (f"+{diff:g}" if diff > 0 else f"{diff:g}")
    else:
        score_mark = "—"
    return rank_mark, score_mark


def cell(value) -> str:
    return " ".join(str(value if value not in (None, "") else "—").split()).replace("|", "/")


def num(value) -> str:
    """Trim float noise: 1506.0 -> 1506, 79.20 -> 79.2."""
    if isinstance(value, bool) or value is None:
        return "—"
    if isinstance(value, float):
        return str(int(value)) if value.is_integer() else f"{value:g}"
    return str(value)


def short_time(stamp) -> str:
    return re.sub(r"\.\d+", "", str(stamp or "")).replace("+00:00", "Z")


def write_leaderboard_note(root: Path, day: date, results, sna: Path):
    """results: [(spec, rows|None, meta)] — writes the snapshot note and advances state."""
    date_str = day.isoformat()
    state = load_lb_state(root)
    prev_boards = state.get("boards") or {}
    same_day = state.get("date") == date_str
    degraded, skipped = [], []
    body = [f"\n# Trend Radar 榜单 {date_str}\n\n",
            "> 每次抓取整体覆盖，只保留当前快照；变化由 Δ 列给出（对比上一份快照）。\n",
            "> Arena AI（原 LMArena）无公开 API，数据经非官方每日镜像（MIT 许可）；"
            "官方口径以表头 `来源` 为准。SWE-bench 取官方仓库 JSON。\n"]
    new_state = {"date": state.get("date") if same_day else date_str, "boards": dict(prev_boards)}
    source_lines = []
    for spec, rows, meta in results:
        bid = spec["id"]
        if rows is None:
            reason = meta.get("skipped") or meta.get("error") or "未知原因"
            (skipped if meta.get("skipped") else degraded).append(f"{bid}：{reason}")
            body.append(f"\n## {bid} — {spec['label']}\n\n> [{'未启用' if meta.get('skipped') else '降级'}]"
                        f" {reason}\n")
            source_lines.append(f'  - "{spec["label"]}：{reason}"')
            continue
        snapshot = sna / f"lb-{bid}.raw"
        digest = hashlib.sha256(meta["raw"]).hexdigest()[:12]
        snapshot.write_bytes(meta["raw"])
        head = " · ".join(str(x) for x in (meta.get("source_url"), meta.get("snapshot"),
                                           short_time(meta.get("fetched_at"))) if x)
        body.append(f"\n## {bid} — {spec['label']}\n\n"
                    f"> 来源 {head} · 共 {meta['items']} 条，此处列前 {LB_TOP}"
                    + (f" · 上游更新 {meta['upstream_updated']}" if meta.get("upstream_updated") else "")
                    + f" · 快照 sha256 {digest}\n\n")
        body.append(f"| # | Δ | {spec['name']} | {spec['vendor']} | {spec['score']} | "
                    f"Δ{spec['score']} | {spec['note']} |\n")
        body.append("|---|----|------|------|------|------|------|\n")
        prev_board = prev_boards.get(bid) or {}
        for rank, row in enumerate(rows, 1):
            if rank > LB_TOP:
                break
            rank_mark, score_mark = delta_marks(prev_board.get(row["name"]), rank, row["score"])
            body.append(f"| {rank} | {rank_mark} | {cell(row['name'])} | {cell(row['vendor'])} | "
                        f"{num(row['score'])} | {score_mark} | {cell(row['note'])} |\n")
        source_lines.append(
            f'  - "{spec["label"]}：{meta.get("source_url")}（{meta["items"]} 条，'
            f'{short_time(meta.get("fetched_at"))}，快照 sha256 {digest}）"')
        new_state["boards"][bid] = {r["name"]: {"rank": i + 1, "score": r["score"]}
                                    for i, r in enumerate(rows)}
    body.append("\n---\n## Related\n\n")
    body += related_links(root, exclude=("TR-leaderboards",))
    fm = fm_block(["tags:", "  - type/permanent", "  - status/archive", "  - topic/ai",
                   f"created: {date_str}", f"data-date: {date_str}", "source:", *source_lines])
    path = root / LB_NOTE_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(fm + "".join(body), encoding="utf-8")
    state_path = root / LB_STATE_REL
    if same_day:
        # Re-run on the same day: keep the earlier values (so Δ stays day-over-day) but
        # record boards that were not in the snapshot before, so they get a baseline.
        for bid, board in new_state["boards"].items():
            prev_boards.setdefault(bid, board)
        new_state["boards"] = prev_boards
    state_path.write_text(json.dumps(new_state, ensure_ascii=False, indent=1), encoding="utf-8")
    return path, degraded, skipped, len(results)


def fetch_leaderboards(root: Path, day: date, sna: Path):
    results = []
    for spec in LEADERBOARDS:
        try:
            rows, meta = spec["fn"](day)
            results.append((spec, rows, meta))
        except Exception as exc:                      # noqa: BLE001 — degrade one board
            results.append((spec, None, {"error": f"{type(exc).__name__}: {exc}"}))
    path, degraded, skipped, total = write_leaderboard_note(root, day, results, sna)
    print(f"写入 {path.relative_to(root)}（{total} 个榜："
          f"{total - len(degraded) - len(skipped)} 正常 / {len(degraded)} 降级 / {len(skipped)} 未启用）")
    for spec, rows, meta in results:
        if rows:
            top = "，".join(f"{r['name']} {r['score']}" for r in rows[:3])
            print(f"  {spec['id']}: {top}")
        else:
            print(f"  {spec['id']}: {meta.get('skipped') or meta.get('error')}")
    return results


# ---------------------------------------------------------------- fetch


def redact(url: str) -> str:
    """Never let a credential reach disk or stdout."""
    return re.sub(r"(api_key=)[^&\s]+", r"\1***", url)


def write_raw_note(root: Path, day: date, payload, sna: Path):
    """payload: {sid: (items, raw_bytes, api, error, skipped)}"""
    date_str = day.isoformat()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    source_lines = [f'  - "原始清单 {date_str}：机器生成，零 AI 改写"']
    hashes, degraded, skipped, hits, total = {}, [], [], 0, 0
    body = [f"\n# Trend Radar Raw {date_str}\n",
            "\n> 机器生成，零 AI 改写；每条 = 源侧返回字段的原样映射（标题/分数/时间戳取自响应）。\n",
            f"> 抓取时间 {now}；快照 {sna}/（`fetch --purge` 清理）。\n",
            "> 校验方式：每条 URL 的源侧原样字段必须出现在该源快照字节流中，命中率见文末 Provenance。\n"]
    for sid, label, _fn in SOURCES:
        items, raw_bytes, api, err, skip = payload[sid]
        if err:
            (skipped if skip else degraded).append(f"{sid}（{err}）")
            body.append(section_header(sid, label, 0, err, skip))
            source_lines.append(f'  - "{label}：{err}"')
            continue
        hashes[sid] = hashlib.sha256(raw_bytes).hexdigest()[:12]
        hits += len(items)
        total += len(items)
        source_lines.append(f'  - "{label}：{redact(api)}（{len(items)} 条，{now}）"')
        body.append(section_header(sid, label, len(items), None))
        for it in items:
            body.append(f"- {md_link(it['title'], it['url'])} — {it['meta']}\n")
    body.append("\n## Provenance\n")
    body.append(f"- 抓取时间：{now}\n")
    body.append(f"- URL 命中：{hits}/{total}（源侧原样字段在快照字节流中命中）\n")
    body.append(f"- 降级源：{'、'.join(degraded) if degraded else '无'}\n")
    body.append(f"- 未启用源：{'、'.join(skipped) if skipped else '无'}\n")
    if hashes:
        body.append("- 快照 sha256 前 12 位：" +
                    "，".join(f"{sid} {h}" for sid, h in hashes.items()) + "\n")
    counts = {sid: len(payload[sid][0]) for sid, _l, _f in SOURCES if not payload[sid][3]}
    body.append("- 各节条目数：" +
                "，".join(f"{sid} {n}" for sid, n in counts.items()) + "\n")
    fm = fm_block([f"tags:", "  - type/lit", "  - status/archive", "  - topic/ai",
                   f"created: {date_str}", f"data-date: {date_str}", "source:"] + source_lines)
    text = fm + "".join(body)
    path = root / "archives" / f"TR-raw-D-{date_str}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    existed = path.exists()
    path.write_text(text, encoding="utf-8")
    return path, existed, len(text)


def cmd_fetch(args) -> int:
    root = Path(args.vault).resolve()
    day = args.date
    payload, pooled = {}, []
    for sid, label, fn in SOURCES:
        floor = SECTION_FLOOR.get(sid, MIN_ITEMS)
        try:
            items, raw_bytes, api = fn(day)
            kept, dropped = provenance_check(sid, items, raw_bytes)
            if len(kept) < floor:
                err = (f"仅 {len(kept)} 条通过快照校验（阈值 {floor}）"
                       + (f"，{len(dropped)} 条未命中快照" if dropped else ""))
                payload[sid] = ([], raw_bytes, api, err, False)
                pooled.append((sid, label, [], err, dropped, False))
                continue
            payload[sid] = (kept, raw_bytes, api, None, False)
            pooled.append((sid, label, kept, None, dropped, False))
        except SourceSkipped as exc:
            payload[sid] = ([], b"", "", str(exc), True)
            pooled.append((sid, label, [], str(exc), [], True))
        except Exception as exc:                      # noqa: BLE001 — degrade, never abort
            msg = f"{type(exc).__name__}: {exc}"
            payload[sid] = ([], b"", "", msg, False)
            pooled.append((sid, label, [], msg, [], False))
    if args.purge:
        purge_snapshots(snapshot_dir(day.isoformat(), Path(args.snapshot_dir) if args.snapshot_dir else None))
        return 0
    sna = snapshot_dir(day.isoformat(), Path(args.snapshot_dir) if args.snapshot_dir else None)
    sna.mkdir(parents=True, exist_ok=True)
    for sid, _l, _f in SOURCES:
        items, raw_bytes, _api, err, _skip = payload[sid]
        if not err and raw_bytes:
            (sna / f"{sid}.raw").write_bytes(raw_bytes)
    path, existed, size = write_raw_note(root, day, payload, sna)
    print(f"{'重写' if existed else '写入'} {path.relative_to(root)}（{size} B）")
    fetch_leaderboards(root, day, sna)
    print(f"快照目录 {sna}")
    ok = sum(1 for sid, _l, _f in SOURCES if not payload[sid][3])
    skipped_n = sum(1 for sid, _l, _f in SOURCES if payload[sid][4])
    print(f"源 {ok}/{len(SOURCES)} 正常"
          + (f"（{skipped_n} 未启用）" if skipped_n else "") + "\n")
    print("# 候选池（用于人工/AI 挑选，非最终报告）\n")
    for sid, label, items, err, dropped, skip in pooled:
        print(f"## {sid} — {label}")
        if err:
            print(f"  [{'未启用' if skip else '降级'}] {err}")
            continue
        for it in items[:20]:
            print(f"  [{it['score']}] {it['title']} — {it['url']}")
        if dropped:
            print(f"  （{len(dropped)} 条未通过快照校验，已剔除）")
        print()
    return 0


def purge_snapshots(sna: Path) -> None:
    if not sna.exists():
        print(f"快照目录不存在：{sna}")
        return
    for child in sna.glob("*"):
        child.unlink()
    sna.rmdir()
    print(f"已删除快照目录 {sna}")


# ---------------------------------------------------------------- report


def raw_sections(root: Path, date_str: str) -> dict:
    """{url: section id} for a daily raw note — the provenance layer of every pick."""
    path = root / "archives" / f"TR-raw-D-{date_str}.md"
    if not path.exists():
        return {}
    found, sid = {}, ""
    for line in path.read_text(encoding="utf-8").splitlines():
        head = re.match(r"^## (\S+) — ", line)
        if head:
            sid = head.group(1)
            continue
        m = re.match(r"^- \[.+\]\((?:<)?([^)>\s]+)(?:>)?\) — ", line)
        if m and sid:
            found[m.group(1)] = sid
    return found


def section_counts(root: Path, date_str: str) -> dict:
    """{sid: count} for the sections that returned items (raw note's Provenance line)."""
    path = root / "archives" / f"TR-raw-D-{date_str}.md"
    if not path.exists():
        return {}
    m = re.search(r"^- 各节条目数：(.+)$", path.read_text(encoding="utf-8"), re.M)
    if not m:
        return {}
    counts = {}
    for pair in m.group(1).split("，"):
        sid, _sep, n = pair.rpartition(" ")
        if sid and n.isdigit():
            counts[sid] = int(n)
    return counts


def pool_size(root: Path, date_str: str) -> int:
    """Candidate pool = every item of every non-degraded raw section that day."""
    return sum(section_counts(root, date_str).values())


def academic_available(root: Path, date_str: str) -> set:
    """Academic sections that actually returned items today."""
    return {sid for sid in section_counts(root, date_str) if sid in ACADEMIC_SIDS}


def quota_problems(counts: dict) -> list:
    """Academic-section bias: ML algorithms first, engineering/algorithms buckets capped."""
    out = []
    for sid, (kind, limit) in BUCKET_QUOTA.items():
        got = counts.get(sid, 0)
        if kind == "min" and got < limit:
            out.append(f"学术节来自 {sid} 的条目 {got} < {limit}（ML 算法线是主偏好）")
        elif kind == "max" and got > limit:
            out.append(f"学术节来自 {sid} 的条目 {got} > {limit}（该桶只作添头/拓展）")
    return out


def cmd_report(args) -> int:
    root = Path(args.vault).resolve()
    date_str = args.date.isoformat()
    items = json.loads(Path(args.items).read_text(encoding="utf-8"))
    if not isinstance(items, list):
        print("ERROR: items 文件必须是 JSON 数组")
        return 2
    write_index(root, args.date, quiet=True)      # ensure Related targets resolve
    sections = raw_sections(root, date_str)
    if not sections:
        print(f"ERROR: 缺少 {date_str} 的原始清单，先跑 fetch")
        return 2
    pool = pool_size(root, date_str)
    errors = []
    if not (REPORT_MIN <= len(items) <= REPORT_MAX):
        errors.append(f"条数 {len(items)} 超出 sanity 界 [{REPORT_MIN},{REPORT_MAX}]")
    queries, seen_urls, picked = [], set(), {"精选": [], "学术": []}
    for idx, it in enumerate(items, 1):
        url = str(it.get("url", "")).strip()
        src = str(it.get("source", "")).strip()
        why = str(it.get("why", "")).strip()
        origin = str(it.get("from", "raw")).strip()
        query = str(it.get("query", "")).strip()
        section = str(it.get("section", "精选")).strip() or "精选"
        if not url.startswith(("http://", "https://")):
            errors.append(f"#{idx} url 非法：{url!r}")
        if url in seen_urls:
            errors.append(f"#{idx} url 重复：{url}")
        seen_urls.add(url)
        if not src:
            errors.append(f"#{idx} 缺 source")
        if not why:
            errors.append(f"#{idx} 缺 why")
        if section not in picked:
            errors.append(f"#{idx} section 只能是 {list(picked)}，得到 {section!r}")
        else:
            picked[section].append(url)
        origin_sid = sections.get(url)
        if origin == "raw":
            if origin_sid is None:
                errors.append(f"#{idx} 声称来自原始清单，但 URL 不在 TR-raw-D-{date_str}：{url}")
            elif section == "学术" and origin_sid not in ACADEMIC_SIDS:
                errors.append(f"#{idx} 学术节条目却来自非学术源 {origin_sid}：{url}")
            elif section == "精选" and origin_sid in ACADEMIC_SIDS:
                errors.append(f"#{idx} 来自学术源 {origin_sid} 的条目应放「学术」节：{url}")
        elif origin == "websearch":
            if not query:
                errors.append(f"#{idx} from=websearch 必须提供 query")
            else:
                queries.append(query)
        else:
            errors.append(f"#{idx} from 只能是 raw 或 websearch，得到 {origin!r}")
    for layer in ("精选", "学术"):
        if not picked[layer]:
            errors.append(f"{layer} 节为空（两节都至少要有一条）")
    cited = {}
    for url in picked["学术"]:
        sid = sections.get(url)
        if sid:
            cited[sid] = cited.get(sid, 0) + 1
    available = academic_available(root, date_str)
    if len(available) >= 2 and len(cited) < 2:
        errors.append(f"学术节只用到 {len(cited)} 个学术源（今日可用 {sorted(available)}），需 ≥2")
    errors += quota_problems(cited)
    if errors:
        print("ERROR: items 校验失败：")
        for e in errors:
            print(f"  - {e}")
        return 2
    raw_note = f"TR-raw-D-{date_str}"
    degraded, degraded_sid = [], ""
    raw_path = root / "archives" / f"{raw_note}.md"
    for line in raw_path.read_text(encoding="utf-8").splitlines():
        head = re.match(r"^## (\S+) — ", line)
        if head:
            degraded_sid = head.group(1)
        elif line.startswith("> [降级]"):
            degraded.append(f"{degraded_sid} {line.removeprefix('> [降级] ').strip()}")
    fm = fm_block(["tags:", "  - type/permanent", "  - status/archive", "  - topic/ai",
                   f"created: {date_str}", f"data-date: {date_str}", "source:",
                   f'  - "原始清单（API 快照逐条校验）：[[{raw_note}]]"']
                  + [f'  - "web_search：{q}"' for q in sorted(set(queries))])
    body = [f"\n# Trend Radar {date_str}\n",
            f"\n> 候选池 {pool} 条（原始清单正常节合计）/ 入选 {len(items)} 条"
            f"（精选 {len(picked['精选'])} + 学术 {len(picked['学术'])}）；"
            f"条数随当日信号浮动，不设固定配额；每条含来源与一句为什么值得看。\n"]
    if note_exists(root, "TR-leaderboards"):
        body.append("> 榜单快照（每日覆盖，含较昨日 Δ）：[[TR-leaderboards]]\n")
    if degraded:
        body.append("> 降级：<br>" + "<br>".join(degraded) + "\n")
    for layer, heading in (("精选", "## 精选"), ("学术", "## 学术")):
        body.append(f"\n{heading}\n\n")
        for it in items:
            if (str(it.get("section", "精选")).strip() or "精选") != layer:
                continue
            tail = f"{it['source']} · {it['why']}"
            if str(it.get("from")) == "websearch":
                tail += f" ⟦ws: {it['query']}⟧"
            body.append(f"- [ ] {md_link(it['title'], it['url'])} — {tail}\n")
    body.append("\n---\n## Related\n\n")
    body.append(f"- [[{raw_note}]]\n")
    body += related_links(root)
    path = root / "archives" / f"TR-D-{date_str}.md"
    if path.exists() and not args.force:
        print(f"ERROR: {path.name} 已存在（加 --force 覆盖）")
        return 2
    path.write_text(fm + "".join(body), encoding="utf-8")
    print(f"写入 {path.relative_to(root)}（候选池 {pool} / 入选 {len(items)} 条："
          f"精选 {len(picked['精选'])} + 学术 {len(picked['学术'])}，"
          f"web_search {len(set(queries))} 查询）")
    write_index(root, args.date)
    return 0


# ---------------------------------------------------------------- index


def artifact_sort_key(name: str):
    m = re.match(r"^TR-(?:raw-)?([DWMY])-(.+)$", name)
    if not m:
        return (9, name)
    kind, tag = m.group(1), m.group(2)
    return ({"D": 0, "W": 1, "M": 2, "Y": 3}[kind], tag)


def current_reports(root: Path):
    out = []
    for path in (root / "archives").glob("TR-[DWMY]-*.md"):
        out.append(path)
    return sorted(out, key=lambda p: artifact_sort_key(p.stem), reverse=True)


def raw_for(report_stem: str, root: Path):
    m = re.match(r"^TR-([DWMY]-(.+))$", report_stem)
    if not m:
        return None
    candidate = root / "archives" / f"TR-raw-{m.group(1)}.md"
    return candidate if candidate.exists() else None


def item_count(path: Path) -> int:
    return len(parse_items(path))


def note_exists(root: Path, name: str) -> bool:
    """True when a wikilink target resolves inside this vault."""
    return any((root / rel).exists() for rel in (f"{name}.md",)) or any(
        p.stem == name for p in root.rglob("*.md"))


def related_links(root: Path, extra=(), exclude=()) -> list:
    names = [n for n in (*extra, "TR-leaderboards", INDEX_NAME, "AI 报告挂载 Todo")
             if n not in exclude]
    return [f"- [[{name}]]\n" for name in dict.fromkeys(names) if note_exists(root, name)]


def leaderboard_labels(root: Path) -> list:
    """Board names in the current TR-leaderboards snapshot, in file order."""
    path = root / "archives" / "TR-leaderboards.md"
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## \S+ — (.+)$", line)
        if m:
            out.append(m.group(1).split("（")[0].strip())
    return out


def write_index(root: Path, day: date, quiet: bool = False) -> Path:
    reports = current_reports(root)
    lines = [fm_block(["tags:", "  - todo"]),
             "\n## Aim\n\n",
             "Trend Radar 每日情报流的索引：原始清单与精选报告一律落 `archives/`"
             "（`TR-raw-*` / `TR-*`），本笔记只挂载当前仍在的件。"
             "报告按 ISO 周 → 自然月 → 自然年滚动合并（7/4/12），被合并件删除。\n",
             "\n## Items\n\n"]
    if reports:
        for rep in reports:
            raw = raw_for(rep.stem, root)
            kind = {"D": "日报", "W": "周报", "M": "月报", "Y": "年报"}[rep.stem[3]]
            tail = f"（{kind}，{item_count(rep)} 条）"
            if raw:
                tail += f" — 原始 [[{raw.stem}]]"
            lines.append(f"- [ ] [[{rep.stem}]]{tail}\n")
    else:
        lines.append("- [ ] （尚无报告：跑一次 `python3 tools/trend_radar.py fetch`）\n")
    if note_exists(root, "TR-leaderboards"):
        labels = leaderboard_labels(root)
        tail = "、".join(labels) if labels else "每榜前 10"
        lines.append(f"- [ ] [[TR-leaderboards]]（当前榜单快照：{tail}；每日覆盖）\n")
    lines += ["\n## Key Methods\n\n",
              "- 调用：让 AI 跑 skill `trend-radar`（`.agent/skills/trend-radar/SKILL.md`）\n",
              "- 抓取层：HuggingFace（模型/数据集/Space/日报论文）/ arXiv（AI 桶 cs.AI·LG·CL + "
              "ML 算法桶 stat.ML·math.OC·cs.NA + 工程桶 cs.SE·PL·AR·OS + 算法桶 cs.DS·CG·CC）/ "
              "Semantic Scholar / OpenAlex（期刊会议）/ Hacker News / "
              "Lobsters / GitHub，原始清单零 AI 改写、逐条可回溯到 API 快照\n",
              "- 精选层：分「精选 + 学术」两节，条数随当日信号浮动（不设固定配额）；"
              "学术节以 ML 算法/优化为主（≥2 条），工程桶与算法桶各 ≤2；"
              "每条一句为什么值得看，空白处用 web_search 补漏\n",
              "\n## Applications\n\n---\n## **Related**\n\n",
              *related_links(root, ("Index of Todos",), exclude=INDEX_NAME)]
    path = root / INDEX_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(lines), encoding="utf-8")
    register_in_todos_index(root)
    if not quiet:
        print(f"写入 {path.relative_to(root)}")
    return path


def register_in_todos_index(root: Path) -> None:
    path = root / TODOS_INDEX_REL
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    if f"[[{INDEX_NAME}]]" in text:
        return
    anchor = "- [ ] [[AI 报告挂载 Todo]]"
    if anchor in text:
        text = text.replace(anchor, f"{anchor}\n- [ ] [[{INDEX_NAME}]]", 1)
    else:
        text = text.replace("## Key Methods", f"- [ ] [[{INDEX_NAME}]]\n\n## Key Methods", 1)
    path.write_text(text, encoding="utf-8")
    print(f"已登记 [[{INDEX_NAME}]] 到 {TODOS_INDEX_REL}")


def cmd_index(args) -> int:
    root = Path(args.vault).resolve()
    write_index(root, args.date)
    return 0


# ---------------------------------------------------------------- merge


DAILY_RE = re.compile(r"^TR-(raw-)?D-(\d{4}-\d{2}-\d{2})$")
WEEKLY_RE = re.compile(r"^TR-(raw-)?W-(\d{4})-W(\d{2})$")
MONTHLY_RE = re.compile(r"^TR-(raw-)?M-(\d{4}-\d{2})$")

KIND_CN = {"D": "日报", "W": "周报", "M": "月报", "Y": "年报"}
THRESHOLD = {"W": 7, "M": 4, "Y": 12}


def raw_sibling(path: Path) -> Path:
    return path.with_name(path.stem.replace("TR-", "TR-raw-", 1) + ".md")


ITEM_LINE_RE = re.compile(r"^- (?:\[ \] )?\[(.+)\]\((?:<)?([^)>\s]+)(?:>)?\) — (.+)$")


def parse_items(path: Path):
    """Return [{"title","url","tail"}] for bullet item lines of a TR artifact."""
    return parse_items_in(path.read_text(encoding="utf-8"))


def parse_items_in(text: str):
    out = []
    for line in text.splitlines():
        m = ITEM_LINE_RE.match(line)
        if m:
            out.append({"title": m.group(1), "url": m.group(2), "tail": m.group(3)})
    return out


def parse_sections_in(text: str):
    """[{"head": "精选", "items": [...]}] — item bullets grouped under their `## ` heading."""
    out, cur = [], None
    for line in text.splitlines():
        head = re.match(r"^## (\S+)$", line)
        if head:
            cur = {"head": head.group(1), "items": []}
            out.append(cur)
            continue
        m = ITEM_LINE_RE.match(line)
        if m:
            if cur is None:
                cur = {"head": "条目", "items": []}
                out.append(cur)
            cur["items"].append({"title": m.group(1), "url": m.group(2), "tail": m.group(3)})
    return out


def coverage_of(path: Path):
    """(start, end) ISO dates covered by one artifact."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^coverage: (\d{4}-\d{2}-\d{2})\.\.(\d{4}-\d{2}-\d{2})$", text, re.M)
    if m:
        return m.group(1), m.group(2)
    dm = re.search(r"^TR-(?:raw-)?D-(\d{4}-\d{2}-\d{2})$", path.stem, re.M)
    if dm:
        return dm.group(1), dm.group(1)
    return "", ""


def render_items(family: str, entries) -> list:
    box = "- [ ] " if family == "report" else "- "
    return [f"{box}{md_link(e['title'], e['url'])} — {e['tail']}" for e in entries]


def merge_family(root: Path, family: str, kind: str, label: str, children, day: date,
                 dry_run: bool) -> list:
    """Merge one family+period into archives/TR-<raw-><kind>-<label>.md.

    An existing target is the base (idempotent re-merge); children are folded in,
    deduped by URL, then deleted. Returns deleted paths (empty on dry-run).
    """
    prefix = "TR-raw-" if family == "raw" else "TR-"
    target = root / "archives" / f"{prefix}{kind}-{label}.md"
    base_entries = parse_items(target) if target.exists() else []
    entries, index = [], {e["url"]: 0 for e in base_entries}
    for e in base_entries:
        entries.append(e)
    dates = []
    for child in sorted(children):
        start, end = coverage_of(child)
        if start:
            dates.extend([start, end])
        child_date = start if start == end else ""
        child_text = child.read_text(encoding="utf-8")
        layers = {e["url"]: sec["head"] for sec in parse_sections_in(child_text)
                  for e in sec["items"]}
        for e in parse_items_in(child_text):
            if e["url"] in index:
                if child_date and f"⟦{child_date}⟧" not in entries[index[e["url"]]]["tail"]:
                    entries[index[e["url"]]]["tail"] += f" ⟦{child_date}⟧"
                continue
            index[e["url"]] = len(entries)
            fold = dict(e)
            if family == "report" and "学术" in layers.get(e["url"], ""):
                fold["tail"] += " ⟦学术⟧"
            entries.append(fold)
    if family == "raw":
        entries = entries[:MERGE_RAW_CAP]
    span = f"{min(dates)}..{max(dates)}" if dates else f"{day.isoformat()}..{day.isoformat()}"
    if target.exists():                       # keep the wider coverage on re-merge
        old = coverage_of(target)
        if old[0]:
            span = f"{min(old[0], span.split('..')[0])}..{max(old[1], span.split('..')[1])}"
    src = [f'  - "合并自 {len(children)} 份{KIND_CN[kind]}：'
           + "、".join(sorted(c.stem for c in children)) + '"']
    if target.exists():
        src.append(f'  - "上一版 {target.stem}"')
    tags = ["  - type/lit", "  - status/archive", "  - topic/ai"] if family == "raw" \
        else ["  - type/permanent", "  - status/archive", "  - topic/ai"]
    head = fm_block(["tags:", *tags, f"created: {day.isoformat()}",
                     f"period: {label}", f"coverage: {span}", "source:", *src])
    raw_ref = root / "archives" / f"TR-raw-{kind}-{label}.md"
    lines = [head, f"\n# Trend Radar {'原始清单 ' if family == 'raw' else ''}"
                   f"{KIND_CN[kind]} {label}\n\n",
             f"> 覆盖区间 {span.replace('..', ' … ')}；"
             f"被合并的 {len(children)} 份{KIND_CN[kind]}已按滚动规则删除（不保留被合并件）。\n",
             "> 条目按 URL 去重；跨件重复的条目标注其出现日期 ⟦YYYY-MM-DD⟧。\n"]
    if family == "raw":
        lines.append(f"> 原始层按合并顺序保留前 {MERGE_RAW_CAP} 条（完整快照不保留）。\n")
    if family == "report":
        lines.append(f"> 证据层：[[{raw_ref.stem}]]\n")
    lines.append(f"\n## 条目（{len(entries)}）\n\n")
    lines += [ln + "\n" for ln in render_items(family, entries)]
    if family == "report":
        lines += ["\n---\n## Related\n\n", f"- [[{raw_ref.stem}]]\n"]
        lines += related_links(root)
    if dry_run:
        print(f"[dry-run] 将写 {target.relative_to(root)}"
              f"（{len(entries)} 条）← 折叠 {len(children)} 份")
        return []
    target.write_text("".join(lines), encoding="utf-8")
    deleted = []
    for child in children:
        child.unlink()
        deleted.append(child.relative_to(root))
    print(f"写入 {target.relative_to(root)}（{len(entries)} 条）← 合并 {len(children)} 份，"
          f"删除 {len(deleted)} 件："
          + "、".join(sorted(d.name for d in deleted)))
    return deleted


def _period_groups(archives: Path, kind: str):
    """{period_label: [files]} for the given artifact kind."""
    groups = {}
    for path in archives.glob(f"TR-{kind}-*.md"):
        if kind == "D":
            m = DAILY_RE.match(path.stem)
            if not m:
                continue
            groups.setdefault(week_label(date.fromisoformat(m.group(2))), []).append(path)
        elif kind == "W":
            m = WEEKLY_RE.match(path.stem)
            if not m:
                continue
            d = date.fromisocalendar(int(m.group(2)), int(m.group(3)), 4)
            groups.setdefault(f"{d.year:04d}-{d.month:02d}", []).append(path)
        else:
            m = MONTHLY_RE.match(path.stem)
            if not m:
                continue
            groups.setdefault(m.group(2)[:4], []).append(path)
    return groups


def cmd_merge(args) -> int:
    root = Path(args.vault).resolve()
    day, dry = args.date, args.dry_run
    archives = root / "archives"
    merged = []
    for kind, source_kind in (("W", "D"), ("M", "W"), ("Y", "M")):
        for label, group in sorted(_period_groups(archives, source_kind).items()):
            if len(group) < THRESHOLD[kind]:
                continue
            group_sorted = sorted(group)
            anchor = max((coverage_of(p) for p in group_sorted), key=lambda c: c[1])
            anchor_date = date.fromisoformat(anchor[1]) if anchor[1] else day
            raw_children = [p for p in (raw_sibling(c) for c in group_sorted) if p.exists()]
            merged += merge_family(root, "raw", kind, label, raw_children, anchor_date, dry)
            merged += merge_family(root, "report", kind, label, group_sorted, anchor_date, dry)
    if not merged:
        print("[dry-run] 无周期达到阈值，无需合并" if dry else "无需合并（无周期达到阈值）")
    return 0


# ---------------------------------------------------------------- verify


def all_note_stems(root: Path):
    stems = set()
    for path in root.rglob("*.md"):
        rel = path.relative_to(root)
        if str(rel).startswith((".obsidian", ".git", "template/")):
            continue
        stems.add(path.stem)
    return stems


def resolve_artifact(root: Path, day: date, family: str):
    """Today's artifact: the daily, or the rolled-up file that now covers it."""
    prefix = "TR-raw-" if family == "raw" else "TR-"
    daily = root / "archives" / f"{prefix}D-{day.isoformat()}.md"
    if daily.exists():
        return daily, "D"
    week = root / "archives" / f"{prefix}W-{week_label(day)}.md"
    if week.exists() and covers(week, day):
        return week, "W"
    month = root / "archives" / f"{prefix}M-{week_month(day)}.md"
    if month.exists() and covers(month, day):
        return month, "M"
    year = root / "archives" / f"{prefix}Y-{day.year:04d}.md"
    if year.exists() and covers(year, day):
        return year, "Y"
    return daily, "D"


def covers(path: Path, day: date) -> bool:
    start, end = coverage_of(path)
    return bool(start) and start <= day.isoformat() <= end


def cmd_verify(args) -> int:
    root = Path(args.vault).resolve()
    day = args.date
    date_str = day.isoformat()
    problems, notes = [], []

    raw_path, raw_kind = resolve_artifact(root, day, "raw")
    if not raw_path.exists():
        problems.append(f"缺原始清单 archives/TR-raw-*-{date_str}（当天件与滚动件均不存在）")
    else:
        text = raw_path.read_text(encoding="utf-8")
        if raw_kind == "D":
            legacy_raw = day < LAYER_CUTOVER
            sections = re.findall(r"^## (\S+) — (.+)$", text, re.M)
            present = {sid for sid, _label in sections}
            if len(sections) != len(SOURCES) and not legacy_raw:
                problems.append(f"原始清单节数 {len(sections)} ≠ 源数 {len(SOURCES)}")
            if legacy_raw:
                notes.append(f"旧契约原始清单（< {LAYER_CUTOVER}）：{len(sections)} 节，"
                             f"新增的 arXiv 桶/s2 不要求存在")
            for sid, _label, _fn in SOURCES:
                if legacy_raw and sid not in present:
                    continue
                block = re.search(rf"^## {re.escape(sid)} — [^\n]*\n(.*?)(?=^## |\Z)",
                                  text, re.M | re.S)
                if not block:
                    problems.append(f"原始清单缺 {sid} 节")
                    continue
                body = block.group(1)
                if "[未启用]" in body:
                    reason = re.search(r"\[未启用\] (.+)", body)
                    notes.append(f"{sid} 未启用：{reason.group(1) if reason else '未写明原因'}")
                    continue
                if "[降级]" in body:
                    reason = re.search(r"\[降级\] 抓取失败：(.+)", body)
                    if reason:
                        notes.append(f"{sid} 降级：{reason.group(1)}")
                    else:
                        problems.append(f"{sid} 标了降级但未写原因")
                    continue
                n = len(parse_items_in(body))
                floor = SECTION_FLOOR.get(sid, MIN_ITEMS)
                if n < floor:
                    problems.append(f"{sid} 条目 {n} < {floor}")
                else:
                    notes.append(f"{sid} {n} 条")
            prov = re.search(r"URL 命中：(\d+)/(\d+)", text)
            if not prov:
                problems.append("原始清单缺 Provenance 命中率")
            elif prov.group(1) != prov.group(2):
                problems.append(f"Provenance 命中率不足：{prov.group(1)}/{prov.group(2)}")
            else:
                notes.append(f"provenance {prov.group(1)}/{prov.group(2)}")
        else:
            n = len(parse_items(raw_path))
            if n == 0:
                problems.append(f"滚动原始件 {raw_path.name} 无条目")
            elif n > MERGE_RAW_CAP:
                problems.append(f"滚动原始件 {raw_path.name} 超过 {MERGE_RAW_CAP} 条上限（{n}）")
            else:
                notes.append(f"滚动原始件 {raw_path.name}（{n} 条，含 {date_str}）")

    rep_path, rep_kind = resolve_artifact(root, day, "report")
    if not rep_path.exists():
        problems.append(f"缺当日报告 archives/TR-*-{date_str}")
    else:
        rep_text = rep_path.read_text(encoding="utf-8")
        lines = [ln for ln in rep_text.splitlines() if ln.startswith("- [ ] ")]
        if rep_kind == "D":
            legacy = day < LAYER_CUTOVER
            if legacy:
                notes.append(f"旧契约日报（< {LAYER_CUTOVER}）：只查条目可回溯性，"
                             f"不套两节/条数规则")
            elif not (REPORT_MIN <= len(lines) <= REPORT_MAX):
                problems.append(f"报告条数 {len(lines)} 不在 sanity 界 "
                                f"[{REPORT_MIN},{REPORT_MAX}]")
            picked, cur = {}, None
            for ln in rep_text.splitlines():
                head = re.match(r"^## (\S+)", ln)
                if head:
                    cur = head.group(1)
                    picked.setdefault(cur, [])
                    continue
                m = re.match(r"^- \[ \] \[.+\]\((?:<)?([^)>\s]+)(?:>)?\) — (.+)$", ln)
                if not m:
                    if ln.startswith("- [ ] "):
                        problems.append(f"报告行格式不合规：{ln[:70]}")
                    continue
                if cur:
                    picked[cur].append((m.group(1), m.group(2)))
            for layer in ("精选", "学术"):
                if not legacy and not picked.get(layer):
                    problems.append(f"报告缺「{layer}」节或该节无条目")
            sections = raw_sections(root, date_str) if raw_kind == "D" else {}
            cited = {}
            for layer, rows in picked.items():
                if layer == "Related":
                    continue
                for url, tail in rows:
                    ws = re.search(r"⟦ws: (.+?)⟧$", tail)
                    if "·" not in tail:
                        problems.append(f"报告行缺 why：{url}")
                    if ws and not ws.group(1).strip():
                        problems.append(f"web_search 标注为空：{url}")
                    sid = sections.get(url)
                    if sections and sid is None and not ws:
                        problems.append(f"报告 URL 既不在原始清单也无 web_search 标注：{url}")
                        continue
                    if legacy or not sid or layer not in ("精选", "学术"):
                        continue
                    if layer == "学术" and sid not in ACADEMIC_SIDS:
                        problems.append(f"报告学术节含非学术源条目（{sid}）：{url}")
                    if layer == "精选" and sid in ACADEMIC_SIDS:
                        problems.append(f"报告精选节含学术源条目（{sid}）：{url}")
                    if layer == "学术":
                        cited[sid] = cited.get(sid, 0) + 1
            if raw_kind == "D" and not legacy:
                pool = pool_size(root, date_str)
                m = re.search(r"候选池 (\d+) 条.*?入选 (\d+) 条", rep_text)
                if not m:
                    problems.append("报告缺「候选池 N / 入选 M」一行")
                else:
                    n_pool, n_pick = int(m.group(1)), int(m.group(2))
                    if n_pool != pool:
                        problems.append(f"报告候选池 {n_pool} ≠ 原始清单合计 {pool}")
                    if n_pick != len(lines):
                        problems.append(f"报告入选 {n_pick} ≠ 实际条目 {len(lines)}")
                    if n_pick > n_pool:
                        problems.append(f"报告入选 {n_pick} > 候选池 {n_pool}")
                available = academic_available(root, date_str)
                if len(available) >= 2 and len(cited) < 2:
                    problems.append(f"报告学术节只用到 {len(cited)} 个学术源"
                                    f"（今日可用 {sorted(available)}），需 ≥2")
                quota = quota_problems(cited)
                if quota:
                    problems += [f"配额：{p}" for p in quota]
                else:
                    notes.append("学术配额 ok（" + "，".join(
                        f"{sid} {cited.get(sid, 0)}" for sid in BUCKET_QUOTA) + "）")
        else:
            if not lines:
                problems.append(f"滚动报告件 {rep_path.name} 无条目")
            notes.append(f"滚动报告件 {rep_path.name}（{len(lines)} 条，含 {date_str}）")
        notes.append(f"报告 {len(lines)} 条（候选池 "
                     f"{pool_size(root, date_str) if raw_kind == 'D' else '—'}）")

    index_path = root / INDEX_REL
    if not index_path.exists():
        problems.append(f"缺索引 {INDEX_REL}")
    else:
        text = index_path.read_text(encoding="utf-8")
        if "  - todo" not in text:
            problems.append("索引缺裸 todo 标签")
        stems = all_note_stems(root)
        for m in re.finditer(r"\[\[([^\]|#]+)", text):
            if m.group(1).split("/")[-1] not in stems:
                problems.append(f"索引含失效 wikilink：[[{m.group(1)}]]")
        reports = current_reports(root)
        for rep in reports:
            if f"[[{rep.stem}]]" not in text:
                problems.append(f"索引缺当前件链接：[[{rep.stem}]]")
        notes.append(f"索引链 {len(reports)} 件")

    week_counts = {}
    for path in (root / "archives").glob("TR-D-*.md"):
        m = DAILY_RE.match(path.stem)
        if m:
            label = week_label(date.fromisoformat(m.group(2)))
            week_counts[label] = week_counts.get(label, 0) + 1
    for label, n in sorted(week_counts.items()):
        if n >= THRESHOLD["W"]:
            problems.append(f"ISO 周 {label} 有 {n} 份日报未合并（应 <{THRESHOLD['W']}）")
    for path in root.glob("TR-*.md"):
        problems.append(f"TR 文件落在 root：{path.name}")

    lb_path = root / LB_NOTE_REL
    if not lb_path.exists():
        problems.append(f"缺榜单快照 {LB_NOTE_REL}")
    else:
        text = lb_path.read_text(encoding="utf-8")
        for spec in LEADERBOARDS:
            block = re.search(rf"^## {re.escape(spec['id'])} — [^\n]*\n(.*?)(?=^## |\Z)",
                              text, re.M | re.S)
            if not block:
                problems.append(f"榜单缺 {spec['id']} 节")
                continue
            body = block.group(1)
            if "[降级]" in body or "[未启用]" in body:
                notes.append(f"{spec['id']} 未出数（降级/未启用，已注明原因）")
                continue
            rows = len(re.findall(r"^\| \d+ \|", body, re.M))
            if rows < LB_TOP:
                problems.append(f"榜单 {spec['id']} 只有 {rows} 行 < {LB_TOP}")
            elif "来源" not in body or "sha256" not in body:
                problems.append(f"榜单 {spec['id']} 缺来源/快照指纹")
            else:
                notes.append(f"{spec['id']} {rows} 行 + 来源指纹")
        state_path = root / LB_STATE_REL
        if not state_path.exists():
            problems.append(f"缺榜单状态文件 {LB_STATE_REL}（Δ 无从计算）")
        else:
            try:
                state = json.loads(state_path.read_text(encoding="utf-8"))
                if not state.get("date") or not isinstance(state.get("boards"), dict):
                    problems.append("榜单状态文件结构不完整")
                else:
                    notes.append(f"榜单状态 {state['date']}（{len(state['boards'])} 个榜）")
            except ValueError:
                problems.append("榜单状态文件不是合法 JSON")
        index_text = (root / INDEX_REL).read_text(encoding="utf-8") \
            if (root / INDEX_REL).exists() else ""
        if "[[TR-leaderboards]]" not in index_text:
            problems.append("索引未挂 [[TR-leaderboards]]")

    print(f"# Trend Radar 校验 {date_str}\n")
    for n in notes:
        print(f"  ok   {n}")
    if problems:
        print()
        for p in problems:
            print(f"  FAIL {p}")
        print(f"\nPROBLEMS: {len(problems)}")
        return 1
    print("\nALL CHECKS PASS")
    return 0


# ---------------------------------------------------------------- run


def prov_candidates(url: str):
    """Strings that legitimately represent this URL inside an API payload."""
    cands = {url}
    if "://" in url:
        rest = url.split("://", 1)[1]
        cands.add(rest)
        path = rest.split("/", 1)[1] if "/" in rest else ""
        path = path.split("?")[0]
        if path:
            cands.add(path)
            cands.add(url_tail(path))
    cands.add(url_tail(url))
    return {c for c in cands if c}


def snapshot_recheck(root: Path, day: date, snap: Path) -> list:
    """Re-assert every raw-list URL against the retained API snapshot bytes."""
    raw_path = root / "archives" / f"TR-raw-D-{day.isoformat()}.md"
    text = raw_path.read_text(encoding="utf-8")
    bad = []
    for sid, _label, _fn in SOURCES:
        block = re.search(rf"^## {re.escape(sid)} — [^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
        snap_file = snap / f"{sid}.raw"
        if not block or not snap_file.exists():
            continue
        raw_bytes = snap_file.read_bytes()
        for it in parse_items_in(block.group(1)):
            if not any(c.encode("utf-8") in raw_bytes for c in prov_candidates(it["url"])):
                bad.append(f"{sid}: {it['url']}")
    return bad


def cmd_run(args) -> int:
    root = Path(args.vault).resolve()
    date_str = args.date.isoformat()
    snap = snapshot_dir(date_str, Path(args.snapshot_dir) if args.snapshot_dir else None)
    if not (root / "archives" / f"TR-raw-D-{date_str}.md").exists():
        print("ERROR: 当天还没有原始清单，先跑 `trend_radar.py fetch`")
        return 2
    if snap.exists():
        bad = snapshot_recheck(root, args.date, snap)
        if bad:
            print("ERROR: 快照复核失败（原始清单条目未在快照中命中）：")
            for b in bad[:10]:
                print(f"  - {b}")
            return 1
        print(f"快照复核通过（每条 URL 命中对应源快照字节流）")
    else:
        print(f"提示：快照目录不存在（{snap}），跳过在线复核")
    rc = cmd_report(argparse.Namespace(vault=str(root), date=args.date, items=args.items,
                                       force=True))
    if rc:
        return rc
    cmd_merge(argparse.Namespace(vault=str(root), date=args.date, dry_run=False))
    write_index(root, args.date, quiet=True)      # merge may have folded today's daily away
    rc = cmd_verify(argparse.Namespace(vault=str(root), date=args.date))
    if args.purge:
        purge_snapshots(snap)
    return rc


# ---------------------------------------------------------------- cli


def main() -> int:
    # Shared flags are accepted both before and after the subcommand
    # (SUPPRESS keeps the top-level value when the subcommand omits them).
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--vault", default=argparse.SUPPRESS,
                        help="vault root (default: repo root)")
    common.add_argument("--snapshot-dir", default=argparse.SUPPRESS,
                        help="snapshot base dir (default /tmp/trend-radar)")
    common.add_argument("--date", type=date.fromisoformat, default=argparse.SUPPRESS,
                        help="run date (YYYY-MM-DD)")

    parser = argparse.ArgumentParser(description="Trend Radar — daily trending → archive")
    parser.add_argument("--vault", default=str(ROOT), help="vault root (default: repo root)")
    parser.add_argument("--snapshot-dir", default="", help="snapshot base dir (default /tmp/trend-radar)")
    parser.add_argument("--date", type=date.fromisoformat,
                        default=date.today(), help="run date (YYYY-MM-DD)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("fetch", parents=[common], help="抓取全部源，写原始清单，打印候选池")
    p.add_argument("--purge", action="store_true", help="删除当天快照后退出（不抓取）")
    p.set_defaults(func=cmd_fetch)

    p = sub.add_parser("report", parents=[common], help="由 items.json 生成当日精选报告")
    p.add_argument("--items", required=True)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("merge", parents=[common],
                       help="滚动合并（7 日报→周报，4 周报→月报，12 月报→年报）")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_merge)

    p = sub.add_parser("index", parents=[common], help="重写 a_sticker/todos/Trend Radar.md")
    p.set_defaults(func=cmd_index)

    p = sub.add_parser("verify", parents=[common], help="离线校验当天三层产出")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("run", parents=[common], help="report + merge + index + verify（日常一条命令）")
    p.add_argument("--items", required=True)
    p.add_argument("--purge", action="store_true", help="结束后删除 /tmp 快照")
    p.set_defaults(func=cmd_run)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
