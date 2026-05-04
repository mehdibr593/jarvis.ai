#!/usr/bin/env python3
"""Conversation history logger for J.A.R.V.I.S"""
import json
import os
from datetime import datetime
from pathlib import Path

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

def log_conversation(speaker: str, message: str):
    """Log a conversation turn with timestamp."""
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = LOGS_DIR / f"conversation_{today}.json"
    
    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "speaker": speaker,
        "message": message
    }
    
    try:
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        else:
            history = []
        
        history.append(entry)
        
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Logger] Failed: {e}")

def get_today_summary() -> str:
    """Get a summary of today\'s conversations."""
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = LOGS_DIR / f"conversation_{today}.json"
    
    if not log_file.exists():
        return "No conversations today yet."
    
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            history = json.load(f)
        return f"{len(history)} messages exchanged today."
    except:
        return "Could not load conversation history."
