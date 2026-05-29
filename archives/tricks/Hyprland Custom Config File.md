---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/technique
---

# Hyprland Custom Config File

🌳 **导航**: [[Hyprland Workspace System - Tree Navigation]] > **配置管理** > **主配置**

> [!summary]
> 这是 Hyprland 的**主入口配置文件**，集成了所有工作空间脚本、快捷键绑定和系统启动配置。

---

## 📁 系统文件位置

| 用途             | 路径                                                   |
| -------------- | ---------------------------------------------------- |
| **主配置**        | `~/.config/hypr/conf/custom.conf`                    |
| **工作区配置**      | `~/.config/hypr/conf/custom_workspace.conf` (符号链接)   |
| **默认配置**       | `~/.config/hypr/conf/custom/default_workspace.conf`  |
| **Headless配置** | `~/.config/hypr/conf/custom/headless_workspace.conf` |
| **脚本目录**       | `~/.config/hypr/scripts/custom/`                     |
| **状态目录**       | `~/.config/hypr/state/`                              |
| **日志目录**       | `~/.config/hypr/logs/`                               |

---

## 🔗 完整依赖关系图

### 📜 依赖的脚本文件 (12个)

#### **核心脚本** ⭐ 必需

| 脚本名 | 功能 | 启动方式 | 参考 |
|--------|------|---------|------|
| `ws-lib.sh` | 17+ 个共用函数库 | 被其他脚本 source | [[ws-lib.sh]] |
| `ws-init.sh` | 一次性初始化系统 | exec-once 启动 | [[ws-init.sh]] |
| `ws-monitor.sh` | 实时后台监控显示器变化 | exec-once ... & | [[ws-monitor.sh]] |

#### **工作空间切换脚本**

| 脚本名 | 功能 | 快捷键 | 参考 |
|--------|------|--------|------|
| `ws-quick-toggle.sh` | 快速切换 default ↔ headless | Super+Shift+T | [[ws-quick-toggle.sh]] |
| `to_default.sh` | 切换到物理屏模式 | Super+Shift+D | [[to_default.sh]] |
| `to_headless.sh` | 切换到虚拟屏模式 | Super+Shift+H | [[to_headless.sh]] |

#### **诊断与修复脚本**

| 脚本名 | 功能 | 快捷键 | 参考 |
|--------|------|--------|------|
| `ws-debug.sh` | 系统诊断（7个命令） | Ctrl+Shift+V (verify) | [[ws-debug.sh]] |
| `ws-repair.sh` | 自动修复系统状态不一致 | Ctrl+Shift+R --aggressive | [[ws-repair.sh]] |

#### **高级功能脚本**

| 脚本名 | 功能 | 执行方式 | 参考 |
|--------|------|---------|------|
| `ws-profile.sh` | 配置快照管理 | 手动执行 | [[ws-profile.sh]] |
| `ws-export-config.sh` | 配置导出(JSON/YAML) | 手动执行 | [[ws-export-config.sh]] |
| `ws-migrate.sh` | 跨机器迁移 | 手动执行 | [[ws-migrate.sh]] |
| `ws-performance.sh` | 性能测试与优化 | 手动执行 | [[ws-performance.sh]] |

### 📋 依赖的配置文件 (2个)

| 配置文件                      | 用途         | 指向对象         | 创建基础                | 参考                                                                                                                 |
| ------------------------- | ---------- | ------------ | ------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `default_workspace.conf`  | 物理显示器工作区配置 | 工作空间、布局、绑定等  | 从 custom.conf 复制并修改 | [[Hyprland Custom Workspace Config File for 1 Monitor]] 或 [[Hyprland Custom Workspace Config File for 2 Monitors]] |
| `headless_workspace.conf` | 虚拟显示器工作区配置 | 虚拟屏工作空间、分辨率等 | 从 custom.conf 复制并修改 | [[Hyprland Custom Workspace Config File for Headless Monitor]]                                                     |

### 🔀 符号链接依赖

```
核心符号链接：
~/.config/hypr/conf/custom_workspace.conf 
    ├─ 初始状态 → ~/.config/hypr/conf/custom/default_workspace.conf
    └─ 切换时改变 → ~/.config/hypr/conf/custom/headless_workspace.conf
    
创建命令：
ln -sfn ~/.config/hypr/conf/custom/default_workspace.conf ~/.config/hypr/conf/custom_workspace.conf
```

---

## 🎯 依赖加载顺序

```
1️⃣  启动变量定义
    ├─ $mainMod = SUPER
    ├─ $HYPRSCRIPTS = ~/.config/hypr/scripts
    └─ $SCRIPTS = ~/.config/ml4w/scripts

2️⃣  启动应用程序 (exec-once)
    ├─ fcitx5 (输入法)
    ├─ clash-verge (代理)
    └─ easyeffects (音频)

3️⃣  配置环境变量
    └─ http_proxy, https_proxy 等代理设置

4️⃣  加载工作区配置
    └─ source ~/.config/hypr/conf/custom_workspace.conf
       (此时符号链接必须已存在)

5️⃣  绑定快捷键
    ├─ 工作空间切换快捷键 (6个)
    ├─ 应用启动快捷键 (4个)
    ├─ 诊断修复快捷键 (2个)
    └─ 截图快捷键 (3个)

6️⃣  系统兼容性配置
    ├─ xwayland { force_zero_scaling = true }
    └─ dwindle { pseudotile = true }

7️⃣  启动核心脚本 (exec-once)
    ├─ ws-init.sh (初始化)
    └─ ws-monitor.sh & (后台监控)
```

---

## ⌨️ 快捷键绑定完整列表

### 工作空间管理快捷键 ⭐ 最常用

| 快捷键 | 绑定脚本 | 功能描述 | 调用类型 |
|--------|---------|---------|---------|
| **Super+Shift+T** | ws-quick-toggle.sh | 快速在 default ↔ headless 间切换 | exec, 一步切换 |
| **Super+Shift+D** | to_default.sh | 切换到物理屏模式 | exec, 完整切换 |
| **Super+Shift+H** | to_headless.sh | 切换到虚拟屏模式 | exec, 完整切换 |
| **Super+Shift+S** | ws-debug.sh status | 显示当前工作空间状态 | exec, 仅查看信息 |

### 系统诊断与修复快捷键 🔧

| 快捷键 | 绑定脚本 | 功能描述 | 注意事项 |
|--------|---------|---------|---------|
| **Ctrl+Shift+V** | ws-debug.sh verify | 验证系统完整性 | 只检查，不修改 |
| **Ctrl+Shift+R** | ws-repair.sh --aggressive | 自动修复系统不一致 | 强制修复模式，可能影响当前状态 |

### 应用启动快捷键

| 快捷键 | 应用程序 | 说明 |
|--------|---------|------|
| Super+B | google-chrome-stable | 打开浏览器 |
| Super+C | code | 打开代码编辑器 (VS Code) |
| Super+R | rofi -show run | 应用启动器 |
| Super+O | obsidian | 打开笔记应用 |

### 截图快捷键

| 快捷键 | 脚本调用 | 功能 |
|--------|---------|------|
| Super+P | screenshot.sh | 截图菜单（选择模式） |
| Super+Alt+P | screenshot.sh --instant | 整屏截图 |
| Super+Shift+P | screenshot.sh --instant-area | 区域截图 |

---

## 📊 配置文件内容分解

### 第一部分：路径变量定义
```bash
$mainMod = SUPER
$HYPRSCRIPTS = ~/.config/hypr/scripts
$SCRIPTS = ~/.config/ml4w/scripts
```

### 第二部分：应用自动启动
```bash
exec-once = fcitx5
exec-once = clash-verge
exec-once = easyeffects
exec-once = /usr/lib/pam_kwallet_init
```

### 第三部分：代理环境变量
```bash
env = http_proxy,http://127.0.0.1:7897
env = https_proxy,http://127.0.0.1:7897
```

### 第四部分：工作区配置加载 ⭐ 关键步骤
```bash
source = ~/.config/hypr/conf/custom_workspace.conf
```

### 第五部分：快捷键绑定 (15个快捷键)
所有 bind 命令，绑定 15 个快捷键

### 第六部分：系统兼容性配置
```bash
xwayland { force_zero_scaling = true }
dwindle { pseudotile = true }
```

### 第七部分：系统启动脚本 ⭐ 关键步骤
```bash
exec-once = ~/.config/hypr/scripts/custom/ws-init.sh
exec-once = ~/.config/hypr/scripts/custom/ws-monitor.sh &
```

---

## 📌 部署前检查清单

### 必需项目
- [ ] 所有12个脚本文件已复制到 `~/.config/hypr/scripts/custom/`
- [ ] 所有脚本已设置执行权限: `chmod +x ~/.config/hypr/scripts/custom/*.sh`
- [ ] `default_workspace.conf` 已从 custom.conf 复制
- [ ] `headless_workspace.conf` 已创建
- [ ] 符号链接已创建

### 目录验证
- [ ] `~/.config/hypr/conf/custom/` 目录存在
- [ ] `~/.config/hypr/scripts/custom/` 目录存在
- [ ] `~/.config/hypr/state/` 目录存在
- [ ] `~/.config/hypr/logs/` 目录存在

### 配置文件验证
- [ ] `~/.config/hypr/conf/custom.conf` 存在且语法正确
- [ ] `default_workspace.conf` 包含工作空间定义
- [ ] `headless_workspace.conf` 包含虚拟屏配置

---

## 🧩 配置模板（独立维护）

模板内容已拆分到独立笔记，避免主配置页与子配置页重复维护。

- 模板中心：[[Hyprland Workspace Config Templates]]
- 子配置中心：[[Hyprland Custom Workspace Config File]]
- 单屏子配置：[[Hyprland Custom Workspace Config File for 1 Monitor]]
- 双屏子配置：[[Hyprland Custom Workspace Config File for 2 Monitors]]
- 虚拟屏子配置：[[Hyprland Custom Workspace Config File for Headless Monitor]]

> [!tip]
> 维护策略：主笔记只保留“依赖关系和使用方式”，模板细节统一在 [[Hyprland Workspace Config Templates]] 维护。

---

## 重要注意事项

> [!warning] 符号链接必需
> 配置加载依赖符号链接的存在。必须手动创建：
> ```bash
> ln -sfn ~/.config/hypr/conf/custom/default_workspace.conf ~/.config/hypr/conf/custom_workspace.conf
> ```

> [!warning] 执行权限必需
> 所有脚本都需要执行权限，否则无法运行：
> ```bash
> chmod +x ~/.config/hypr/scripts/custom/*.sh
> ```

> [!tip] 工作区配置创建
> 需要从现有 custom.conf 复制并根据显示器配置修改：
> ```bash
> cp ~/.config/hypr/conf/custom.conf ~/.config/hypr/conf/custom/default_workspace.conf
> cp ~/.config/hypr/conf/custom.conf ~/.config/hypr/conf/custom/headless_workspace.conf.temp
> ```
> 切换到虚拟屏前，先从 `headless_workspace.conf.temp` 生成 `headless_workspace.conf`。

> [!info] 监控脚本
> `ws-monitor.sh` 在后台运行（注意末尾的 `&`），持续监控系统状态变化

---

## 相关文档链接

| 类型 | 链接 | 说明 |
|------|------|------|
| 📖 集成指南 | [[Hyprland Config File with Scripts]] | 脚本集成完整指南 |
| 🗺️ 配置中心 | [[Hyprland Custom Workspace Config File]] | 工作区配置中心 hub |
| 📍 系统规划 | [[Hyprland Workspace Config 优化系统 - 完整地图]] | 整体系统架构和规划 |
| 🌳 导航 | [[Hyprland Workspace System - Tree Navigation]] | 所有文档的树形导航 |
| 📊 脚本库 | [[ws-lib.sh]] | 所有脚本的共用函数库 |
