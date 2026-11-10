#!/bin/bash
# ============================================================
# Fetch Precompiled Quick Shelf Binary from GitHub Release
# ============================================================
set -euo pipefail

BIN_DIR="${XDG_BIN_HOME:-$HOME/.local/bin}"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/quick/shelf"
DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/quick-shelf"
REPO="bitzzdev/quickShelf"
RELEASE_TAG="quick-shelf-latest"
TARGET_NAME="quick-shelf-x86_64"
DEST_BIN="$BIN_DIR/quick-shelf"

mkdir -p "$BIN_DIR" "$CONFIG_DIR" "$DATA_DIR/images"

echo ":: Fetching Quick Shelf binary from GitHub ($REPO)..."

DOWNLOAD_URL="https://github.com/$REPO/releases/download/$RELEASE_TAG/$TARGET_NAME"
TEMP_FILE="$(mktemp /tmp/quick-shelf-bin.XXXXXX)"

cleanup() {
    rm -f "$TEMP_FILE"
}
trap cleanup EXIT

fetch_success=false

# Try downloading from releases
if curl -fsSL "$DOWNLOAD_URL" -o "$TEMP_FILE" 2>/dev/null; then
    fetch_success=true
elif curl -fsSL "https://github.com/$REPO/releases/latest/download/$TARGET_NAME" -o "$TEMP_FILE" 2>/dev/null; then
    fetch_success=true
fi

if [ "$fetch_success" = true ] && [ -s "$TEMP_FILE" ]; then
    chmod +x "$TEMP_FILE"
    # Basic binary sanity check
    if file "$TEMP_FILE" | grep -qi "ELF.*executable"; then
        mv "$TEMP_FILE" "$DEST_BIN"
        chmod +x "$DEST_BIN"
        echo "   Quick Shelf binary installed successfully to $DEST_BIN"
        pkill -x quick-shelf 2>/dev/null || true
        if command -v notify-send >/dev/null 2>&1; then
            notify-send -a "Quick Shelf" -i "quick-shelf" "Quick Shelf" "quickShelf updated by github.com/bitzzdev" 2>/dev/null || true
        fi
        "$DEST_BIN" --version 2>/dev/null || true
        exit 0
    else
        echo "   Warning: Downloaded file is not an ELF binary."
    fi
fi

echo "   Could not fetch binary from $DOWNLOAD_URL"
echo "   Ensure GitHub Actions build workflow has completed on $REPO."
exit 1
