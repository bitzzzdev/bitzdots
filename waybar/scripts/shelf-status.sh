#!/bin/bash
# ============================================================
# Quick Shelf Waybar Module Status Script
# ============================================================

if command -v quick-shelf &>/dev/null; then
    quick-shelf --status 2>/dev/null && exit 0
fi

if [ -x "$HOME/.local/bin/quick-shelf" ]; then
    "$HOME/.local/bin/quick-shelf" --status 2>/dev/null && exit 0
fi

DOTFILES_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
if [ -x "$DOTFILES_DIR/scripts/quick-shelf.py" ]; then
    "$DOTFILES_DIR/scripts/quick-shelf.py" --status 2>/dev/null && exit 0
fi

# Fallback output if not installed yet
echo '{"text":"\udb84\udcac","alt":"shelf","tooltip":"Quick Shelf (Click to fetch and install)","class":"offline","count":0}'
