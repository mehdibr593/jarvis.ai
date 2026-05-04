#!/usr/bin/env python3
"""Network Monitor for J.A.R.V.I.S - Master Mehdi"""
import subprocess
import json
import platform
import socket
import time
from pathlib import Path

_OS = platform.system()

def get_wifi_devices() -> str:
    """Get all devices connected to WiFi."""
    try:
        if _OS == "Linux":
            result = subprocess.run(
                ["ip", "neigh", "show"],
                capture_output=True, text=True
            )
            lines = [l for l in result.stdout.strip().split("\n") if "REACHABLE" in l or "STALE" in l]
            if not lines:
                # Try arp-scan
                result = subprocess.run(
                    ["arp", "-a"], capture_output=True, text=True
                )
                lines = result.stdout.strip().split("\n")
            return "\n".join(lines) if lines else "No devices found"
        elif _OS == "Windows":
            result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
            return result.stdout
    except Exception as e:
        return f"Error: {e}"

def get_network_speed() -> str:
    """Quick network speed test using curl."""
    try:
        import psutil, time
        net1 = psutil.net_io_counters()
        time.sleep(1)
        net2 = psutil.net_io_counters()
        down = (net2.bytes_recv - net1.bytes_recv) / 1024
        up   = (net2.bytes_sent - net1.bytes_sent) / 1024
        return f"Download: {down:.1f} KB/s | Upload: {up:.1f} KB/s"
    except Exception as e:
        return f"Speed check failed: {e}"

def get_public_ip() -> str:
    """Get public IP address."""
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "5", "https://api.ipify.org"],
            capture_output=True, text=True
        )
        return f"Public IP: {result.stdout.strip()}"
    except:
        return "Could not get public IP"

def get_vpn_status() -> str:
    """Check VPN status."""
    try:
        if _OS == "Linux":
            result = subprocess.run(
                ["ip", "link", "show"],
                capture_output=True, text=True
            )
            vpn_interfaces = [l for l in result.stdout.split("\n") 
                            if any(v in l.lower() for v in ["tun", "tap", "vpn", "wg"])]
            if vpn_interfaces:
                return f"VPN ACTIVE: {vpn_interfaces[0].strip()}"
            return "VPN: Not connected"
        elif _OS == "Windows":
            result = subprocess.run(
                ["ipconfig"], capture_output=True, text=True
            )
            if "PPP" in result.stdout or "VPN" in result.stdout.upper():
                return "VPN: Connected"
            return "VPN: Not connected"
    except Exception as e:
        return f"VPN check failed: {e}"

def check_internet() -> str:
    """Check if internet is working."""
    try:
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return "Internet: Online ✓"
    except:
        return "Internet: OFFLINE ✗"

def full_network_report() -> str:
    """Generate complete network report."""
    lines = [
        "=" * 45,
        "J.A.R.V.I.S NETWORK REPORT",
        f"For: Master Mehdi Barchichou",
        "=" * 45,
        "",
        check_internet(),
        get_network_speed(),
        get_vpn_status(),
        get_public_ip(),
        "",
        "Connected Devices:",
        get_wifi_devices(),
        "=" * 45,
    ]
    return "\n".join(lines)

def network_monitor(parameters: dict = None, response=None, player=None, session_memory=None) -> str:
    params = parameters or {}
    action = params.get("action", "report").lower()
    
    if player:
        player.write_log(f"[Network] {action}")
    
    if action == "report":
        return full_network_report()
    elif action == "devices":
        return get_wifi_devices()
    elif action == "speed":
        return get_network_speed()
    elif action == "vpn":
        return get_vpn_status()
    elif action == "ip":
        return get_public_ip()
    elif action == "internet":
        return check_internet()
    else:
        return full_network_report()
