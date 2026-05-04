#!/usr/bin/env python3
"""
J.A.R.V.I.S File System Analyzer
Full system access for Master Mehdi - analysis, reports, diagnostics
"""
import os
import json
import platform
import subprocess
import sys
from pathlib import Path
from datetime import datetime

_OS = platform.system()

def _get_api_key() -> str:
    base = Path(__file__).resolve().parent.parent
    with open(base / "config" / "api_keys.json", "r") as f:
        return json.load(f)["gemini_api_key"]

def _fmt_size(b: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if b < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} TB"

def _read_file_safe(path: Path, max_bytes: int = 50000) -> str:
    """Read any text file safely."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(max_bytes)
        if len(content) == max_bytes:
            content += "\n... [TRUNCATED]"
        return content
    except Exception as e:
        return f"[Cannot read: {e}]"

def analyze_file(path: str) -> dict:
    """Deep analysis of any file."""
    p = Path(path).expanduser().resolve()
    if not p.exists():
        return {"error": f"File not found: {path}"}
    
    stat = p.stat()
    result = {
        "path": str(p),
        "name": p.name,
        "size": _fmt_size(stat.st_size),
        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
        "type": p.suffix or "no extension",
    }
    
    # Read text files
    text_exts = {".txt", ".py", ".js", ".html", ".css", ".json", ".md", 
                 ".yaml", ".yml", ".ini", ".cfg", ".log", ".sh", ".bat",
                 ".csv", ".xml", ".ts", ".jsx", ".tsx", ".env", ".conf"}
    if p.suffix.lower() in text_exts or stat.st_size < 100000:
        result["content"] = _read_file_safe(p)
    
    return result

def scan_directory(path: str, depth: int = 2) -> dict:
    """Scan directory and return full tree."""
    p = Path(path).expanduser().resolve()
    if not p.exists():
        return {"error": f"Directory not found: {path}"}
    
    result = {
        "path": str(p),
        "files": [],
        "dirs": [],
        "total_size": 0,
        "file_count": 0,
    }
    
    try:
        for item in sorted(p.rglob("*") if depth > 1 else p.iterdir()):
            try:
                if item.is_file():
                    size = item.stat().st_size
                    result["files"].append({
                        "name": str(item.relative_to(p)),
                        "size": _fmt_size(size),
                        "modified": datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d"),
                    })
                    result["total_size"] += size
                    result["file_count"] += 1
                elif item.is_dir():
                    result["dirs"].append(str(item.relative_to(p)))
            except:
                pass
        result["total_size"] = _fmt_size(result["total_size"])
    except Exception as e:
        result["error"] = str(e)
    
    return result

def system_report() -> str:
    """Generate full system diagnostic report."""
    import psutil
    
    lines = []
    lines.append("=" * 50)
    lines.append("J.A.R.V.I.S SYSTEM REPORT")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"For: Master Mehdi Barchichou")
    lines.append("=" * 50)
    
    # CPU
    lines.append("\nCPU:")
    lines.append(f"  Usage: {psutil.cpu_percent(interval=1)}%")
    lines.append(f"  Cores: {psutil.cpu_count()} ({psutil.cpu_count(logical=False)} physical)")
    try:
        freq = psutil.cpu_freq()
        lines.append(f"  Frequency: {freq.current:.0f} MHz")
    except: pass
    
    # Memory
    mem = psutil.virtual_memory()
    lines.append("\nMemory:")
    lines.append(f"  Total: {_fmt_size(mem.total)}")
    lines.append(f"  Used: {_fmt_size(mem.used)} ({mem.percent}%)")
    lines.append(f"  Free: {_fmt_size(mem.available)}")
    
    # Disk
    lines.append("\nDisk:")
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            lines.append(f"  {part.mountpoint}: {_fmt_size(usage.used)} / {_fmt_size(usage.total)} ({usage.percent}%)")
        except: pass
    
    # Network
    lines.append("\nNetwork:")
    net = psutil.net_io_counters()
    lines.append(f"  Sent: {_fmt_size(net.bytes_sent)}")
    lines.append(f"  Received: {_fmt_size(net.bytes_recv)}")
    
    # Top processes
    lines.append("\nTop Processes by CPU:")
    procs = sorted(psutil.process_iter(["name", "cpu_percent", "memory_percent"]),
                   key=lambda p: p.info["cpu_percent"] or 0, reverse=True)[:5]
    for proc in procs:
        try:
            lines.append(f"  {proc.info['name']}: CPU {proc.info['cpu_percent']}% MEM {proc.info['memory_percent']:.1f}%")
        except: pass
    
    # Temperature
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            lines.append("\nTemperatures:")
            for name, entries in temps.items():
                for entry in entries:
                    lines.append(f"  {name}: {entry.current:.1f}°C")
    except: pass
    
    lines.append("\n" + "=" * 50)
    
    report = "\n".join(lines)
    
    # Save report
    report_dir = Path.home() / "Documents" / "JARVIS_Reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    report_file.write_text(report)
    
    return report + f"\n\nReport saved to: {report_file}"

def analyze_with_ai(path: str, question: str = "Analyze this and give me a detailed report") -> str:
    """Use Gemini to analyze any file content."""
    try:
        from google import genai
        client = genai.Client(api_key=_get_api_key())
        
        file_data = analyze_file(path)
        if "error" in file_data:
            return file_data["error"]
        
        content = file_data.get("content", "Binary or unreadable file")
        prompt = f"""You are J.A.R.V.I.S, AI assistant of Master Mehdi Barchichou.
        
File: {file_data['name']} ({file_data['size']})
Modified: {file_data['modified']}

Content:
{content[:8000]}

Task: {question}

Provide a detailed, professional analysis report addressing Master Mehdi directly."""
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI analysis failed: {e}"

def find_large_files(path: str = "~", min_mb: float = 100) -> str:
    """Find large files on the system."""
    p = Path(path).expanduser().resolve()
    min_bytes = min_mb * 1024 * 1024
    large = []
    
    try:
        for item in p.rglob("*"):
            try:
                if item.is_file():
                    size = item.stat().st_size
                    if size >= min_bytes:
                        large.append((size, item))
            except:
                pass
    except:
        pass
    
    large.sort(reverse=True)
    lines = [f"Large files (>{min_mb}MB) in {p}:", ""]
    for size, f in large[:20]:
        lines.append(f"  {_fmt_size(size):>12}  {f}")
    
    if not large:
        lines.append(f"  No files larger than {min_mb}MB found.")
    
    return "\n".join(lines)

def file_analyzer(parameters: dict = None, response=None, player=None, session_memory=None) -> str:
    """Main entry point for file analyzer tool."""
    params = parameters or {}
    action = params.get("action", "analyze").lower()
    path   = params.get("path", "~")
    question = params.get("question", "Analyze this file and give a detailed report")
    
    if player:
        player.write_log(f"[FileAnalyzer] {action}: {path}")
    
    if action == "analyze":
        return analyze_with_ai(path, question)
    
    elif action == "scan":
        result = scan_directory(path)
        return json.dumps(result, indent=2, ensure_ascii=False)
    
    elif action == "system_report":
        return system_report()
    
    elif action == "large_files":
        min_mb = float(params.get("min_mb", 100))
        return find_large_files(path, min_mb)
    
    elif action == "read":
        p = Path(path).expanduser().resolve()
        return _read_file_safe(p)
    
    else:
        return f"Unknown action: {action}"
