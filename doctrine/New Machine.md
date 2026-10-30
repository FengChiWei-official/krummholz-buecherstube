# New Machine

> 版本：v6（2026-10-30）。
> 同步组：本机状态变化时同步 `doctrine/Vault Extension.md` §同步面 第 10 行。

## Definition

在新设备上得到与旧机器**相同的体验**：结构（笔记、判据、工具、文档）全部随 git 走；
只有 Obsidian 的插件设置与两份运行时状态是每机各异的。本文件是复现清单。

## 仓库里有的 vs 每机各异的

| | 内容 | 迁移方式 |
|---|---|---|
| **在 git 里** | 全部笔记（`library/` `archives/` `a_sticker/` `zzz_output/`）、`doctrine/`、`tools/`（含测试与 CI）、`template/`、`README.md` / `AGENTS.md` | `git clone` 即得。含记忆底座卡片的复习调度注释（插件 `dataStore = NOTES`，调度写回笔记本身） |
| **每机各异（不在 git）** | `.obsidian/`：主题、快捷键、社区插件与其设置、插件的调度索引 `data.json` | 按 §步骤 3–4 手工装 |
| **每机各异** | `archives/work/TR-leaderboards.state.json`（榜单 Δ 的上一次快照，已 gitignore） | 新机器首日无 Δ；跑一次 `python3 tools/trend_radar.py fetch` 即恢复 |
| **每机各异（临时）** | `/tmp/trend-radar/<date>/` 当日候选池快照 | 无需迁移，`fetch` 当场重建 |
| **环境变量** | `SEMANTIC_SCHOLAR_API_KEY` / `OPENALEX_API_KEY` / `ARTIFICIAL_ANALYSIS_API_KEY`（趋势雷达可选；缺则该源降级或标未启用）；`TR_SNAPSHOT_DIR`（快照根目录，可选）；`VAULT_ROOT`（把工具指向别的 vault，可选） | 按需 export；key 只从环境读，绝不写进笔记 |

## 步骤

1. `git clone <repo> <dir> && cd <dir>`。
2. 确认 Python ≥ 3.11（`tools/vaultkit/config.py` 用 stdlib `tomllib`）。跑 `python3 tools/vault.py status`：
   应出节律行、主干计数、编号 next moves。**新 clone 的节律行显示「今天」是已知局限**——它取 git 提交时间与
   mtime 的较大者，而 checkout 会刷新 mtime。
3. Obsidian：把该目录作为 vault 打开；装旧机器的三个社区插件（见 `.obsidian/community-plugins.json`）：
   `templater-obsidian`、`tag-wrangler`、`obsidian-spaced-repetition`。
4. 间隔重复插件设置（核对 `.obsidian/plugins/obsidian-spaced-repetition/data.json`，**不要相信任何文档里的旧值**）：
   - `convertFoldersToDecks = true`——按文件夹分 deck，`a_sticker/or/` 即一个 deck，**不需要任何 tag**
     （与 doctrine「无 tag」一致）。
   - `singleLineCardSeparator = "::"`——与 `a_sticker/or/记忆底座-首批卡片.md` 的语法一致。
   - `dataStore = NOTES`——复习调度写回笔记本身，因此调度状态随 git 走。
5. 可选：`python3 -m venv .venv && .venv/bin/pip install pytest`，然后 `.venv/bin/python -m pytest -q`（CI 也这么跑）。
6. `zzz_output/Root.md` 补一行 `[[Raw Index of Root]]`（owner 动作；AI 不碰 `zzz_output/` 内容）。

## 验收

| 检查 | 期望 |
|---|---|
| `python3 tools/vault.py check` | exit 0，硬门 G1/G2/G3 全绿 |
| `python3 tools/vault.py status` | 节律行 + 主干计数 + 编号 next moves（节律行显示「今天」属正常） |
| `python3 -m pytest -q` | 全绿（v6 为 55 条） |
| `git status` | 干净——`.obsidian/` 被 gitignore，不产生噪声 |
| Obsidian 打开 `a_sticker/or/记忆底座-首批卡片.md` | 间隔重复面板出现**按文件夹划分**的 deck（名含 `or`），卡片可复习 |

## Related

- [[Vault Extension]]
- [[Agent Contract]]
