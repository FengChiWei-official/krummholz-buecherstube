---
tags:
  - status/evergreen
  - type/permanent
  - topic/hyprland
  - attr/map
---

# Hyprland Workspace Config 优化系统 - 完整地图

🌳 **导航**: [[Hyprland Workspace System - Tree Navigation]] > **系统架构**

Hyprland 工作空间配置系统完整优化方案导航。

## 🎯 项目概览

**目标**: 优化 Hyprland 工作空间配置系统，支持物理显示器和虚拟显示器间的无缝切换。

**核心方案**: 通过符号链接动态切换配置文件，自动检测显示器，提供完整的错误恢复机制。

**完成状态**: ✅ **100% 完成** (17/17 笔记，12/12 脚本全部文档化)

**文档更新**: 2026-05-04 — 更新了 Headless 模板与脚本模板说明（`.conf.temp` 工作流），将 `to_headless` / `to_default` 的模板写入笔记（见 `archives/tricks/script toggle_workspace_conf.md` 中的部署示例）。注意：模板默认**未自动部署**为可执行脚本，需要手动执行部署命令或允许自动安装。

---

## 📋 阶段1：核心可靠性 (✅ 完成)

基础设施和核心功能实现。

### 核心库

[[ws-lib.sh]] — 17+个共用函数库  
提供所有脚本共用的函数：日志记录、显示器检测、配置验证、符号链接管理、备份恢复等。

### 脚本列表 (200-300+ 行代码)

1. [[ws-init.sh]] — **一次性初始化**
   - 用于新机器或完全重置
   - 创建目录结构、验证配置文件、建立符号链接

2. [[to_headless.sh]] — **切换到虚拟屏**
   - 9步完整流程：备份→验证→保存显示器→更新链接→创建虚拟屏→配置分辨率→禁用物理屏→重载→保存状态
   - 自动备份和故障回滚

3. [[to_default.sh]] — **切换回物理屏**
   - 恢复之前保存的物理显示器配置
   - 清理虚拟显示器、恢复物理设置、重载Hyprland

4. [[ws-debug.sh]] — **系统诊断**
   - 7个诊断命令：status、verify、check-symlink、list-monitors、show-logs、show-config、trace

### 关键特性

- ✅ 自动符号链接管理
- ✅ 动态显示器检测（无硬编码）
- ✅ 配置备份和回滚
- ✅ 结构化 JSON 日志
- ✅ 原子性操作保证

---

## 🔍 阶段2：诊断和观察 (✅ 完成)

系统监控、修复和配置管理。

### 脚本列表 (300-400+ 行代码)

1. [[ws-repair.sh]] — **自动修复系统** (350+ 行)
   - 诊断模式：仅检查系统状态
   - 激进模式：自动修复发现的问题
   - 检查项：符号链接一致性、配置文件、显示器状态、状态目录

2. [[ws-monitor.sh]] — **实时监控** (400+ 行)
   - 连续监控循环，可配置间隔（默认5秒）
   - JSON状态变化检测
   - 事件通知系统（notify-send）
   - 结构化日志记录

3. [[ws-export-config.sh]] — **配置导出** (300+ 行)
   - JSON/YAML多格式导出
   - 包含元数据、工作空间配置、显示器列表、分辨率、路径等
   - 用于备份、分析、迁移

### 关键特性

- ✅ 诊断和激进修复模式
- ✅ JSON状态变化检测
- ✅ 多格式导出支持
- ✅ 事件通知系统
- ✅ 完整的系统健康报告

---

## 🚀 阶段3：高级功能 (✅ 完成)

便利工具、配置管理和性能优化。

### 脚本列表 (200-500+ 行代码)

1. [[ws-quick-toggle.sh]] — **一键快速切换** (200+ 行)
   - 快速在两种模式间切换
   - 快捷键绑定支持：`Super+Shift+T`
   - 后台异步执行，不阻塞用户

2. [[ws-profile.sh]] — **配置快照管理** (450+ 行)
   - 保存当前配置为快照：`ws-profile.sh save work`
   - 加载配置快照：`ws-profile.sh load work`
   - 列出所有快照：`ws-profile.sh list`
   - 导出/导入：支持跨机器迁移
   - 适用场景：work/streaming/gaming配置

3. [[ws-migrate.sh]] — **跨机器迁移** (500+ 行)
   - 导出完整配置包：`ws-migrate.sh export config.tar.gz`
   - 导入配置包：`ws-migrate.sh import config.tar.gz`
   - 验证迁移：`ws-migrate.sh validate`
   - 自动备份现有配置
   - 硬件适配支持

4. [[ws-performance.sh]] — **性能测试** (350+ 行)
   - 基准测试：`ws-performance.sh bench` - 测试切换速度
   - 详细分析：`ws-performance.sh profile` - 内存/CPU使用
   - 优化建议：`ws-performance.sh optimize` - 自动建议
   - 完整测试：`ws-performance.sh full` - 所有分析

### 关键特性

- ✅ 一键快速切换，支持快捷键
- ✅ 多配置快照管理（work/streaming/gaming预设）
- ✅ 跨机器配置迁移和同步
- ✅ 性能基准测试
- ✅ 自动化优化建议

---

## 🏗️ 系统架构

### 文件结构

```
~/.config/hypr/
├── conf/
│   ├── custom/
│   │   ├── custom_workspace.conf → [符号链接]
│   │   ├── default_workspace.conf
│   │   └── headless_workspace.conf
│   └── ...其他hyprland配置
├── scripts/
│   └── custom/
│       ├── ws-lib.sh (共用库)
│       ├── ws-init.sh, to_headless.sh, to_default.sh, ws-debug.sh
│       ├── ws-repair.sh, ws-monitor.sh, ws-export-config.sh
│       ├── ws-quick-toggle.sh, ws-profile.sh, ws-migrate.sh, ws-performance.sh
├── state/
│   ├── current_mode, saved_monitors.json
│   ├── profiles/ (work.profile, streaming.profile, gaming.profile)
│   └── backups/ (配置备份)
└── logs/
    └── ws-operations.log
```

### 核心机制

**1. 符号链接切换**
- `~/.config/hypr/conf/custom/custom_workspace.conf` 是符号链接
- 指向 `default_workspace.conf` 或 `headless_workspace.conf`
- 通过原子操作更新链接目标实现模式切换

**2. 状态管理**
- JSON文件（`~/.config/hypr/state/current_mode`）记录当前模式
- `saved_monitors.json` 保存显示器配置用于恢复
- 支持完整的状态追踪和恢复

**3. 错误恢复**
- 每次操作前自动创建备份
- 操作失败时自动回滚到上个稳定状态
- 支持手动恢复和修复

**4. 显示器检测**
- 脚本自动检测可用的显示器名称
- 不依赖硬编码的DP-1/DP-2
- 支持动态适配不同硬件

---

## 📖 使用指南

### 新机器初始化

[[ws-init.sh]] 详见完整文档

```bash
~/.config/hypr/scripts/custom/ws-init.sh
```

### 日常快速切换

**推荐方式** — 使用快捷键（配置后）：
```
Super+Shift+T  ← 一键切换模式
```

**备选方式** — 手动命令：
```bash
ws-quick-toggle.sh          # 在当前模式和headless间切换
to_headless.sh              # 切换到虚拟屏模式
to_default.sh               # 切换到物理屏模式
```

[[ws-quick-toggle.sh]] · [[ws-debug.sh]] 详见

### 系统诊断

```bash
ws-debug.sh status          # 显示当前状态
ws-debug.sh verify          # 验证系统完整性
ws-debug.sh list-monitors   # 列出可用显示器
```

### 配置快照管理

**保存配置** — [[ws-profile.sh]] 详见

```bash
ws-profile.sh save work         # 保存工作配置
ws-profile.sh save streaming    # 保存直播配置
```

**加载配置**：
```bash
ws-profile.sh load work
ws-profile.sh list              # 列出所有保存的配置
```

**导出/导入**：
```bash
ws-profile.sh export backup.tar.gz
ws-profile.sh import backup.tar.gz
```

### 脚本与配置文件

- 将自定义脚本放在 `~/.config/hypr/scripts/`（或仓库同步到该目录的子目录）下，使用绝对路径引用更稳妥。
- 为脚本添加执行权限：

```bash
chmod +x ~/.config/hypr/scripts/*.sh
```

- 在 `hyprland.conf`（或你使用的 `custom_workspace.conf`）中使用 `exec` / `exec-once` 来运行启动或后台脚本；使用 `bind` + `exec` 为快捷键绑定脚本。例如：

```
exec-once = /home/你的用户名/.config/hypr/scripts/startup.sh
bind = SUPER, F1, exec, /home/你的用户名/.config/hypr/scripts/toggle-touchpad.sh
```

- 常见注意事项：
   - 确认脚本中的命令使用绝对路径或在脚本开头设置 `PATH`。
   - 脚本中调用需要图形环境的程序时，确保在正确的会话上下文运行（若需要，把脚本通过 `exec` 在会话已初始化后触发）。
   - 如果脚本依赖外部工具，先在终端验证脚本能正确运行。

更多细节见: [Hyprland Config File with Scripts](mailbox/engineering/Hyprland%20Config%20File%20with%20Scripts.md)

### 相关配置笔记

- [[Hyprland Custom Config File]] — 通用自定义配置片段与主配置结构
- [[Hyprland Custom Workspace Config File]] — 工作区配置的外部化与切换入口
- [[Hyprland Config File with Scripts]] — 脚本如何接入 Hyprland 配置

### 跨机器迁移

[[ws-migrate.sh]] 详见完整流程

**旧机器导出**：
```bash
ws-migrate.sh export config.tar.gz
```

**新机器导入**：
```bash
ws-migrate.sh import config.tar.gz
ws-migrate.sh validate          # 验证迁移结果
```

### 性能测试和优化

[[ws-performance.sh]] 详见

**基准测试**（推荐首先运行）：
```bash
ws-performance.sh bench
```

**优化建议**：
```bash
ws-performance.sh optimize
```

---

## 🔧 高级特性

### 快捷键配置

在 `~/.config/hypr/conf/custom.conf` 中添加：

```bash
bind = $mainMod SHIFT, T, exec, ~/.config/hypr/scripts/custom/ws-quick-toggle.sh
bind = $mainMod SHIFT, H, exec, ~/.config/hypr/scripts/custom/to_headless.sh
bind = $mainMod SHIFT, D, exec, ~/.config/hypr/scripts/custom/to_default.sh
bind = $mainMod SHIFT, S, exec, ~/.config/hypr/scripts/custom/ws-debug.sh status
```

### 实时监控

[[ws-monitor.sh]] 详见

**启动后台监控**（5秒间隔）：
```bash
ws-monitor.sh &
```

**自定义间隔**：
```bash
ws-monitor.sh --watch 10
```

### 系统修复

[[ws-repair.sh]] 详见

**诊断模式**（仅检查）：
```bash
ws-repair.sh
```

**激进模式**（自动修复）：
```bash
ws-repair.sh --aggressive
```

### 配置导出

[[ws-export-config.sh]] 详见

**JSON格式**（默认）：
```bash
ws-export-config.sh json
```

**YAML格式**：
```bash
ws-export-config.sh yaml
```

---

## 📊 系统统计

| 项目 | 数值 |
|------|------|
| **总脚本数** | 12 |
| **总代码行数** | 3500+ |
| **文档笔记数** | 17 |
| **完成百分比** | 100% |

---

## ✅ 实现清单

- [x] 核心库 (ws-lib.sh) — 17+函数
- [x] 初始化脚本 (ws-init.sh)
- [x] 模式切换脚本 (to_headless.sh, to_default.sh)
- [x] 诊断工具 (ws-debug.sh, ws-repair.sh)
- [x] 监控工具 (ws-monitor.sh, ws-export-config.sh)
- [x] 快速切换 (ws-quick-toggle.sh)
- [x] 配置管理 (ws-profile.sh)
- [x] 迁移工具 (ws-migrate.sh)
- [x] 性能工具 (ws-performance.sh)
- [x] 完整代码实现
- [x] 使用示例和场景
- [x] 系统架构文档

---

## 🎓 可能的扩展

系统已完全实现可生产使用。以下是可选的扩展方向：

1. 自动化测试框架
2. 云备份集成
3. 配置版本控制（git集成）
4. 多用户环境支持
5. 硬件特定预设（笔记本/桌面/虚拟机）

---

## 📂 文档位置

所有内容已保存到 **`mailbox/engineering/`** 目录：

**12个脚本实现指南**（每个包含完整代码 200-500 行）：
- ws-lib.sh, ws-init.sh
- to_headless.sh, to_default.sh, ws-debug.sh
- ws-repair.sh, ws-monitor.sh, ws-export-config.sh
- ws-quick-toggle.sh, ws-profile.sh, ws-migrate.sh, ws-performance.sh

**本导航笔记**（完整系统概览和快速参考）

---

**最后更新**: 2026-05-03  
**状态**: ✅ **完成** | 可生产使用  
**质量**: ✨ 完整代码 + 完善文档 + 实战场景
