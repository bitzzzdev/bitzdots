# Changelog

All notable changes to bitzdots will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [Unreleased]

### Added
- Quick Shelf widget integration: App shortcut storage and image drop shelf with instant thumbnail preview and two-way drag-and-drop.
- Precompiled binary fetcher script `scripts/fetch-quick-shelf.sh` allowing users to install release binaries directly without on-device compilation.
- DEVos shell helper commands in `fish/config.fish`: `dev shelf fetch`, `dev shelf update`, `dev shelf status`, `dev shelf toggle`, and `dev shelf homescreen`.
- Interactive Waybar module `custom/shelf` with status script `waybar/scripts/shelf-status.sh` and click actions to toggle the shelf.
- Dedicated Matugen template `matugen/templates/quick-shelf.css` generating `~/.config/quick-shelf/style.css` on wallpaper change.
- Instant theme reload hook for `quick-shelf` in `scripts/reload-theme.sh`.
- Hyprland floating window rule for `quick-shelf` and `SUPER + D` keybinding to toggle the widget.
- Fallback runner script `scripts/quick-shelf.py` providing instant availability on systems before remote binaries are fetched.
- GitHub Actions CI workflow to validate configuration scripts and shell syntax.

### Changed
- Standardized documentation in `README.md` and `CONTRIBUTING.md` to follow clean human writing guidelines.
- Documented environment variables (`XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_RUNTIME_DIR`, `WALLPAPER_DIR`).
- Updated `install.sh` with Quick Shelf script symlinks and executable permissions.
