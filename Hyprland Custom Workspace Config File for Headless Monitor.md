---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text

>[!tip]
>In path `/.config/hypr/conf/custom/default_workspace.conf`

```

# ==========================================
# 串流模式 (虚拟显示器配置)
# ==========================================

# 1. 定义虚拟屏幕 (Sunshine 必须先执行 hyprctl output create headless)
monitor = HEADLESS-1, 1920x1080@60, auto, 1

# 2. 将工作区强绑定到虚拟屏幕
# 这样无论你怎么切，它们都会显示在 HEADLESS-1 上
workspace = 1, monitor:HEADLESS-1
workspace = 21, monitor:HEADLESS-1

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

:
```

---

## Thoughts