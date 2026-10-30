# Vault Extension

> 版本：v6（2026-10-30）。
> 同步组：改任何文档或工具文案前，先读本文件 §同步面。

## Definition

维护者手册：**怎么改这个系统而不破坏它的特性**，以及**改了一处要同步哪几处**。
它不是原理（[[Vault Design]]）、不是操作流程（[[Vault Workflow]]）、不是 AI 接手契约（[[Agent Contract]]）、
不是新设备清单（[[New Machine]]）。

## 不可破坏的特性

| # | 特性 | 判据 |
|---|---|---|
| P1 | **硬门恰 3 条**（G1/G2/G3） | `tools/vaultkit/rules.py` 里 `tier="hard"` 的 Rule 数 == 3；新判据默认 `report` |
| P2 | **单解析器** | `grep -rln '_WIKILINK_RE\|def parse_frontmatter\|def extract_links\|_FENCE_RE' tools/vaultkit/` 只命中 `parse.py` |
| P3 | **单配置** | zone / genre / threshold / path 字面量只在 `tools/vault.toml`；代码与文档只引用键名 |
| P4 | **单规则表** | `check` 与 `rawindex --check` 都从 `rules.RULES` 渲染；加规则 = 追加一个 `Rule` |
| P5 | **退出码固定** | 0 正常 / 1 硬门失败或未知目标 / 2 配置缺失——不复用为别的含义 |
| P6 | **写操作默认 dry-run** | `rawindex --sync` 不带 `--apply` 不落盘；新增写命令沿用同一默认 |
| P7 | **性能预算** | `vault.py status` < 2 s；git 考古一次性批量（`cli.git_first_seen_index`），不得回到每笔记一个子进程 |
| P8 | **输出格式即契约** | `tests/` 断言输出字符串；改措辞 = 改测试 |
| P9 | **内容边界** | 状态只在 todo 树；AI 不写 own-voice 正文；`zzz_output/` 内容 AI 不碰 |

## 代码放哪里（分层）

| 关注点 | 文件 |
|---|---|
| 常量 / 区域 / 体裁 / 阈值 / 路径 | `tools/vault.toml`（`tools/vaultkit/config.py` 读取） |
| 文本解析（唯一） | `tools/vaultkit/parse.py` |
| 图 / 登记边 / 环 / 绑定邻居 | `tools/vaultkit/model.py` |
| 判据 | `tools/vaultkit/rules.py` |
| 命令 / 渲染 / help | `tools/vaultkit/cli.py` |
| 趋势雷达（源与阈值由 `--help` epilog 自动列出） | `tools/trend_radar.py` |

分层自检：加一条判据不应改动 `check` 的输出结构、`status` 的字段或 `triage` 的类别。

## 改法配方

### 1. 加一条判据

1. `tools/vaultkit/rules.py` 的 `RULES` 追加 `Rule(id, tier, title, fn, short, note)`：
   `tier` 默认 `"report"`；`fn(ctx) -> list[str]` **首行是摘要**、其余是明细，不要自带缩进（渲染器加）；
   `short` 是 `rawindex --check` 的标题（`None` = 不出现）；`note` 可选 `ctx -> str`，在 `check` 标题下打一行。
2. `tests/fixtures/mini_vault/` 造最小触发场景，在 `tests/test_cli.py` 断言那行输出。
3. 按 §同步面 第 2 行同步文档。

### 2. 改一个阈值 / 分区 / 体裁

只改 `tools/vault.toml`。文档只准写键名（如 `todo_stale_days`），不准写数值——数值副本被 §自检 第 2 条拦。

### 3. 加一个子命令 / 旗标

1. `cli.py build_parser()` 用 `parents=[common]`（继承 `--strict` / `--json`）。
2. 实现拆 `collect_*`（返回 dict，供 `--json`）与 `cmd_*`（渲染文本）；`wants_json(args)` 分支里 `emit_json(payload)`。
3. `HELP_TOPICS` 加一个 topic（面向使用者时）。
4. 按 §同步面 第 5 行同步入口表与 README。

### 4. 改主干模型 / 登记语义

`tools/vault.toml [trunk] model`（`tree` | `dag`）是唯一开关；`model.Graph.registration_violations()` 按模型分流。
改语义按 §同步面 第 4 行同步。

## 同步面

左列是触发点，右列必须同改，同一提交内完成。

| # | 触发改动 | 必须同步 |
|---|---|---|
| 1 | `tools/vault.toml` | 无需改文档；核对 `cli.py` 的 `HELP_TOPICS` / epilog 是否引用了被改的键名 |
| 2 | `tools/vaultkit/rules.py` 判据增删改名 | `README.md` §工具；`AGENTS.md` §Invariants；`doctrine/Agent Contract.md` §6；`doctrine/Vault Design.md` §判据两级制；`tools/vaultkit/cli.py`（`cmd_check` 头行、`help rawindex` 文案）；`a_sticker/or/记忆底座-首批卡片.md` 规则卡；`tests/` |
| 3 | 硬门增删 | 先要 owner 裁决 + `doctrine/Vault Design.md` §决策台账 新 D 号；再第 2 行全部 + `tests/` + `.github/workflows/ci.yml` |
| 4 | `tools/vaultkit/model.py` 登记语义 / 主干模型 | `doctrine/Vault Design.md` §两棵树 + §关键 doctrine；`README.md` §两棵树；`AGENTS.md` 硬规则 3；`cli.py help dag` |
| 5 | `cli.py` 子命令 / 旗标 / 退出码 | `README.md` §工具；`doctrine/Agent Contract.md` §1 + §Exit codes；`cli.py` 顶层 epilog |
| 6 | 体裁 / 分区规则 | `AGENTS.md` 硬规则 2、4；`doctrine/Vault Design.md` §区域；`README.md` §区域；记忆底座卡「体裁由什么决定」 |
| 7 | 字段政策 | `AGENTS.md` 硬规则 4；`doctrine/Vault Design.md` §字段；`README.md` §最小记忆集；记忆底座卡「保留哪些 frontmatter 字段」 |
| 8 | 模板政策 | `AGENTS.md` 硬规则 4；`doctrine/Vault Design.md` §字段；`README.md` §最小记忆集第 1 条 |
| 9 | doctrine 任何语义变化 | `doctrine/Vault Design.md` §决策台账（新 D 号）；`a_sticker/or/记忆底座-首批卡片.md` 重新生成（该文件头部自带漂移规则） |
| 10 | 本机 / Obsidian / 插件设置 | `doctrine/New Machine.md` §本机状态表 |
| 11 | 新增 doctrine 文件 | `AGENTS.md` §Source of truth；`README.md` §协作 + §Related Files；`doctrine/Vault Design.md` §区域；`.agent/skills/vault-ops/SKILL.md` §Load order；本表自身 |

## 自检

```bash
# 1) 无过时的 v5 判据措辞（只应命中本文件的示例命令）
grep -rn 'I1–I4\|I1-I4' README.md AGENTS.md doctrine/ tools/vaultkit/ | grep -v 'Vault Extension'

# 2) 阈值数值无副本（只应命中 tools/vault.toml）
grep -rnE '(^|[^0-9])90([^0-9]|$)|0\.97|(^|[^0-9])0\.9([^0-9]|$)' README.md AGENTS.md doctrine/*.md .agent/skills/*/SKILL.md

# 3) 规则 id 与四处文档一致（期望打印 OK）
python3 - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, "tools")
from vaultkit import rules
ids = [r.id for r in rules.RULES]
docs = ("README.md", "AGENTS.md", "doctrine/Vault Design.md", "doctrine/Agent Contract.md")
missing = {d: [i for i in ids if i not in Path(d).read_text(encoding="utf-8")] for d in docs}
print({d: m for d, m in missing.items() if m} or "OK")
PY
```

## Related

- [[Vault Design]]
- [[Vault Workflow]]
- [[Agent Contract]]
- [[New Machine]]
