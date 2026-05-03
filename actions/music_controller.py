#!/usr/bin/env python3
"""Music Controller for J.A.R.V.I.S - Master Mehdi"""
import subprocess
import platform
import time

_OS = platform.system()

def _run(cmd: list) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return r.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def spotify_control(action: str, query: str = "") -> str:
    """Control Spotify via dbus on Linux."""
    if _OS == "Linux":
        dbus_base = ["dbus-send", "--print-reply", "--dest=org.mpris.MediaPlayer2.spotify",
                     "/org/mpris/MediaPlayer2"]
        if action == "play_pause":
            _run(dbus_base + ["org.mpris.MediaPlayer2.Player.PlayPause"])
            return "Spotify: Play/Pause toggled"
        elif action == "next":
            _run(dbus_base + ["org.mpris.MediaPlayer2.Player.Next"])
            return "Spotify: Next track"
        elif action == "prev":
            _run(dbus_base + ["org.mpris.MediaPlayer2.Player.Previous"])
            return "Spotify: Previous track"
        elif action == "stop":
            _run(dbus_base + ["org.mpris.MediaPlayer2.Player.Stop"])
            return "Spotify: Stopped"
        elif action == "status":
            result = _run(dbus_base + ["org.freedesktop.DBus.Properties.Get",
                         "string:org.mpris.MediaPlayer2.Player",
                         "string:Metadata"])
            return f"Spotify status: {result[:200]}"
        elif action == "play" and query:
            # Open Spotify with search
            subprocess.Popen(["spotify", f"--uri=spotify:search:{query}"])
            return f"Spotify: Searching for {query}"
    elif _OS == "Windows":
        import pyautogui
        if action == "play_pause":
            pyautogui.press("playpause")
            return "Play/Pause toggled"
        elif action == "next":
            pyautogui.press("nexttrack")
            return "Next track"
        elif action == "prev":
            pyautogui.press("prevtrack")
            return "Previous track"
    return f"Spotify {action} not supported on {_OS}"

def vlc_control(action: str, path: str = "") -> str:
    """Control VLC media player."""
    if _OS == "Linux":
        vlc_dbus = ["dbus-send", "--print-reply", "--dest=org.mpris.MediaPlayer2.vlc",
                    "/org/mpris/MediaPlayer2"]
        if action == "play_pause":
            _run(vlc_dbus + ["org.mpris.MediaPlayer2.Player.PlayPause"])
            return "VLC: Play/Pause toggled"
        elif action == "next":
            _run(vlc_dbus + ["org.mpris.MediaPlayer2.Player.Next"])
            return "VLC: Next"
        elif action == "stop":
            _run(vlc_dbus + ["org.mpris.MediaPlayer2.Player.Stop"])
            return "VLC: Stopped"
        elif action == "open" and path:
            subprocess.Popen(["vlc", path])
            return f"VLC: Opening {path}"
    return f"VLC {action} done"

def music_controller(parameters: dict = None, response=None, player=None, session_memory=None) -> str:
    params  = parameters or {}
    action  = params.get("action", "play_pause").lower()
    app     = params.get("app", "spotify").lower()
    query   = params.get("query", "")
    path    = params.get("path", "")
    
    if player:
        player.write_log(f"[Music] {app}: {action}")
    
    if app == "vlc":
        return vlc_control(action, path)
    else:
        return spotify_control(action, query)
