---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text
**标题：** 终端与Shell环境配置修复  
**标签：** #Linux #EndeavourOS #Fish #终端

**问题描述：**  
终端启动时出现 oh-my-posh 路径错误，提示无法找到指定文件。

**根源分析：**  
ML4W 配置文件中将 oh-my-posh 的路径硬编码为了 $HOME/.local/bin/oh-my-posh。当系统通过包管理器（如 Pacman/Yay）全局安装该程序时，实际路径位于 /usr/bin/oh-my-posh，导致脚本找不到执行文件。

**修复方案：**  
修改 Shell 初始化脚本，移除绝对路径，改为动态查找。

codeBash

```
# 执行以下命令进行替换
sed -i 's|\$HOME/.local/bin/oh-my-posh|oh-my-posh|g' ~/.config/fish/conf.d/20-customization.fish
```

完成后重新打开终端即可生效。

---

## Thoughts
