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
# # ==========================================
# Workspace & Monitor Configuration
# ==========================================

# 解绑原有冲突按键
unbind = $mainMod CTRL, right
unbind = $mainMod CTRL, left
unbind = $mainMod TAB
unbind = $mainMod CTRL, down
unbind = $mainMod CTRL, up


# --- 2. 左右切换：同一屏幕内切换工作区 ---
# 使用 m+1 和 m-1 代表只在“当前显示器 (monitor)”所属的工作区之间循环
bind = $mainMod CTRL, right, workspace, r+1
bind = $mainMod CTRL, left, workspace, r-1

# 左右移动窗口：将窗口移到同一屏幕的下一个/上一个工作区
bind = $mainMod CTRL ALT, right, movetoworkspace, r+1
bind = $mainMod CTRL ALT, left, movetoworkspace, r-1

# --- 3. 上下切换：不同屏幕（显示器）之间切换 ---
# focusmonitor +1 / -1 用于在物理显示器之间切换焦点
bind = $mainMod CTRL, down, workspace, 21 
bind = $mainMod CTRL, up, workspace, 1

# 上下移动窗口：将当前窗口发送到下一个/上一个屏幕（显示器）
bind = $mainMod CTRL ALT, down, movetoworkspace, 21
bind = $mainMod CTRL ALT, up, movetoworkspace, 1

# ==========================================
# Window State & Special Workspace
# ==========================================

# 浮动与全屏控制
unbind = $mainMod, F
unbind = $mainMod CTRL, F
bind = $mainMod CTRL, F, togglefloating
bind = $mainMod, F, fullscreen, 0

# 特殊工作区 (Special Workspace) 控制
unbind = $mainMod, S
unbind = $mainMod CTRL ALT, S
bind = $mainMod, S, togglespecialworkspace
bind = $mainMod CTRL ALT, S, movetoworkspace, special

```
---

## Thoughts
