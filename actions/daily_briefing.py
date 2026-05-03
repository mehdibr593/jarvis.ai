#!/usr/bin/env python3
"""Daily Briefing for J.A.R.V.I.S - Master Mehdi"""
import json
import subprocess
from datetime import datetime
from pathlib import Path

def _get_api_key() -> str:
    base = Path(__file__).resolve().parent.parent
    with open(base / "config" / "api_keys.json") as f:
        return json.load(f)["gemini_api_key"]

def morning_briefing(parameters: dict = None, response=None, player=None, session_memory=None) -> str:
    """Generate a morning briefing for Master Mehdi."""
    now  = datetime.now()
    hour = now.hour
    
    if hour < 12:
        greeting = "Good morning"
    elif hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    day  = now.strftime("%A, %B %d, %Y")
    time = now.strftime("%I:%M %p")
    
    # Check reminders
    reminders_path = Path(__file__).resolve().parent.parent / "memory" / "reminders.json"
    reminders = []
    try:
        if reminders_path.exists():
            data = json.loads(reminders_path.read_text())
            today_str = now.strftime("%Y-%m-%d")
            reminders = [r for r in data if r.get("date") == today_str]
    except:
        pass
    
    lines = [
        f"{greeting}, Master Mehdi.",
        f"Today is {day}. The time is {time}.",
        "",
    ]
    
    if reminders:
        lines.append(f"You have {len(reminders)} reminder(s) today:")
        for r in reminders:
            lines.append(f"  • {r.get('time', '')} — {r.get('message', '')}")
        lines.append("")
    
    # System status
    try:
        import psutil
        cpu  = psutil.cpu_percent(interval=0.5)
        mem  = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        lines.append(f"System Status: CPU {cpu}% | RAM {mem}% | Disk {disk}%")
    except:
        pass
    
    lines.append("")
    lines.append("All systems are online and ready, Master Mehdi.")
    lines.append("How may I assist you today?")
    
    return "\n".join(lines)
