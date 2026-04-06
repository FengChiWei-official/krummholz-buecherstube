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
#!/bin/bash
LINK=~/.config/hypr/conf/custom_workspace.conf
HEADLESS=~/.config/hypr/conf/custom/headless_workspace.conf

#!/bin/bash
LINK=~/.config/hypr/conf/custom_workspace.conf
HEADLESS=~/.config/hypr/conf/custom/headless_workspace.conf

# 1. 强制链接配置文件
ln -sf "$HEADLESS" "$LINK"

# 2. 检查是否已经存在 HEADLESS 显示器
if ! hyprctl monitors | grep -q "HEADLESS"; then
    # 如果不存在，则创建一个
    hyprctl output create headless
    # 等待一秒确保输出已初始化
    sleep 1
fi

# 3. 强制设置分辨率和刷新率 (防止出现 0.06Hz 的问题)
# 这里的 HEADLESS-1 是默认生成的第一个名称，如果是递增的，可以用变量获取
TARGET=$(hyprctl monitors | grep "HEADLESS" | head -n 1 | awk '{print $2}')
#hyprctl keyword monitor "$TARGET,2560x1440@60,auto,1"
hyprctl keyword monitor "$TARGET,2800x1968@60,auto,1"


# 4. 刷新并通知
hyprctl reload
notify-send "Hyprland" "已切换至 Headless 模式 ($TARGET)"

# 在 to_headless.sh 中创建完虚拟屏后执行：
hyprctl keyword monitor "DP-1, disable"
hyprctl keyword monitor "DP-2, disable"



```


## Text
```
#!/bin/bash
LINK=~/.config/hypr/conf/custom_workspace.conf
DEFAULT=~/.config/hypr/conf/custom/default_workspace.conf

# 1. 恢复配置文件链接
ln -sf "$DEFAULT" "$LINK"

# 2. 找到所有以 HEADLESS 开头的显示器并循环移除
# 这样即使你有 HEADLESS-2, HEADLESS-3 也能一键清空
mapfile -t HEADLESS_MONITORS < <(hyprctl monitors | grep "Monitor HEADLESS" | awk '{print $2}')

for monitor in "${HEADLESS_MONITORS[@]}"; do
    hyprctl output remove "$monitor"
    echo "已移除: $monitor"
done

# 3. 刷新配置并通知
hyprctl reload
notify-send "Hyprland" "已移除所有虚拟屏幕，恢复默认模式"

# 在 to_headless.sh 中创建完虚拟屏后执行：
hyprctl keyword monitor "DP-1, enable"
hyprctl keyword monitor "DP-2, enable"


```

---

## Thoughts