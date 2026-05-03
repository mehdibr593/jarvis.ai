#!/usr/bin/env python3
"""Security Monitor for J.A.R.V.I.S - Master Mehdi"""
import psutil
import subprocess
import platform
from datetime import datetime

_OS = platform.system()

_SUSPICIOUS = [
    "keylogger", "miner", "cryptominer", "ransomware",
    "trojan", "backdoor", "rootkit", "spyware"
]

def scan_processes() -> str:
    """Scan running processes for suspicious activity."""
    suspicious = []
    high_cpu   = []
    
    for proc in psutil.process_iter(["name", "cpu_percent", "memory_percent", "pid"]):
        try:
            name = proc.info["name"].lower()
            cpu  = proc.info["cpu_percent"] or 0
            
            if any(s in name for s in _SUSPICIOUS):
                suspicious.append(f"  ⚠️  SUSPICIOUS: {proc.info['name']} (PID {proc.info['pid']})")
            
            if cpu > 80:
                high_cpu.append(f"  🔥 HIGH CPU: {proc.info['name']} ({cpu}%)")
        except:
            pass
    
    lines = ["SECURITY SCAN REPORT", "=" * 40]
    
    if suspicious:
        lines.append("\n⚠️  SUSPICIOUS PROCESSES DETECTED:")
        lines.extend(suspicious)
    else:
        lines.append("\n✅ No suspicious processes detected")
    
    if high_cpu:
        lines.append("\n⚠️  High CPU processes:")
        lines.extend(high_cpu[:5])
    
    lines.append(f"\nScan completed: {datetime.now().strftime('%H:%M:%S')}")
    return "\n".join(lines)

def check_open_ports() -> str:
    """Check open network connections."""
    try:
        conns = psutil.net_connections()
        listening = [c for c in conns if c.status == "LISTEN"]
        lines = [f"Open ports: {len(listening)}"]
        for c in listening[:10]:
            lines.append(f"  Port {c.laddr.port}")
        return "\n".join(lines)
    except Exception as e:
        return f"Port check failed: {e}"

def security_monitor(parameters: dict = None, response=None, player=None, session_memory=None) -> str:
    params = parameters or {}
    action = params.get("action", "scan").lower()
    
    if player:
        player.write_log(f"[Security] {action}")
    
    if action == "scan":
        return scan_processes()
    elif action == "ports":
        return check_open_ports()
    elif action == "full":
        return scan_processes() + "\n\n" + check_open_ports()
    return scan_processes()
