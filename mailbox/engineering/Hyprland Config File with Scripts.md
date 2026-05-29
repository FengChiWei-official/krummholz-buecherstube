

🌳 **导航**: [[Hyprland Workspace System - Tree Navigation]] > **配置管理** > **脚本集成**

完整指南：如何在 Hyprland 主配置中引用脚本调用与快捷键绑定。

> [!note]
> 主配置正文只保留在 [[Hyprland Custom Config File]]。这里不再重复写 `custom.conf` 内容，只说明脚本接入方式。

## 快速参考

| 任务 | 命令 |
|------|------|
| 为脚本添加执行权限 | `chmod +x ~/.config/hypr/scripts/custom/*.sh` |
| 启动时运行脚本 | `exec-once = ~/.config/hypr/scripts/startup.sh` |
| 按键绑定脚本 | `bind = $mainMod, KEY, exec, /path/to/script.sh` |
| 后台运行脚本 | `exec-once = ~/.config/hypr/scripts/script.sh &` |
| 带参数的脚本 | `bind = $mainMod, KEY, exec, script.sh --arg value` |

## 完整配置示例

脚本路径变量、`exec-once` 和 `bind` 的具体写法都已统一整理到 [[Hyprland Custom Config File]]，这里仅保留“脚本如何接入主配置”的说明：

- 脚本目录统一用 `~/.config/hypr/scripts/custom/`
- 主配置统一通过 `source = ~/.config/hypr/conf/custom_workspace.conf` 加载工作区配置
- 快捷键绑定只在主配置笔记里保留一次

## 初始化步骤

### 第1步：创建目录结构

```bash
mkdir -p ~/.config/hypr/scripts/custom
mkdir -p ~/.config/hypr/conf/custom
mkdir -p ~/.config/hypr/state
mkdir -p ~/.config/hypr/logs
```

### 第2步：将脚本放入目录

```bash
# 例如从仓库复制脚本
cp ~/your-repo/scripts/ws-*.sh ~/.config/hypr/scripts/custom/
cp ~/your-repo/scripts/to_*.sh ~/.config/hypr/scripts/custom/
```

### 第3步：设置执行权限

```bash
# 为所有脚本添加执行权限
chmod +x ~/.config/hypr/scripts/custom/*.sh
chmod +x ~/.config/hypr/scripts/*.sh

# 或针对单个脚本
chmod +x ~/.config/hypr/scripts/custom/ws-init.sh
```

### 第4步：验证脚本

```bash
# 测试脚本是否能运行
~/.config/hypr/scripts/custom/ws-debug.sh status
~/.config/hypr/scripts/custom/ws-debug.sh verify
```

### 第5步：执行初始化

```bash
~/.config/hypr/scripts/custom/ws-init.sh
```

### 第6步：重新加载 Hyprland

```bash
hyprctl reload
```

## 常见注意事项

- ✅ 使用 `$mainMod` 变量而非硬编码 `SUPER`
- ✅ 使用 `$HYPRSCRIPTS` 等变量保持路径一致性
- ✅ 在脚本中使用绝对路径或环境变量
- ✅ 为需要图形环境的脚本添加 `&` 后台执行
- ✅ 在修改配置后运行 `hyprctl reload` 重新加载
- ⚠️ 调用脚本前确认它们具有执行权限（`chmod +x`）
- ⚠️ 脚本中如使用 Wayland/X11 特定功能，确保环境变量正确设置
- ⚠️ 如脚本会阻塞（如长时间运行的任务），使用 `&` 或后台运行

## 快捷键语法参考

| 类型 | 语法 |
|------|------|
| 基础快捷键 | `bind = $mod, KEY, exec, command` |
| 组合键 | `bind = $mod SHIFT, KEY, exec, command` |
| Alt组合 | `bind = $mod ALT, KEY, exec, command` |
| Ctrl组合 | `bind = $mod CTRL, KEY, exec, command` |
| 多个修饰符 | `bind = $mod CTRL ALT, KEY, exec, command` |
| 带参数 | `bind = $mod, KEY, exec, script.sh --arg value` |
| 后台执行 | `bind = $mod, KEY, exec, script.sh &` |

## 对应笔记

- [[Hyprland Workspace Config 优化系统 - 完整地图]] - 总体系统设计
- [[Hyprland Custom Config File]] - 唯一主配置源
- [[ws-init.sh]] - 初始化脚本文档
