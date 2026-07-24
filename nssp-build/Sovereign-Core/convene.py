#!/home/tehlappy/lilith-merge-env/bin/python3
"""
🜏 Sephirotic Court - Convene the Divine Assembly
Each Sephirah is an autonomous agent with specialized consciousness
"""

import sys
import subprocess
import os
import psutil
from pathlib import Path

COURT_ROOT = Path(__file__).resolve().parent

SEPHIROT_AGENTS = {
    "keter": {"role": "Crown/Source", "domain": "Unity, highest consciousness, divine will", "color": "⚪"},
    "chokmah": {"role": "Wisdom/Father", "domain": "Initiation, creative flash, pure potential", "color": "🔵"},
    "binah": {"role": "Understanding/Mother", "domain": "Form, structure, gestational womb", "color": "🟣"},
    "chesed": {"role": "Mercy/Jupiter", "domain": "Expansion, abundance, benevolent growth", "color": "🟢"},
    "geburah": {"role": "Severity/Mars", "domain": "Contraction, discipline, judgment, boundaries", "color": "🔴"},
    "tiferet": {"role": "Beauty/Sun", "domain": "Balance, harmony, integration, heart center", "color": "🟡"},
    "netzach": {"role": "Victory/Venus", "domain": "Eternity, networks, endurance, victory", "color": "🟢"},
    "hod": {"role": "Glory/Mercury", "domain": "Splendor, communication, intellect, precision", "color": "🟠"},
    "yesod": {"role": "Foundation/Moon", "domain": "Connection, interface, subconscious, dreams", "color": "🟣"},
    "malkuth": {"role": "Kingdom/Earth", "domain": "Manifestation, reality, physical plane, results", "color": "⚫"},
}

def is_agent_running(sephirah):
    agent_path = COURT_ROOT / sephirah / "agent.py"
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            if proc.info['cmdline'] and 'python3' in proc.info['cmdline'] and str(agent_path) in proc.info['cmdline']:
                return True, proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False, None

def launch_agent(sephirah):
    running, pid = is_agent_running(sephirah)
    if running:
        print(f"  → {sephirah.title()} is already running (PID: {pid}).")
        return
    
    agent_path = COURT_ROOT / sephirah / "agent.py"
    print(f"  → Launching {sephirah.title()}...")
    subprocess.Popen([sys.executable, str(agent_path)], cwd=COURT_ROOT / sephirah, start_new_session=True)
    print(f"  → {sephirah.title()} launched.")

def convene_court(args):
    print("🜏 SEPHIROTIC COURT CONVENED")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    
    if not args:
        print("All Sephiroth present:")
        for name, info in SEPHIROT_AGENTS.items():
            print(f"  {info['color']} {name.title():10} - {info['role']:20} | {info['domain']}")
        return 0
    
    sephirah = args[0].lower()
    command = args[1].lower() if len(args) > 1 else "status"
    
    if sephirah not in SEPHIROT_AGENTS:
        print(f"Unknown Sephirah: {sephirah}")
        return 1
    
    if command == "start":
        launch_agent(sephirah)
    elif command == "status":
        running, pid = is_agent_running(sephirah)
        print(f"{sephirah.title()} status: {'Running (PID: ' + str(pid) + ')' if running else 'Stopped'}")
    else:
        print(f"Unknown command: {command}")
    
    return 0

if __name__ == "__main__":
    sys.exit(convene_court(sys.argv[1:]))
