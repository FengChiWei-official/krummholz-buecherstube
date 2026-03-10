---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
aliases:
  - Make Hyprland Notification Properly Work
---

## Symptom

``` bash
❯ swaync
Starting SwayNotificationCenter version swaync 0.12.4
** Message: 17:45:15.645: configModel.vala:513: Loading Config: "/etc/xdg/swaync/config.json"

(process:75359): Adwaita-WARNING **: 17:45:15.656: Using GtkSettings:gtk-application-prefer-dark-theme with libadwaita is unsupported. Please use AdwStyleManager:color-scheme instead.
** Message: 17:45:15.779: functions.vala:104: Loading CSS: "/etc/xdg/swaync/style.css"
** Message: 17:45:15.780: functions.vala:117: Loading CSS: "/etc/xdg/swaync/style.css"
Could not acquire notification name. Please close any other notification daemon like mako or dunst
```

---

## Thoughts

### Step One
> aim: Prevents [[Hyprland]] from trying launch [[KDE]] components for notificaions .

create a script `~/.config/hypr/scripts/notifications.sh`.

``` bash
#!/bin/bash

# 暴力清理所有潜在的冲突进程
pkill -9 -x swaync
pkill -9 -f "plasma-notification"
pkill -9 -x dunst
pkill -9 -x mako

# 等待 DBus 释放名称
timeout=5
while busctl --user list | grep -q "org.freedesktop.Notifications" && [ $timeout -gt 0 ]; do
    sleep 0.5
    ((timeout--))
done

# 启动 swaync
swaync > /dev/null 2>&1 &
```

### Step Two
> Register the script into config

in `~/.config/hypr/conf/custom.conf`

``` conf
exec-once = ~/.config/hypr/scripts/notifications.sh
```