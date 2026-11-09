<div align="center">
  <h1>bitzdots</h1>
  <p><strong>Lean Hyprland dotfiles • Automatic matugen M3 theming • Low-end optimized</strong></p>

  <p>
    <a href="#-features">Features</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="docs/getting-started.md">Getting Started</a> •
    <a href="docs/installation.md">Installation</a> •
    <a href="docs/keybindings.md">Keybindings</a> •
    <a href="docs/theming.md">Theming</a> •
    <a href="docs/performance.md">Performance</a> •
    <a href="docs/faq.md">FAQ</a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/hyprland-latest-blue?style=flat-square" alt="Hyprland">
    <img src="https://img.shields.io/badge/arch-supported-1793D1?style=flat-square&logo=archlinux" alt="Arch">
    <img src="https://img.shields.io/badge/fedora-supported-294172?style=flat-square&logo=fedora" alt="Fedora">
    <img src="https://img.shields.io/badge/debian-supported-A81D33?style=flat-square&logo=debian" alt="Debian">
    <img src="https://img.shields.io/badge/nixos-supported-5277C3?style=flat-square&logo=nixos" alt="NixOS">
    <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
  </p>

  <p>
    <a href="https://github.com/bitzzdev/bitzdots">
      <img src="ss/ss3.png" alt="Screenshot 1" width="45%">
    </a>
    <a href="https://github.com/bitzzdev/bitzdots">
      <img src="ss/ss2.png" alt="Screenshot 2" width="45%">
    </a>
    <a href="https://github.com/bitzzdev/bitzdots">
      <img src="ss/ss1.png" alt="Screenshot 3" width="45%">
    </a>
    <a href="https://github.com/bitzzdev/bitzdots">
      <img src="ss/ss4.png" alt="Screenshot 4" width="45%">
    </a>
  </p>
</div>

---

> [!WARNING]
> **Repository Renaming Notice:** This repository will be renamed to **DEVdots** soon.

bitzdots is a **lean, automated theming system** for Hyprland on Wayland. Change your wallpaper and every component, including the status bar, terminal, launcher, notifications, logout screen, audio visualizer, and Qt/KDE apps, adapts to match.

Built for **low-end hardware** without sacrificing usability. The full stack (Hyprland + waybar + swaync) idles under **300MB RAM**, with aggressive CPU optimizations to keep fans quiet on older machines.

## Features

- **Full-stack auto-theming:** One wallpaper change propagates to 20+ components via matugen M3 color extraction (waybar, kitty, rofi, swaync, wlogout, cava, Hyprland borders, Qt/KDE, GTK, and browser CSS).
- **Event-driven cache daemon:** inotify-based background pre-generation keeps wallpaper switching fast.
- **Live wallpaper support:** Static images with animated transitions (`awww`) and video wallpapers (`mpvpaper`) use automatic palette extraction.
- **26 templates:** Every themed component, including launcher, power, wallpaper-grid themes, and eight SVG icons, uses a template.
- **Rofi-powered menus:** The app launcher, clipboard manager (cliphist), power menu, wallpaper picker, WiFi, Bluetooth, audio, system monitor, and Quick Shelf styling are keyboard-navigable.
- **Waybar with 16 modules:** Workspace display, CPU animation, media, Quick Shelf, recording indicator, brightness, power profiles, notifications, and system TUIs.
- **Screen recording:** wf-recorder supports full-screen and region recording with audio and organized output directories.
- **Screenshots with clipboard:** Fullscreen and selection screenshots both save and copy to the clipboard.
- **Fish shell and fastfetch:** The shell stays quiet and fastfetch shows the custom BITZ logo on startup.
- **Safe theme switching:** Every matugen run creates a backup and restores the previous theme if generation fails.
- **Wallpaper cache daemon:** inotify watches wallpaper directories and pre-generates palettes.
- **Multi-distro installer:** Automated setup supports Arch, Fedora, Debian/Ubuntu, and NixOS with `--with-deps`.

## Quick Start

```bash
git clone https://github.com/bitzzdev/bitzdots.git ~/.config/bitzdots
cd ~/.config/bitzdots
chmod +x install.sh

# Link configs only:
./install.sh

# Or link configs + install all system packages:
./install.sh --with-deps
```

See the **[Getting Started guide](docs/getting-started.md)** for a full walkthrough.

## Keybindings at a Glance

| Key | Action |
|-----|--------|
| `SUPER + T` | Open terminal |
| `SUPER + Q` | Close window |
| `SUPER + Space` | App launcher (rofi) |
| `SUPER + V` | Clipboard history |
| `SUPER + SHIFT + S` | Selection screenshot |
| `Print` | Fullscreen screenshot |
| `SUPER + R` | Toggle screen recording |
| `SUPER + SHIFT + W` | Wallpaper picker |
| `SUPER + N` | Toggle notifications |
| `SUPER + P` | Power menu |
| `SUPER + L` | Lock screen |

Full reference: **[docs/keybindings.md](docs/keybindings.md)**

## Documentation

| Guide | Description |
|-------|------------|
| [Getting Started](docs/getting-started.md) | First-time setup, recommended config |
| [Installation](docs/installation.md) | Detailed install per distro, manual steps |
| [Features](docs/features.md) | Complete feature breakdown |
| [Keybindings](docs/keybindings.md) | All keyboard shortcuts |
| [Waybar Modules](docs/waybar-modules.md) | Every module explained |
| [Theming](docs/theming.md) | How matugen works, templates |
| [Scripts](docs/scripts.md) | All utility scripts documented |
| [Performance](docs/performance.md) | Low-end optimization guide |
| [Customization](docs/customization.md) | Add new components, modify themes |
| [DEVos Aliases](docs/devos-aliases.md) | Arch Linux `dev` shortcuts & pacman aliases |
| [FAQ](docs/faq.md) | Common issues and solutions |

## Directory Structure

```
~/.config/
├── hypr/              # Hyprland (Lua config)
│   ├── hyprland.lua   # Entry point
│   ├── keybinds.lua   # 55+ keybinds
│   ├── appearance.lua # Blur, opacity, borders
│   ├── animations.lua # Window animations
│   ├── rules.lua      # 20+ window rules
│   ├── monitors.lua   # Monitor setup
│   ├── input.lua      # Keyboard, mouse, touchpad
│   └── autostart.lua  # Startup applications
├── waybar/            # Status bar
│   ├── config.jsonc   # Module layout (themed, 15 modules)
│   ├── style.css      # Styling (themed)
│   └── scripts/       # 17 custom scripts
├── rofi/              # App launcher & menus
│   ├── themes/        # 27 variants
│   ├── icons/         # 8 themed SVG icons
│   ├── scripts/       # Power, clipboard, wallpaper
│   └── config.rasi    # Main config
├── swaync/            # Notification center
├── wlogout/           # Logout screen
├── kitty/             # Terminal (themed)
├── cava/              # Audio visualizer (themed)
├── matugen/           # Theming engine (26 templates)
├── qshelf/             # Generated Quick Shelf palette lives in ~/.config/qshelf
├── fish/              # Fish shell config
├── fastfetch/         # System fetch (custom logo)
└── scripts/           # 10 utility scripts
```

## Performance

bitzdots is engineered for **low-resource environments**:

| Metric | Value |
|--------|-------|
| **Idle RAM (full stack)** | ~250-300MB |
| **Waybar CPU** | ~3.5% idle |
| **Compositor** | Hyprland (~170MB) |
| **Notification daemon** | swaync (~85MB) |
| **Status bar** | waybar (~60MB) |

Optimization strategies are documented in **[Performance](docs/performance.md)**.

## Theming Pipeline

```
Wallpaper image
    ↓ matugen (Material 3 palette extraction)
Material 3 & base16 color schemes
    ↓ 26 templates
Config files for every component (20+ files)
    ↓ reload-theme.sh
All apps pick up new colors instantly
```

## Quick Shelf Widget

bitzdots integrates **Quick Shelf**, a lightweight desktop shelf and Waybar popover:
- **App Shortcuts**: Quick-launch pinned apps or search and add installed desktop applications.
- **Image Shelf**: Drag and drop images from file managers or web browsers into the shelf for instant preview.
- **Two-way Drag and Drop**: Drag thumbnails directly out of the shelf into external apps (Discord, web browsers, GIMP, Nautilus).
- **Homescreen Widget**: Runs on the desktop background layer (`quick-shelf --homescreen`).
- **Waybar Module**: Displays item counts with click-to-toggle popover on the bar (`SUPER + D`).

To fetch the precompiled release binary without on-device compilation:
```bash
dev shelf fetch
```
Or update:
```bash
dev shelf update
```

## Requirements

- **Hyprland** (Wayland compositor)
- **matugen:** Material 3 color palette generator
- **inotify-tools:** Required by the cache daemon
- **Nerd Font:** Provides icons, JetBrainsMono is recommended
- **GTK 3** and **gtk-layer-shell**: for Wayland layer widgets

## Environment Variables

- `XDG_CONFIG_HOME`: user configuration directory (defaults to `~/.config`)
- `XDG_DATA_HOME`: user data directory (defaults to `~/.local/share`)
- `XDG_RUNTIME_DIR`: runtime socket directory (defaults to `/run/user/<UID>` or `/tmp`)
- `WALLPAPER_DIR`: directory containing wallpaper images (defaults to `~/Pictures/Wallpapers`)

## Supported Distros

Arch Linux (including Arch-based), Fedora, Debian/Ubuntu, NixOS.

## Philosophy

1. **Low-end first:** Every watt and megabyte matters. Scripts are optimized for minimal CPU and RAM, not convenience.
2. **Theme automatically:** One wallpaper change updates everything. No manual color picking.
3. **Safe by default:** Every theme generation creates a backup. A failure won't leave broken configs.
4. **Keyboard-driven:** Everything is within reach of the home row. The mouse is optional.
5. **No bloat:** Every component earns its place. There are no unused default configs or unnecessary dependencies.

## License

MIT
