#!/usr/bin/env python3
"""
Quick Shelf widget and Waybar helper fallback.
Supports app shortcuts, image drop shelf with instant previews, and two-way drag-and-drop.
"""

import sys
import os
import json
import shutil
import socket
import subprocess
import time
from pathlib import Path

# Paths
CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "qshelf"
DATA_DIR = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / "quick-shelf"
IMAGES_DIR = DATA_DIR / "images"
SHORTCUTS_FILE = DATA_DIR / "shortcuts.json"
IMAGES_FILE = DATA_DIR / "images.json"
STYLE_FILE = CONFIG_DIR / "style.css"
COLORS_FILE = CONFIG_DIR / "colors.css"
SOCKET_FILE = Path(os.environ.get("XDG_RUNTIME_DIR", "/tmp")) / f"quick-shelf-{os.getuid()}.sock"

CONFIG_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_CSS = b"""
@define-color bg rgba(22, 13, 17, 0.94);
@define-color bg-alt rgba(38, 20, 32, 0.6);
@define-color fg #f8e4df;
@define-color fg-muted #d4a8a2;
@define-color selected #d46478;
@define-color active rgba(53, 24, 44, 0.5);
@define-color border-color rgba(110, 68, 80, 0.45);
@define-color card-bg rgba(38, 20, 32, 0.6);
@define-color card-hover rgba(53, 24, 44, 0.85);

.quick-shelf-window {
    background-color: @bg;
    border: 2px solid @selected;
    border-radius: 0;
    padding: 0;
}
.qs-header {
    background-color: @bg-alt;
    margin-bottom: 12px;
    padding: 12px 16px;
    border-bottom: 2px solid @border-color;
}
.qs-mainbox {
    padding: 8px 12px 12px;
}
.qs-title {
    font-size: 14px;
    font-weight: bold;
    color: @fg;
}
.qs-badge {
    background: @selected;
    color: @bg;
    border-radius: 0;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: 600;
}
.qs-btn {
    background: @bg-alt;
    color: @fg;
    border: 1px solid @border-color;
    border-radius: 0;
    padding: 6px 10px;
}
.qs-btn:hover {
    background: @selected;
    color: @bg;
}
.qs-section-title {
    font-size: 12px;
    font-weight: bold;
    color: @fg-muted;
    margin-top: 6px;
    margin-bottom: 6px;
}
.qs-app-card {
    background: @card-bg;
    border: 1px solid @border-color;
    border-radius: 0;
    padding: 8px 6px;
    min-width: 68px;
    min-height: 68px;
}
.qs-app-card:hover {
    background: @card-hover;
    border-color: @selected;
}
.qs-app-label {
    font-size: 11px;
    color: @fg;
    margin-top: 4px;
}
.qs-image-card {
    background: @card-bg;
    border: 1px solid @border-color;
    border-radius: 0;
    padding: 4px;
}
.qs-image-card:hover {
    border-color: @selected;
}
.qs-dropzone {
    border: 2px dashed @border-color;
    border-radius: 0;
    padding: 18px 12px;
    background: @card-bg;
}
.qs-preview-overlay {
    background: @bg;
    border-radius: 0;
    padding: 16px;
    border: 1px solid @border-color;
}
.qs-tab-active {
    background: @selected;
    color: @bg;
    font-weight: bold;
}
"""

def load_json(path, default):
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving {path}: {e}", file=sys.stderr)

def get_shortcuts():
    defaults = [
        {"id": "kitty", "name": "Terminal", "exec": "kitty", "icon": "kitty"},
        {"id": "brave", "name": "Browser", "exec": "brave-origin", "icon": "brave-browser"},
        {"id": "files", "name": "Files", "exec": "nautilus", "icon": "org.gnome.Nautilus"},
        {"id": "code", "name": "Editor", "exec": "code", "icon": "com.visualstudio.code"}
    ]
    if not SHORTCUTS_FILE.exists():
        save_json(SHORTCUTS_FILE, defaults)
        return defaults
    return load_json(SHORTCUTS_FILE, defaults)

def get_images():
    images = load_json(IMAGES_FILE, [])
    valid = [img for img in images if Path(img.get("path", "")).exists()]
    if len(valid) != len(images):
        save_json(IMAGES_FILE, valid)
    return valid

def print_status():
    shortcuts = get_shortcuts()
    images = get_images()
    s_count = len(shortcuts)
    i_count = len(images)
    total = s_count + i_count
    cls = "has-items" if total > 0 else "empty"
    tooltip = (
        f"Quick Shelf\n  • Shortcuts: {s_count}\n  • Images: {i_count}\n\n"
        "Left-click: Toggle shelf\nRight-click: Add shortcut"
    )
    print(json.dumps({
        "text": "\U000f10ac",
        "alt": "shelf",
        "tooltip": tooltip,
        "class": cls,
        "count": total
    }))

def send_ipc(cmd):
    if not SOCKET_FILE.exists():
        return None
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect(str(SOCKET_FILE))
        s.sendall(f"{cmd}\n".encode("utf-8"))
        res = s.recv(1024).decode("utf-8").strip()
        s.close()
        return res
    except Exception:
        if SOCKET_FILE.exists():
            SOCKET_FILE.unlink(missing_ok=True)
        return None

def launch_gui(is_homescreen=False):
    import gi
    gi.require_version("Gtk", "3.0")
    try:
        gi.require_version("GtkLayerShell", "0.1")
        from gi.repository import GtkLayerShell
        layer_shell_available = GtkLayerShell.is_supported()
    except Exception:
        GtkLayerShell = None
        layer_shell_available = False

    from gi.repository import Gtk, Gdk, GdkPixbuf, GLib

    # Start IPC server
    if SOCKET_FILE.exists():
        SOCKET_FILE.unlink(missing_ok=True)

    server_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_sock.bind(str(SOCKET_FILE))
    server_sock.listen(5)
    server_sock.setblocking(False)

    win = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
    win.set_title("Quick Shelf")
    win.set_wmclass("quick-shelf", "quick-shelf")
    win.set_default_size(380, -1)
    win.set_resizable(not is_homescreen)
    win.set_decorated(False)

    if layer_shell_available and is_homescreen:
        GtkLayerShell.init_for_window(win)
        layer = GtkLayerShell.Layer.BOTTOM if is_homescreen else GtkLayerShell.Layer.TOP
        GtkLayerShell.set_layer(win, layer)
        GtkLayerShell.set_keyboard_mode(win, GtkLayerShell.KeyboardMode.ON_DEMAND)
        GtkLayerShell.set_exclusive_zone(win, 0)
        GtkLayerShell.set_anchor(win, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_margin(win, GtkLayerShell.Edge.TOP, 40)
        GtkLayerShell.set_anchor(win, GtkLayerShell.Edge.RIGHT, True)
        GtkLayerShell.set_margin(win, GtkLayerShell.Edge.RIGHT, 24)
    else:
        win.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        win.set_skip_taskbar_hint(True)
        if is_homescreen:
            win.set_keep_below(True)
        else:
            win.set_keep_above(True)

    # CSS
    css_provider = Gtk.CssProvider()
    css_parts = []
    if COLORS_FILE.exists():
        css_parts.append(COLORS_FILE.read_bytes())
    css_parts.append(DEFAULT_CSS)
    if STYLE_FILE.exists():
        css_parts.append(STYLE_FILE.read_bytes())
    css_provider.load_from_data(b"\n".join(css_parts))

    screen = Gdk.Screen.get_default()
    if screen:
        Gtk.StyleContext.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    outer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    outer_box.get_style_context().add_class("quick-shelf-window")

    stack = Gtk.Stack()
    stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
    stack.set_transition_duration(150)

    content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    content_box.get_style_context().add_class("qs-mainbox")
    preview_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    preview_box.get_style_context().add_class("qs-preview-overlay")

    stack.add_named(content_box, "content")
    stack.add_named(preview_box, "preview")
    outer_box.pack_start(stack, True, True, 0)
    win.add(outer_box)

    active_view = ["both"]

    def rebuild():
        for ch in content_box.get_children():
            content_box.remove(ch)

        shortcuts = get_shortcuts()
        images = get_images()

        # Header
        hdr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        hdr.get_style_context().add_class("qs-header")

        t_lbl = Gtk.Label(label="\U000f10ac Quick Shelf")
        t_lbl.get_style_context().add_class("qs-title")
        hdr.pack_start(t_lbl, False, False, 0)

        badge = Gtk.Label(label=str(len(shortcuts) + len(images)))
        badge.get_style_context().add_class("qs-badge")
        hdr.pack_start(badge, False, False, 0)

        pills = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        b_all = Gtk.Button(label="All")
        b_app = Gtk.Button(label="Apps")
        b_med = Gtk.Button(label="Media")
        for b in (b_all, b_app, b_med):
            b.get_style_context().add_class("qs-btn")

        if active_view[0] == "apps":
            b_app.get_style_context().add_class("qs-tab-active")
        elif active_view[0] == "media":
            b_med.get_style_context().add_class("qs-tab-active")
        else:
            b_all.get_style_context().add_class("qs-tab-active")

        def set_v(v):
            active_view[0] = v
            rebuild()

        b_all.connect("clicked", lambda _: set_v("both"))
        b_app.connect("clicked", lambda _: set_v("apps"))
        b_med.connect("clicked", lambda _: set_v("media"))
        pills.pack_start(b_all, False, False, 0)
        pills.pack_start(b_app, False, False, 0)
        pills.pack_start(b_med, False, False, 0)
        hdr.pack_end(pills, False, False, 0)
        content_box.pack_start(hdr, False, False, 0)

        # Shortcuts Section
        if active_view[0] in ("both", "apps"):
            sec = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            s_lbl = Gtk.Label(label="Shortcuts")
            s_lbl.get_style_context().add_class("qs-section-title")
            sec.pack_start(s_lbl, False, False, 0)
            content_box.pack_start(sec, False, False, 0)

            flow = Gtk.FlowBox()
            flow.set_valign(Gtk.Align.START)
            flow.set_max_children_per_line(5)
            flow.set_min_children_per_line(3)
            flow.set_selection_mode(Gtk.SelectionMode.NONE)
            flow.set_row_spacing(6)
            flow.set_column_spacing(6)

            icon_theme = Gtk.IconTheme.get_default()

            for item in shortcuts:
                card = Gtk.Button()
                card.get_style_context().add_class("qs-app-card")
                c_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
                c_box.set_halign(Gtk.Align.CENTER)

                icon_name = item.get("icon", "application-x-executable")
                if icon_theme and icon_theme.has_icon(icon_name):
                    img = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.DND)
                else:
                    img = Gtk.Image.new_from_icon_name("application-x-executable", Gtk.IconSize.DND)

                c_box.pack_start(img, False, False, 0)
                name_lbl = Gtk.Label(label=item.get("name", "App"))
                name_lbl.get_style_context().add_class("qs-app-label")
                name_lbl.set_ellipsize(3)
                name_lbl.set_max_width_chars(8)
                c_box.pack_start(name_lbl, False, False, 0)
                card.add(c_box)

                exec_cmd = item.get("exec", "")
                card.connect("clicked", lambda _, cmd=exec_cmd: subprocess.Popen(cmd, shell=True))
                flow.add(card)

            content_box.pack_start(flow, False, False, 0)

        if active_view[0] == "both":
            content_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 4)

        # Media Section
        if active_view[0] in ("both", "media"):
            m_sec = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            m_lbl = Gtk.Label(label="Image Shelf")
            m_lbl.get_style_context().add_class("qs-section-title")
            m_sec.pack_start(m_lbl, False, False, 0)

            clr_btn = Gtk.Button(label="Clear")
            clr_btn.get_style_context().add_class("qs-btn")
            def clear_all(_):
                for img in get_images():
                    try:
                        Path(img["path"]).unlink(missing_ok=True)
                    except Exception:
                        pass
                save_json(IMAGES_FILE, [])
                rebuild()
            clr_btn.connect("clicked", clear_all)
            m_sec.pack_end(clr_btn, False, False, 0)
            content_box.pack_start(m_sec, False, False, 0)

            if not images:
                dz = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
                dz.get_style_context().add_class("qs-dropzone")
                dz_icon = Gtk.Image.new_from_icon_name("insert-image", Gtk.IconSize.DIALOG)
                dz.pack_start(dz_icon, False, False, 0)
                dz_lbl = Gtk.Label(label="Drop images here from file manager or browser")
                dz_lbl.get_style_context().add_class("qs-app-label")
                dz.pack_start(dz_lbl, False, False, 0)
                content_box.pack_start(dz, False, False, 0)
            else:
                scr = Gtk.ScrolledWindow()
                scr.set_min_content_height(100)
                scr.set_max_content_height(240)
                scr.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

                i_flow = Gtk.FlowBox()
                i_flow.set_valign(Gtk.Align.START)
                i_flow.set_max_children_per_line(4)
                i_flow.set_min_children_per_line(3)
                i_flow.set_selection_mode(Gtk.SelectionMode.NONE)
                i_flow.set_row_spacing(8)
                i_flow.set_column_spacing(8)

                for item in images:
                    i_card = Gtk.Button()
                    i_card.get_style_context().add_class("qs-image-card")
                    p_str = item.get("path", "")
                    try:
                        pb = GdkPixbuf.Pixbuf.new_from_file_at_scale(p_str, 76, 76, True)
                        i_widget = Gtk.Image.new_from_pixbuf(pb)
                    except Exception:
                        i_widget = Gtk.Image.new_from_icon_name("image-missing", Gtk.IconSize.DIALOG)

                    i_card.add(i_widget)
                    i_card.connect("clicked", lambda _, it=item: show_preview(it))

                    # Drag Source
                    i_card.drag_source_set(
                        Gdk.ModifierType.BUTTON1_MASK,
                        [Gtk.TargetEntry.new("text/uri-list", Gtk.TargetFlags.OTHER_APP, 0)],
                        Gdk.DragAction.COPY
                    )
                    def on_drag_get(_widget, _context, data, _info, _time, path=p_str):
                        data.set_uris([f"file://{path}"])
                    i_card.connect("drag-data-get", on_drag_get)

                    i_flow.add(i_card)

                scr.add(i_flow)
                content_box.pack_start(scr, True, True, 0)

        content_box.show_all()
        stack.set_visible_child_name("content")

    def show_preview(item):
        for ch in preview_box.get_children():
            preview_box.remove(ch)

        top = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        back_b = Gtk.Button(label="← Back")
        back_b.get_style_context().add_class("qs-btn")
        back_b.connect("clicked", lambda _: stack.set_visible_child_name("content"))
        top.pack_start(back_b, False, False, 0)

        name_l = Gtk.Label(label=item.get("name", "Image"))
        name_l.get_style_context().add_class("qs-title")
        name_l.set_ellipsize(3)
        top.pack_start(name_l, True, True, 0)
        preview_box.pack_start(top, False, False, 0)

        p_str = item.get("path", "")
        try:
            pb = GdkPixbuf.Pixbuf.new_from_file_at_scale(p_str, 340, 220, True)
            img = Gtk.Image.new_from_pixbuf(pb)
            preview_box.pack_start(img, False, False, 6)
        except Exception:
            pass

        info_lbl = Gtk.Label(label=f"Size: {item.get('size_bytes', 0) // 1024} KB")
        info_lbl.get_style_context().add_class("qs-app-label")
        preview_box.pack_start(info_lbl, False, False, 0)

        act = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        act.set_halign(Gtk.Align.CENTER)

        b_copy = Gtk.Button(label="Copy Path")
        b_copy.get_style_context().add_class("qs-btn")
        def copy_path(_):
            cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            cb.set_text(p_str, -1)
            subprocess.Popen(["wl-copy", p_str])
        b_copy.connect("clicked", copy_path)
        act.pack_start(b_copy, False, False, 0)

        b_open = Gtk.Button(label="Open Viewer")
        b_open.get_style_context().add_class("qs-btn")
        b_open.connect("clicked", lambda _: subprocess.Popen(["xdg-open", p_str]))
        act.pack_start(b_open, False, False, 0)

        b_del = Gtk.Button(label="Delete")
        b_del.get_style_context().add_class("qs-btn")
        def del_img(_):
            imgs = [i for i in get_images() if i.get("id") != item.get("id")]
            save_json(IMAGES_FILE, imgs)
            Path(p_str).unlink(missing_ok=True)
            rebuild()
        b_del.connect("clicked", del_img)
        act.pack_start(b_del, False, False, 0)

        preview_box.pack_start(act, False, False, 6)
        preview_box.show_all()
        stack.set_visible_child_name("preview")

    # Drop target
    win.drag_dest_set(
        Gtk.DestDefaults.ALL,
        [Gtk.TargetEntry.new("text/uri-list", Gtk.TargetFlags.OTHER_APP, 0)],
        Gdk.DragAction.COPY
    )

    def on_drag_received(_w, _c, _x, _y, data, _info, _time):
        uris = data.get_uris()
        changed = False
        images = get_images()
        for uri in uris:
            p, _ = GLib.filename_from_uri(uri)
            src_path = Path(p)
            if src_path.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".bmp"):
                dest = IMAGES_DIR / f"{int(time.time())}_{src_path.name}"
                shutil.copy2(src_path, dest)
                images.insert(0, {
                    "id": f"img_{int(time.time())}_{src_path.stem}",
                    "name": src_path.name,
                    "path": str(dest),
                    "added_at": int(time.time()),
                    "size_bytes": dest.stat().st_size
                })
                changed = True
        if changed:
            save_json(IMAGES_FILE, images)
            rebuild()

    win.connect("drag-data-received", on_drag_received)

    rebuild()
    win.show_all()

    # IPC Handler
    def check_ipc():
        try:
            conn, _ = server_sock.accept()
            msg = conn.recv(1024).decode("utf-8").strip()
            if msg == "toggle":
                if win.is_visible():
                    win.hide()
                else:
                    rebuild()
                    win.show_all()
                    win.present()
                conn.sendall(b"ok\n")
            elif msg == "show":
                rebuild()
                win.show_all()
                win.present()
                conn.sendall(b"ok\n")
            elif msg == "hide":
                win.hide()
                conn.sendall(b"ok\n")
            elif msg == "refresh":
                rebuild()
                conn.sendall(b"ok\n")
            elif msg == "reload-style":
                if STYLE_FILE.exists():
                    css_provider.load_from_path(str(STYLE_FILE))
                conn.sendall(b"ok\n")
            else:
                conn.sendall(b"unknown\n")
            conn.close()
        except BlockingIOError:
            pass
        except Exception:
            pass
        return True

    GLib.timeout_add(50, check_ipc)

    try:
        Gtk.main()
    finally:
        if SOCKET_FILE.exists():
            SOCKET_FILE.unlink(missing_ok=True)

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "--toggle"

    if action in ("--help", "-h"):
        print("Usage: quick-shelf [--homescreen|--toggle|--popup|--status|--reload-style]")
        return
    if action in ("--version", "-v"):
        print("quick-shelf 0.1.0 (fallback)")
        return
    if action == "--status":
        print_status()
        return
    if action == "--reload-style":
        res = send_ipc("reload-style")
        print("Reloaded style" if res == "ok" else "quick-shelf not running")
        return
    if action == "--toggle":
        res = send_ipc("toggle")
        if res == "ok":
            return
        launch_gui(is_homescreen=False)
        return
    if action == "--popup":
        res = send_ipc("show")
        if res == "ok":
            return
        launch_gui(is_homescreen=False)
        return
    if action in ("--homescreen", "--desktop"):
        launch_gui(is_homescreen=True)
        return

    print(f"Unknown action: {action}")

if __name__ == "__main__":
    main()
