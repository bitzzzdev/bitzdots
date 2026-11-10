# Changelog

## [Unreleased]

### Added
- Added a Matugen template that generates the Quick Shelf palette at
  `~/.config/quick/shelf/colors.css`.
- Added Quick Shelf to the theme reload sequence when it is running.
- Quick Shelf terminal integration: App shortcut storage and image drop shelf
  with instant thumbnail preview and two-way drag-and-drop.
- Precompiled binary fetcher script `scripts/fetch-quick-shelf.sh` for
  installing release binaries without compiling locally.
- DEVos shelf commands for fetching, updating, checking, toggling, and
  starting the terminal shelf.
- Interactive Waybar module for Quick Shelf item counts and toggle actions.
- Hyprland floating window rule and `SUPER + D` toggle binding.
- Terminal shelf fallback status for systems before the binary is fetched.
- GitHub Actions validation for configuration scripts and shell syntax.

### Changed
- Documented Quick Shelf in the theming pipeline and repository layout.
- Standardized documentation and documented XDG and wallpaper environment
  variables.
- Updated `install.sh` with Quick Shelf script links and executable permissions.
- Moved Quick Shelf configuration and generated theme files to
  `~/.config/quick/shelf/`.
- Made the shelf a terminal UI launched through the existing Waybar and
  Hyprland bindings.
