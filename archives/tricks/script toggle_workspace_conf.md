---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---
> [!note]
> You should create `~/.config/hypr/scripts/custom/to_headless.sh`, with
> [[script toggle_workspace_conf]]
> You should create `~/.config/hypr/scripts/custom/to_default.sh`, with
> [[script toggle_workspace_conf]]

## Text
```
#!/usr/bin/env bash
set -euo pipefail

LINK="$HOME/.config/hypr/conf/custom_workspace.conf"
HEADLESS_TEMPLATE="$HOME/.config/hypr/conf/custom/headless_workspace.conf.temp"
HEADLESS_CONF="$HOME/.config/hypr/conf/custom/headless_workspace.conf"

# 1) 检查模板源
if [ ! -f "$HEADLESS_TEMPLATE" ]; then
  echo "缺少模板: $HEADLESS_TEMPLATE"
  echo "请先创建 headless_workspace.conf.temp"
  exit 1
fi

# 2) 若不存在 Headless 输出则创建
if ! hyprctl monitors | grep -q "Monitor HEADLESS"; then
  hyprctl output create headless
  sleep 1
fi

# 3) 动态获取输出名（不要硬编码 HEADLESS-1）
TARGET=$(hyprctl monitors | awk '/Monitor HEADLESS/ {print $2; exit}')
if [ -z "${TARGET:-}" ]; then
  echo "未检测到 Headless 输出，切换失败"
  exit 1
fi

# 4) 从 .temp 生成运行配置并替换占位符
cp "$HEADLESS_TEMPLATE" "$HEADLESS_CONF"
sed -i "s|__HEADLESS_OUTPUT__|$TARGET|g" "$HEADLESS_CONF"

# 5) 切换链接到 headless 运行配置
ln -sfn "$HEADLESS_CONF" "$LINK"

# 6) 可选：设置 headless 输出分辨率（按需修改）
hyprctl keyword monitor "$TARGET,2800x1968@60,auto,1"

# 7) 重载并通知
hyprctl reload
notify-send "Hyprland" "已切换至 Headless 模式 ($TARGET)"

# 可选：按你的硬件名禁用物理屏
# hyprctl keyword monitor "DP-1, disable"
# hyprctl keyword monitor "DP-2, disable"



```


## Text
```
#!/usr/bin/env bash
set -euo pipefail

LINK="$HOME/.config/hypr/conf/custom_workspace.conf"
DEFAULT="$HOME/.config/hypr/conf/custom/default_workspace.conf"

# 1) 恢复到默认配置
ln -sfn "$DEFAULT" "$LINK"

# 2) 清理所有 Headless 输出（支持 HEADLESS-1/2/3...）
mapfile -t HEADLESS_MONITORS < <(hyprctl monitors | awk '/Monitor HEADLESS/ {print $2}')
for monitor in "${HEADLESS_MONITORS[@]}"; do
  hyprctl output remove "$monitor"
  echo "已移除: $monitor"
done

# 3) 重载并通知
hyprctl reload
notify-send "Hyprland" "已恢复默认模式"

# 可选：按你的硬件名启用物理屏
# hyprctl keyword monitor "DP-1, enable"
# hyprctl keyword monitor "DP-2, enable"


```

---

## Thoughts
## 更新记录
- 2026-05-04: 将 `to_headless` / `to_default` 的完整脚本模板写入本文件，采用 `.conf.temp` -> 生成运行配置 -> `ln -sfn` -> `hyprctl reload` 的工作流。
- 注意：此处为脚本模板文档，**尚未**将脚本部署为 `~/.config/hypr/scripts/custom/*.sh` 可执行文件。如果需要我可以把模板写成真实脚本并设置可执行权限。

## 部署（可复制命令）
以下命令会把本文件中的模板写为可执行脚本并部署到 `~/.config/hypr/scripts/custom/`：

```bash
mkdir -p "$HOME/.config/hypr/scripts/custom"

cat > "$HOME/.config/hypr/scripts/custom/to_headless.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

LINK="$HOME/.config/hypr/conf/custom_workspace.conf"
HEADLESS_TEMPLATE="$HOME/.config/hypr/conf/custom/headless_workspace.conf.temp"
HEADLESS_CONF="$HOME/.config/hypr/conf/custom/headless_workspace.conf"

mkdir -p "$(dirname "$HEADLESS_TEMPLATE")" "$(dirname "$LINK")"

# 1) 检查模板源
if [ ! -f "$HEADLESS_TEMPLATE" ]; then
  echo "缺少模板: $HEADLESS_TEMPLATE"
  echo "请先创建 headless_workspace.conf.temp"
  exit 1
fi

# 2) 尝试检测已有 HEADLESS 输出
HEADLESS_OUTPUT=$(hyprctl monitors -j 2>/dev/null | jq -r '.[] | .name | select(startswith("HEADLESS"))' 2>/dev/null | head -n 1 || true)

# 如果未检测到则创建一个 headless 输出
if [ -z "${HEADLESS_OUTPUT:-}" ]; then
  hyprctl output create headless || true
  sleep 1
  HEADLESS_OUTPUT=$(hyprctl monitors -j 2>/dev/null | jq -r '.[] | .name | select(startswith("HEADLESS"))' 2>/dev/null | head -n 1 || true)
fi

if [ -z "${HEADLESS_OUTPUT:-}" ] || [ "$HEADLESS_OUTPUT" = "null" ]; then
  echo "未检测到 Headless 输出，切换失败"
  exit 1
fi

# 3) 备份已有运行配置（如果存在）
if [ -f "$HEADLESS_CONF" ]; then
  cp "$HEADLESS_CONF" "${HEADLESS_CONF}.bak.$(date +%s)" || true
fi

# 4) 从 .temp 生成运行配置并替换占位符
cp "$HEADLESS_TEMPLATE" "$HEADLESS_CONF"
# 使用 safe sed 替换
sed -i "s|__HEADLESS_OUTPUT__|$HEADLESS_OUTPUT|g" "$HEADLESS_CONF"

# 5) 切换符号链接到 headless 运行配置（原子操作）
ln -sfn "$HEADLESS_CONF" "$LINK"

# 6) 可选：设置 headless 输出分辨率（按需修改）
# 忽略命令错误以保证流程继续
hyprctl keyword monitor "$HEADLESS_OUTPUT,2800x1968@60,auto,1" 2>/dev/null || true

# 7) 重载配置并通知
hyprctl reload
notify-send "Hyprland" "已切换至 Headless 模式 ($HEADLESS_OUTPUT)"

exit 0
EOF

cat > "$HOME/.config/hypr/scripts/custom/to_default.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

LINK="$HOME/.config/hypr/conf/custom_workspace.conf"
DEFAULT="$HOME/.config/hypr/conf/custom/default_workspace.conf"

# 1) 恢复到默认配置
ln -sfn "$DEFAULT" "$LINK"

# 2) 清理所有 Headless 输出（支持 HEADLESS-1/2/3...）
mapfile -t HEADLESS_MONITORS < <(hyprctl monitors | awk '/Monitor HEADLESS/ {print $2}')
for monitor in "${HEADLESS_MONITORS[@]}"; do
  hyprctl output remove "$monitor" || true
  echo "已移除: $monitor"
done

# 3) 重载并通知
hyprctl reload
notify-send "Hyprland" "已恢复默认模式"

exit 0
EOF

chmod +x "$HOME/.config/hypr/scripts/custom/to_headless.sh" "$HOME/.config/hypr/scripts/custom/to_default.sh"
echo "部署完成: $HOME/.config/hypr/scripts/custom/to_headless.sh, to_default.sh"
```

建议先在安全环境用 `bash -n` / `shellcheck` 或将 `hyprctl` 调用替换为 `echo hyprctl ...` 进行干运行测试。