---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

# Hyprland Custom Workspace Config File for Headless Monitor

🌳 **导航**: [[Hyprland Workspace System - Tree Navigation]] > **配置管理** > **工作区配置中心** > **虚拟屏配置**

← [[Hyprland Custom Workspace Config File]]

模板参考：[[Hyprland Workspace Config Templates]]

## Text

>[!tip]
>模板源路径: `/.config/hypr/conf/custom/headless_workspace.conf.temp`
>
>运行时路径: `/.config/hypr/conf/custom/headless_workspace.conf`（每次由 `.temp` 生成）

```

# ==========================================
# 串流模式 (虚拟显示器配置)
# ==========================================

# 1. 定义虚拟屏幕 (Sunshine 必须先执行 hyprctl output create headless)
# 不要硬编码 HEADLESS-1，保留给脚本自动检测并替换占位符
# monitor = __HEADLESS_OUTPUT__, 1920x1080@60, auto, 1

# 2. 将工作区强绑定到虚拟屏幕
# 这样无论你怎么切，它们都会显示在检测到的 Headless 输出上
workspace = 1, monitor:__HEADLESS_OUTPUT__
workspace = 21, monitor:__HEADLESS_OUTPUT__

# 3. 按键绑定 (适配串流场景)

# --- 左右切换：在工作区 1 和 21 之间循环 ---
# 由于在串流中你只有这两个工作区，这样配置可以实现来回切换
bind = $mainMod CTRL, right, workspace, r+1
bind = $mainMod CTRL, left, workspace, r-1

# 左右移动窗口：将窗口移到下一个/上一个工作区
bind = $mainMod CTRL ALT, right, movetoworkspace, r+1
bind = $mainMod CTRL ALT, left, movetoworkspace, r-1

# --- 上下切换：直接跳转 ---
# 在串流中，这两个按键现在起到“在 1 和 21 之间瞬时跳转”的作用
bind = $mainMod CTRL, down, workspace, 21 
bind = $mainMod CTRL, up, workspace, 1

# 上下移动窗口
bind = $mainMod CTRL ALT, down, movetoworkspace, 21
bind = $mainMod CTRL ALT, up, movetoworkspace, 1

# ==========================================
# Window State & Special Workspace
# ==========================================

# 浮动与全屏控制
bind = $mainMod CTRL, F, togglefloating
bind = $mainMod, F, fullscreen, 0

# 特殊工作区 (Special Workspace) 控制
bind = $mainMod, S, togglespecialworkspace
bind = $mainMod CTRL ALT, S, movetoworkspace, special

# ~/.config/hypr/hyprland.conf
bind = CTRL ALT, Backspace, exec, /home/mia/.config/hypr/scripts/custom/to_default.sh

```

### 自动检测输出名并从 `.temp` 生成（避免硬编码）

这部分实现已经收敛到 [[script toggle_workspace_conf]]，本页只保留配置语义：Headless 运行时配置应由 `.temp` 生成，并通过 `__HEADLESS_OUTPUT__` 占位符注入实际输出名。

---

## Thoughts

## 更新记录
- 2026-05-04: 移除对 `HEADLESS-1` 的硬编码，改用 `__HEADLESS_OUTPUT__` 占位符与脚本检测替换流程；文档示例包含从 `.temp` 生成运行配置的命令与检测片段。
- 注意：本文档为配置模版与使用说明，脚本示例在 `archives/tricks/script toggle_workspace_conf.md` 中。实际脚本尚未部署到 `~/.config/hypr/scripts/custom/`。
