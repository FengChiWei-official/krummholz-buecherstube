---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
aliases:
  - Clash work properly in hyprland, however, proxy dont work
---

## Text
**标题：** Hyprland 环境代理配置  
**标签：** #Hyprland #代理 #Clash #环境变量

**问题描述：**  
在 Hyprland 下，应用程序无法感知代理设置，导致网络连接异常。

**根源分析：**  
KDE 等完整的桌面环境会自动处理代理服务的环境变量传递，而 Hyprland 作为窗口管理器需要用户手动声明环境变量，以确保所有子进程继承代理设置。

**配置方法：**  
在 ~/.config/hypr/conf/environments.conf (或主配置文件) 中添加以下环境变量：

codeIni

```
# 设置全局代理指向 Clash 端口
env = http_proxy,http://127.0.0.1:7890
env = https_proxy,http://127.0.0.1:7890
env = all_proxy,socks5://127.0.0.1:7890
env = no_proxy,localhost,127.0.0.1,local
```

**验证方法：**  
执行 env | grep -i proxy，检查是否有 7890 端口的相关输出。

---

## Thoughts
