---
tags:
  - type/lit
  - topic/learning
  - status/archive
  - attr/views
source: Workspace practice
---

# Hyprland Workspace Config Templates

🌳 **导航**: [[Hyprland Workspace System - Tree Navigation]] > **配置管理** > **工作区配置中心** > **配置模板**

← [[Hyprland Custom Workspace Config File]]

> [!summary]
> 这是工作区配置模板集合：把模板和具体子配置分开管理，便于迁移、回滚和自动切换。

## 模板文件约定

- `~/.config/hypr/conf/custom/single_workspace.conf`：单屏模板
- `~/.config/hypr/conf/custom/multi_workspace.conf`：多屏模板
- `~/.config/hypr/conf/custom/headless_workspace.conf.temp`：虚拟屏模板源（固定保留）
- `~/.config/hypr/conf/custom/headless_workspace.conf`：虚拟屏运行配置（每次由 `.temp` 生成）
- `~/.config/hypr/conf/custom/default_workspace.conf`：当前默认场景入口（由 single/multi 映射）
- `~/.config/hypr/conf/custom_workspace.conf`：Hyprland source 入口（符号链接）

## 主入口模板（custom.conf）

这部分主配置正文已经统一收敛到 [[Hyprland Custom Config File]]，本页只保留模板关系：

- `custom.conf` 是主入口
- `custom_workspace.conf` 是被 `source` 的切换入口
- 快捷键与 `exec-once` 的具体代码只在主配置笔记中维护一次

## 单屏模板（single_workspace.conf）

```bash
# TEMPLATE: SINGLE MONITOR
# 替换 eDP-1 为你的实际输出名
monitor = eDP-1, preferred, auto, 1

workspace = 1, monitor:eDP-1
workspace = 2, monitor:eDP-1
workspace = 3, monitor:eDP-1
workspace = 4, monitor:eDP-1
workspace = 5, monitor:eDP-1
```

## 多屏模板（multi_workspace.conf）

```bash
# TEMPLATE: MULTI MONITOR
# 替换 eDP-1 / HDMI-A-1 为你的实际输出名
monitor = eDP-1, preferred, auto, 1
monitor = HDMI-A-1, preferred, auto-right, 1

workspace = 1, monitor:eDP-1
workspace = 2, monitor:eDP-1
workspace = 3, monitor:HDMI-A-1
workspace = 4, monitor:HDMI-A-1
workspace = 5, monitor:eDP-1
```

## Headless 模板源（headless_workspace.conf.temp）

```bash
# TEMPLATE: HEADLESS
# 不要硬编码 HEADLESS-1，使用占位符并由脚本替换
# 例如替换为 HEADLESS-1 / HEADLESS-2 等真实输出名
workspace = 1, monitor:__HEADLESS_OUTPUT__
workspace = 2, monitor:__HEADLESS_OUTPUT__
workspace = 3, monitor:__HEADLESS_OUTPUT__
workspace = 4, monitor:__HEADLESS_OUTPUT__
workspace = 5, monitor:__HEADLESS_OUTPUT__
```

### Headless 输出名自动检测（推荐）

这部分的实现细节已经统一放到 [[script toggle_workspace_conf]] 中；这里仅保留约定：切换时先从 `.temp` 生成 `headless_workspace.conf`，再替换 `__HEADLESS_OUTPUT__`。

## 模板落地步骤

模板落地和脚本生成已经统一交给 [[script toggle_workspace_conf]]，本页不再重复写安装命令或生成片段，以避免多重信源。
## 脚本部署示例
部署与脚本内容请直接查看 [[script toggle_workspace_conf]]；这里不再重复写出可执行代码，避免出现多重信源。
```

## 同类子配置

- [[Hyprland Custom Workspace Config File for 1 Monitor]]
- [[Hyprland Custom Workspace Config File for 2 Monitors]]
- [[Hyprland Custom Workspace Config File for Headless Monitor]]

## 更新记录
- 2026-05-04: 将 Headless 工作流规范化为保留 `.temp` 模板（`headless_workspace.conf.temp`），并推荐使用脚本在切换时从 `.temp` 生成 `headless_workspace.conf`，再通过 `ln -sfn` 指向 `custom_workspace.conf` 后重载 Hyprland。
- 注意：文档中包含脚本模板示例（`to_headless` / `to_default`），但这些示例最初只写入笔记；如果需要，我可以把它们部署为 `~/.config/hypr/scripts/custom/` 下的可执行脚本。

## Related

- [[Hyprland Custom Config File]]
- [[Hyprland Custom Workspace Config File]]
- [[Hyprland Workspace Config 优化系统 - 完整地图]]
