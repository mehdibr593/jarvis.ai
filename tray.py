import gi
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Gtk', '3.0')
from gi.repository import AppIndicator3, Gtk
import subprocess
import psutil
import os
from PIL import Image, ImageDraw, ImageFilter
import tempfile

def create_icon(active=False):
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    if active:
        # Glowing blue orb - RUNNING
        for i in range(8, 0, -1):
            r = int(28 + i * 1.5)
            alpha = int(15 * i)
            d.ellipse([size//2-r, size//2-r, size//2+r, size//2+r],
                     fill=(0, 150, 255, alpha))
        # Core
        d.ellipse([12, 12, 52, 52], fill=(0, 180, 255, 255))
        d.ellipse([20, 20, 44, 44], fill=(0, 220, 255, 255))
        d.ellipse([27, 27, 37, 37], fill=(255, 255, 255, 255))
    else:
        # Dim orb - STOPPED
        d.ellipse([12, 12, 52, 52], fill=(0, 60, 100, 200))
        d.ellipse([22, 22, 42, 42], fill=(0, 90, 140, 200))
        d.ellipse([29, 29, 35, 35], fill=(0, 140, 180, 180))
    
    path = f'/tmp/jarvis_icon_{"on" if active else "off"}.png'
    img.save(path)
    return path

def is_running():
    for p in psutil.process_iter(['cmdline']):
        try:
            if 'main.py' in ' '.join(p.info['cmdline']):
                return True
        except:
            pass
    return False

def start_jarvis(_):
    if not is_running():
        subprocess.Popen(
            ['/home/mehdi2005/Downloads/Mark-XXXIX-main/venv_final/bin/python', 'main.py'],
            cwd='/home/mehdi2005/Downloads/Mark-XXXIX-main'
        )
        indicator.set_icon_full(create_icon(True), "JARVIS Running")
        indicator.set_title("J.A.R.V.I.S — ONLINE")

def stop_jarvis(_):
    for p in psutil.process_iter(['cmdline', 'pid']):
        try:
            if 'main.py' in ' '.join(p.info['cmdline']):
                p.kill()
        except:
            pass
    indicator.set_icon_full(create_icon(False), "JARVIS Stopped")
    indicator.set_title("J.A.R.V.I.S — OFFLINE")

# Create icons
icon_path = create_icon(is_running())

indicator = AppIndicator3.Indicator.new_with_path(
    "jarvis", icon_path, 
    AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
    "/tmp"
)
indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
indicator.set_title("J.A.R.V.I.S")

menu = Gtk.Menu()

title_item = Gtk.MenuItem(label="J.A.R.V.I.S — Mehdi Barchichou")
title_item.set_sensitive(False)
menu.append(title_item)

sep0 = Gtk.SeparatorMenuItem()
menu.append(sep0)

start_item = Gtk.MenuItem(label="▶  Start J.A.R.V.I.S")
start_item.connect("activate", start_jarvis)
menu.append(start_item)

stop_item = Gtk.MenuItem(label="⏹  Stop J.A.R.V.I.S")
stop_item.connect("activate", stop_jarvis)
menu.append(stop_item)

sep = Gtk.SeparatorMenuItem()
menu.append(sep)

quit_item = Gtk.MenuItem(label="✕  Quit Tray")
quit_item.connect("activate", lambda _: Gtk.main_quit())
menu.append(quit_item)

menu.show_all()
indicator.set_menu(menu)

# Auto start tray on login
autostart = """[Desktop Entry]
Type=Application
Name=J.A.R.V.I.S Tray
Exec=python3 /home/mehdi2005/Downloads/Mark-XXXIX-main/tray.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true"""

os.makedirs(os.path.expanduser("~/.config/autostart"), exist_ok=True)
with open(os.path.expanduser("~/.config/autostart/jarvis-tray.desktop"), "w") as f:
    f.write(autostart)

Gtk.main()
