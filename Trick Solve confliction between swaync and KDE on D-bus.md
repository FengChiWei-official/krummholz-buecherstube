---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Symtom

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

# 1. Identify if we are actually in Hyprland
if [ "$XDG_CURRENT_DESKTOP" = "Hyprland" ]; then
    
    # 2. Kill KDE's notification listeners/daemons aggressively 
    # This clears the path for SwayNC to grab the DBus name
    pkill -9 -f org.kde.plasma.Notifications
    pkill -9 -f plasma_waitforname
    
    # 3. If another swaync is stuck, clear it
    pkill -9 swaync
    
    # 4. Give DBus a tiny moment to register the deaths
    sleep 0.5
    
    # 5. Start SwayNC
    swaync &
else
    echo "Not in Hyprland, skipping SwayNC startup."
fi

```

### Step Two
> Register the script into config

in `~/.config/hypr/conf/custom.conf`

``` conf
exec-once = ~/.config/hypr/scripts/notifications.sh
```