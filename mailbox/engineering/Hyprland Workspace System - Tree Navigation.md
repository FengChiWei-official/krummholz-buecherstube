---
tags:
  - status/evergreen
  - type/permanent
  - topic/hyprland
  - attr/map
---

# Hyprland Workspace System - Tree Navigation

完整的 Hyprland 工作空间配置系统导航树。

---

## 🌳 完整导航树

```
Hyprland Workspace System
│
├─ 📖 快速开始 (START HERE)
│  ├─ [[Hyprland Config File with Scripts]] — 初始化步骤（6步）
│  └─ [[Hyprland Custom Config File]] — 快捷键绑定模板
│
├─ 🏗️ 系统架构与规划
│  └─ [[Hyprland Workspace Config - Optimization Map]] — 完整系统概览与阶段分解
│
├─ ⚙️ 配置管理
│  ├─ [[Hyprland Custom Config File]] — 主配置入口
│  ├─ [[Hyprland Custom Workspace Config File]] — 工作区配置中心
│  │  ├─ [[Hyprland Workspace Config Templates]] — 配置模板中心
│  │  ├─ [[Hyprland Custom Workspace Config File for 1 Monitor]] — 单显示器
│  │  ├─ [[Hyprland Custom Workspace Config File for 2 Monitors]] — 双显示器
│  │  └─ [[Hyprland Custom Workspace Config File for Headless Monitor]] — 虚拟屏
│  └─ [[Hyprland Config File with Scripts]] — 脚本集成与快捷键
│
├─ 🔧 脚本实现
│  ├─ 📚 共用库
│  │  └─ [[ws-lib.sh]] — 17+ 个共用函数
│  │
│  ├─ 🟢 阶段1：核心可靠性 (4个脚本)
│  │  ├─ [[ws-init.sh]] — 一次性初始化
│  │  ├─ [[to_headless.sh]] — 切换到虚拟屏（9步）
│  │  ├─ [[to_default.sh]] — 切换回物理屏（7步）
│  │  └─ [[ws-debug.sh]] — 系统诊断（7个命令）
│  │
│  ├─ 🟡 阶段2：诊断与修复 (3个脚本)
│  │  ├─ [[ws-repair.sh]] — 自动修复系统（诊断+激进模式）
│  │  ├─ [[ws-monitor.sh]] — 实时监控（后台运行）
│  │  └─ [[ws-export-config.sh]] — 配置导出（JSON/YAML）
│  │
│  └─ 🔵 阶段3：高级功能 (4个脚本)
│     ├─ [[ws-quick-toggle.sh]] — 快速切换模式
│     ├─ [[ws-profile.sh]] — 配置快照管理
│     ├─ [[ws-migrate.sh]] — 跨机器迁移
│     └─ [[ws-performance.sh]] — 性能测试与优化
│
└─ 📋 参考与使用
   ├─ 快捷键速查表
   ├─ 常见问题
   └─ 故障排除
```

---

## 🚀 快速开始路径

### 第一次部署（推荐顺序）

1. **阅读系统设计** → [[Hyprland Workspace Config - Optimization Map]]
2. **理解快捷键和脚本** → [[Hyprland Config File with Scripts]]
3. **查看配置模板** → [[Hyprland Custom Config File]]
4. **运行初始化脚本** → [[ws-init.sh]]
5. **验证系统状态** → `ws-debug.sh status`

### 日常使用快捷键

| 快捷键 | 功能 |
|--------|------|
| `Super+Shift+T` | 快速切换模式（default ↔ headless） |
| `Super+Shift+H` | 切换到虚拟屏（Headless） |
| `Super+Shift+D` | 切换到物理屏（Default） |
| `Super+Shift+S` | 显示当前状态 |
| `Super+Ctrl+Shift+V` | 验证系统完整性 |
| `Super+Ctrl+Shift+R` | 自动修复系统 |

---

## 📊 项目统计

| 类别 | 数量 |
|------|------|
| **总脚本数** | 12 |
| **总代码行数** | 3500+ |
| **文档笔记数** | 20+ |
| **快捷键绑定** | 6 |
| **初始化步骤** | 6 |
| **完成百分比** | 100% ✅ |

---

## 🎯 各功能区职责

### 配置管理区
- 保存所有 Hyprland 配置文件
- 路径：`~/.config/hypr/conf/custom/`
- 包含：默认配置、Headless配置、符号链接

### 脚本管理区
- 保存所有系统脚本
- 路径：`~/.config/hypr/scripts/custom/`
- 功能：初始化、切换、诊断、修复、监控

### 状态管理区
- 保存系统状态和备份
- 路径：`~/.config/hypr/state/`
- 包含：当前模式、显示器列表、配置备份、日志

---

## 💡 使用建议

- **新用户**：按"快速开始路径"第1-5步依次进行
- **需要自定义**：修改[[Hyprland Custom Workspace Config File]]中的配置
- **遇到问题**：运行`ws-debug.sh verify`诊断，或使用`ws-repair.sh --aggressive`自动修复
- **迁移新机器**：使用[[ws-migrate.sh]]导出/导入配置
- **性能优化**：运行[[ws-performance.sh]]获得优化建议

---

## 📚 按用途快速查询

### 我想要...

- **快速理解系统设计** → [[Hyprland Workspace Config - Optimization Map]]
- **立即开始部署** → [[Hyprland Config File with Scripts]]（6步初始化）
- **查看可用快捷键** → [[Hyprland Custom Config File]]（快捷键绑定部分）
- **修改工作区配置** → [[Hyprland Custom Workspace Config File]]（选择显示器配置）
- **诊断系统问题** → `ws-debug.sh verify`（对应[[ws-debug.sh]]）
- **在新机器上部署** → [[ws-migrate.sh]]（导出/导入流程）
- **保存工作配置** → [[ws-profile.sh]]（快照管理）

---

## 🔗 相关链接

- **总体规划**: [[Hyprland Workspace Config - Optimization Map]]
- **配置模板**: [[Hyprland Custom Config File]]
- **脚本集成**: [[Hyprland Config File with Scripts]]
- **工作区配置**: [[Hyprland Custom Workspace Config File]]

---

**最后更新**: 2026-05-04  
**状态**: ✅ **完成** | 可生产使用  
**维护性**: ⭐⭐⭐⭐⭐ 高度模块化，易于维护和扩展
