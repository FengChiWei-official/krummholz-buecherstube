---
tags:
  - status/evergreen
  - topic/learning
  - type/tips
  - type/lit
---

## 使用 `xrandr` 命令
1. **找到 SDDM 脚本**: 登录界面通常在 X11 会话启动前运行 `/usr/share/sddm/scripts/Xsetup`。
2. **编辑脚本**: 用文本编辑器打开 `Xsetup` 文件（通常需要 root权限）。
3. **添加旋转命令**: 在脚本末尾添加你想要的 `xrandr` 命令。
    - **向左旋转 90°**: `xrandr --output <显示器名> --rotate left`
    - **向右旋转 90°**: `xrandr --output <显示器名> --rotate right`
    - **倒置 (180°)**: `xrandr --output <显示器名> --rotate inverted`
    - **恢复正常**: `xrandr --output <显示器名> --rotate normal`



---
## **related**：