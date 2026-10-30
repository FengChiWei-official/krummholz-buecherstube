# Vault Extension

> 版本：v6（2026-10-30）。
> 同步组：本文件是同步面本身；新增 doctrine 文件按 T11。

## Definition

维护者手册：**怎么改这个系统而不破坏它的特性**，以及**改了一处要同步哪几处**。
它不是原理（[[Vault Design]]）、不是操作流程（[[Vault Workflow]]）、不是 AI 接手契约（[[Agent Contract]]）、
不是新设备清单（[[New Machine]]）。

## 不可破坏的特性

| # | 特性 | 判据 |
|---|---|---|
| P1 | **硬门恰 3 条**（G1/G2/G3） | `tools/vaultkit/rules.py` 里 `tier="hard"` 的 Rule 数 == 3；新判据默认 `report` |
| P2 | **单解析器** | `grep -rln --include='*.py' '_WIKILINK_RE\|def parse_frontmatter\|def extract_links\|_FENCE_RE' tools/vaultkit/` 只命中 `parse.py` |
| P3 | **单配置** | zone / genre / threshold / path 字面量只在 `tools/vault.toml`；代码与文档只引用键名 |
| P4 | **单规则表** | `check` / `rawindex --check` / `status` 都从 `rules.RULES` 渲染；加规则 = 追加一个 `Rule` |
| P5 | **退出码固定** | 0 正常 / 1 硬门失败或未知目标 / 2 配置缺失——不复用为别的含义 |
| P6 | **写操作默认 dry-run** | `rawindex --sync` 不带 `--apply` 不落盘；新增写命令沿用同一默认 |
| P7 | **性能预算** | `vault.py status` < 2 s；git 考古一次性批量（`cli.git_first_seen_index`），不得回到每笔记一个子进程 |
| P8 | **输出格式即契约** | `tests/` 断言输出字符串；改措辞 = 改测试 |
| P9 | **内容边界** | 状态只在 todo 树；AI 不写 own-voice 正文；`zzz_output/` 内容 AI 不碰 |

## 代码放哪里（分层）

| 关注点 | 文件 |
|---|---|
| 常量 / 区域 / 体裁 / 阈值 / 路径 / 模板映射 / 文档同步面 | `tools/vault.toml`（`tools/vaultkit/config.py` 读取） |
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
3. `HELP_TOPICS` 加一个 topic——**有门**：没有 topic 的子命令（`help` 除外）测试会红；命令名还必须在 `.agent/skills/vault-ops/SKILL.md` 里露面，并在 fixture 上真跑一次（`tests/test_docs.py` 的 `BARE` 表）。
4. 按 §同步面 T5 同步入口表、README 与 `tests/`；跑 `python3 tools/vault.py docs-check --gate` 确认没漏。

### 4. 改主干模型 / 登记语义

`tools/vault.toml [trunk] model`（`tree` | `dag`）是唯一开关；`model.Graph.registration_violations()` 按模型分流。
改语义按 §同步面 T4 同步。

### 5. 新增一份 doctrine 文件

1. 文件放 `doctrine/`，头部两行：`> 版本：v6（YYYY-MM-DD）。` 与 `> 同步组：…`（同步组里引用 T 号）。
2. 按 §同步面 T11 同步那四处注册点。
3. `python3 tools/vault.py docs-check --gate` 会替你盯着 T11——新增 doctrine 文件本身是探针。

### 6. 加一个脚手架

1. 文件放 `template/`，含 `aliases:`（material 的还要 `source:`），`[[NAME]]` 会被 `new` 替换成笔记名——它是占位符，不是链接（`rename` 不碰它）。
2. `tools/vault.toml [templates]` 加一个键（键 = 体裁/分区：`node` / `raw` / `index` / `links` / `material` / `todos`）。
3. 无需改文档：文档只引用键名与 `[templates]`，不写文件数量（§自检 拦数值副本）。

### 7. 发版

1. `tools/vaultkit/__init__.py` 的 `__version__` 升到新版本（`status --json` / `check --json` 直接读它）。
2. `tools/CHANGELOG.md`：把 `Unreleased` 段转成 `## v<版本>（日期）`，写清这一版是**加性**还是**破坏性**。
3. `doctrine/` 的 `版本：v6` 头**不动**——那是 doctrine 集的版本，与工具版本独立；只有 doctrine 语义变化才动它（走 T9 + 新 D 号）。
4. `python3 -m pytest -q` + `check` + `docs-check --gate` 全绿后提交，再打标签 `v<版本>`（仓库约定：每个版本一个标签）。
5. 本仓库**不 push**，除非 owner 明确要求。

## 同步面

左列是触发点，右列必须同改，同一提交内完成。

**机器副本**：`tools/vault.toml [docs_sync]`——id 与本表一一对应（`tests/test_docs.py` 断言两边 id 集合相等）。
`python3 tools/vault.py docs-check [--against REV] [--gate]` 按它 diff 工作区，报出触发但没连带改的文件：
默认报告级（exit 0），`--gate` 才 exit 1。

探针是**精确的**，不是「文件碰了就红」：`rules.py` 只改注释不触发 T2；`cli.py` 只改实现、不动子命令名不触发 T5。
没有探针的行（T3、T6–T9）在 `docs-check` 里列为 `manual`——机器看不见，只能靠本表。

探针**覆盖不到**的地方，写在这里免得被误信：

- **T2 只比对判据 id 集合**：`*_note` 说明文字改了不触发。G3 范围行就这么漏过一次——靠 `tests/test_cli.py` 把渲染文字钉到配置上兜住，其余靠纪律。
- **T5 只比对子命令名集合**：加旗标、改 `--help` 文案不触发。新增命令本身会被拦住（那是这套门的起点）。

| # | 触发改动 | 必须同步 | 探针 |
|---|---|---|---|
| T1 | `tools/vault.toml` | 无需改文档；核对 `cli.py` 的 `HELP_TOPICS` / epilog 是否引用了被改的键名 | 路径 |
| T2 | `tools/vaultkit/rules.py` 判据增删改名 | `README.md` §工具；`AGENTS.md` §Invariants；`doctrine/Agent Contract.md` §6；`doctrine/Vault Design.md` §判据两级制；`tools/vaultkit/cli.py`（`cmd_check` 头行、`help rawindex` 文案）；`a_sticker/or/记忆底座-首批卡片.md` 规则卡；`tests/` | 判据 id 集合 |
| T3 | 硬门增删 | 先要 owner 裁决 + `doctrine/Vault Design.md` §决策台账 新 D 号；再 T2 全部 + `tests/` + `.github/workflows/ci.yml` | manual（要人裁决） |
| T4 | `tools/vaultkit/model.py` 登记语义 / 主干模型 | `doctrine/Vault Design.md` §两棵树 + §关键 doctrine；`README.md` §两棵树；`AGENTS.md` 硬规则 3；`cli.py help dag` | 路径 |
| T5 | `cli.py` 子命令 / 旗标 / 退出码 | `README.md` §工具；`doctrine/Agent Contract.md` §1 + §Exit codes；`.agent/skills/vault-ops/SKILL.md`（流程节 + inline help 列表）；`cli.py` 顶层 epilog；`tests/` | 子命令名集合 |
| T6 | 体裁 / 分区规则 | `AGENTS.md` 硬规则 2、4；`doctrine/Vault Design.md` §区域；`README.md` §区域；记忆底座卡「体裁由什么决定」 | manual |
| T7 | 字段政策 | `AGENTS.md` 硬规则 4；`doctrine/Vault Design.md` §字段；`README.md` §最小记忆集；记忆底座卡「保留哪些 frontmatter 字段」 | manual |
| T8 | 模板政策 | `AGENTS.md` 硬规则 4；`doctrine/Vault Design.md` §字段；`README.md` §最小记忆集第 1 条 | manual |
| T9 | doctrine 任何语义变化 | `doctrine/Vault Design.md` §决策台账（新 D 号）；`a_sticker/or/记忆底座-首批卡片.md` 重新生成（该文件头部自带漂移规则） | manual |
| T10 | 本机 / Obsidian / 插件设置 | `doctrine/New Machine.md` §仓库里有的 vs 每机各异的 | 环境变量集合（`.obsidian/` 部分 manual） |
| T11 | 新增 doctrine 文件 | `AGENTS.md` §Source of truth；`README.md` §协作 + §Related Files；`doctrine/Vault Design.md` §区域；`.agent/skills/vault-ops/SKILL.md` §Load order；若新文件有自己的同步组，本表加一行 | 新增文件 |

## 自检

内容一致性由 `tests/test_docs.py` 强制（CI 跑 `pytest`，不过就红）：

| 检查 | 断言 |
|---|---|
| 判据 id 齐全 | 5 份文档（README / AGENTS / Vault Design / Agent Contract / 记忆底座卡）都点到 `RULES` 里的每个 id |
| 无幽灵 id | 扫描范围内出现的判据写法必须真的存在——v5 遗留的旧编号会红 |
| 无 id 区间 | 不许用区间简写（区间查不了成员，而且最先过期） |
| 配置值无副本 | 文档只写键名，不写数值或名字——阈值数值、fold 名（`tools/vault.toml [thresholds]` / `[zones]`） |
| 同步面 id 对齐 | `tools/vault.toml [docs_sync]` 的 id 集合 == 本表 id 集合 |
| 同步面目标存在 | 每行的 `sync` / `paths` 指向的文件真的在 |
| doctrine 头齐 | 每份 `doctrine/*.md` 有 `> 版本：` 与 `> 同步组：`，且引用的 T 号存在 |
| 子命令有用法 | 每个子命令要么有 `help <topic>`，要么在显式豁免表里（现在只有 `help` 自己） |
| 子命令被跑过 | 每个子命令在 fixture vault 上真跑一次——新子命令必须登记进 `BARE` 表才会被跑 |
| 子命令进技能 | 每个子命令名都出现在 `.agent/skills/vault-ops/SKILL.md` 里 |
| 环境变量被登记 | 代码读的环境变量集合一旦变化，`docs-check` 触发 T10，要求同步 `New Machine.md` |

「改了一处有没有连带改」由 `docs-check` 管（提交前跑，见 §同步面）：

```bash
python3 tools/vault.py docs-check --against HEAD          # 报告级：列出漏改
python3 tools/vault.py docs-check --against HEAD --gate   # 漏改则 exit 1
```

不需要 pytest 时的粗筛（只扫散文——下面围栏里的示例不会被上面的检查扫到）：

```bash
# 幽灵 id / id 区间
grep -rnE '(^|[^A-Za-z0-9_])(I[0-9]+[a-c]?|G[0-9]+)([^0-9A-Za-z_]|$)' README.md AGENTS.md doctrine/ tools/vaultkit/cli.py

# 阈值数值副本（只应命中 tools/vault.toml）
grep -rnE '(^|[^0-9])90([^0-9]|$)|0\.97|(^|[^0-9])0\.9([^0-9]|$)' README.md AGENTS.md doctrine/*.md .agent/skills/*/SKILL.md
```

## Related

- [[Vault Design]]
- [[Vault Workflow]]
- [[Agent Contract]]
- [[New Machine]]
