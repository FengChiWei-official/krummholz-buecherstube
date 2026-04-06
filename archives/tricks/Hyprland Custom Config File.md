---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/technique
---

## Definition

The file is in that path `~/.config/hypr/conf/custom.conf`
>[!note]
>related config of workspace in [[Hyprland Custom Workspace Config File]]

> [!tip] 
> YOU SHOULD MANUALLY CREATE A SOFT LINK FOR `workspace.conf`!!!
> With : `ln -s ~/.config/hypr/conf/custom/default_workspace.conf ~/.config/hypr/conf/custom_workspace.conf`


> [!note]
> You should create `~/.config/hypr/scripts/custom/to_headless.sh`, with
> [[script toggle_workspace_conf]]
> You should create `~/.config/hypr/scripts/custom/to_default.sh`, with
> [[script toggle_workspace_conf]]

```
# Add your additional Hyprland configurations here
# Hook for Obsidian: [[Hyprland Config]]

# ===========================================
# Hyprland Configuration File
# Elegantly Annotated
# ===========================================

# Define main modifier key
# Use SUPER (Windows/Command) key as primary modifier
$mainMod = SUPER

# Custom script path definitions
$HYPRSCRIPTS = ~/.config/hypr/scripts     # Hyprland-specific scripts
$SCRIPTS = ~/.config/ml4w/scripts         # Other tool scripts


# ========================
# Auto-start Applications
# ========================
exec-once = fcitx5                        # Chinese input method framework
exec-once = clash-verge                   # Network proxy client
exec-once = $HYPRSCRIPTS/notifications.sh # Custom notification script
exec-once = /usr/lib/pam_kwallet_init     # KDE wallet manager

# ========================
# proxy setting
# ========================

env = http_proxy,http://127.0.0.1:7897
env = https_proxy,http://127.0.0.1:7897
env = all_proxy,socks5://127.0.0.1:7897
env = no_proxy,localhost,127.0.0.1,localaddress,.localdomain.com

# ========================
# Workspace Configuration
# ========================
# Import workspace configuration from external file for cleaner main config
source = ~/.config/hypr/conf/custom_workspace.conf


# ========================
# Default Application Shortcuts
# ========================
# Remove existing browser shortcut
unbind = $mainMod, B

# Application shortcut configuration
bind = $mainMod, B, exec, google-chrome-stable --new-window # Open Chrome browser
bind = $mainMod, C, exec, code                  # Open Visual Studio Code

# Remove existing launcher shortcut
unbind = $mainMod, R
bind = $mainMod, R, exec, rofi -show run        # Use Rofi application launcher

# Remove existing Obsidian shortcut
unbind = $mainMod, O
bind = $mainMod, O, exec, obsidian              # Open Obsidian notes application


# ========================
# Screenshot Configuration
# ========================
# Remove existing screenshot keybindings
unbind = $mainMod, P
unbind = $mainMod ALT, P
unbind = $mainMod SHIFT, P

# Rebind screenshot shortcuts
bind = $mainMod, p, exec, $HYPRSCRIPTS/screenshot.sh               # Normal screenshot (opens menu for mode selection)
bind = $mainMod ALT, P, exec, $HYPRSCRIPTS/screenshot.sh --instant      # Instant full-screen screenshot
bind = $mainMod SHIFT, P, exec, $HYPRSCRIPTS/screenshot.sh --instant-area # Instant area screenshot


# ========================
# System Compatibility Fixes
# ========================
xwayland {
    force_zero_scaling = true  # Force XWayland applications to use zero scaling, fixing display issues
}
dwindle {
    pseudotile = true         # Enable pseudo-tiling layout
    preserve_split = true     # Maintain window split state
}

```

---
## **Related**

