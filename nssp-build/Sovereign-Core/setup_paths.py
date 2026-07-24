#!/usr/bin/env python3
"""
🜏 Sovereign-Core Path Setup
Centralized path resolution for all sephirah agents.
Auto-detects the tree root from file location — no hardcoded paths.

Usage:
    from setup_paths import SOVEREIGN_ROOT, LILITH_ROOT, ensure_dirs
"""
import sys
from pathlib import Path

# --- Root detection -----------------------------------------------------------

SOVEREIGN_ROOT = Path(__file__).resolve().parent
LILITH_ROOT = SOVEREIGN_ROOT.parent                    # 🜏 Lilith/
REPOS_ROOT = LILITH_ROOT / "_shared" / "repos"
THRONE_ROOT = LILITH_ROOT / "_shared" / "THRONE"
MEMORY_ROOT = LILITH_ROOT / "_shared" / "memory"
COUNCIL_BUS_DIR = Path.home() / ".lilith" / "council_bus"

# Ensure SOVEREIGN_ROOT is on sys.path so council_bus is importable
if str(SOVEREIGN_ROOT) not in sys.path:
    sys.path.insert(0, str(SOVEREIGN_ROOT))

# --- Agent helpers ------------------------------------------------------------

def get_agent_dir(sephirah: str) -> Path:
    """Return the directory for a given sephirah agent."""
    return SOVEREIGN_ROOT / sephirah.lower().replace(" ", "-")

SEPHIROT = [
    "keter", "chokmah", "binah", "chesed", "geburah",
    "tiferet", "netzach", "hod", "yesod", "malkuth",
]

def ensure_dirs():
    """Ensure all required directories exist."""
    COUNCIL_BUS_DIR.mkdir(parents=True, exist_ok=True)
    for s in SEPHIROT:
        inbox = COUNCIL_BUS_DIR / s
        inbox.mkdir(exist_ok=True)
    return True


# --- Path reference map -------------------------------------------------------
# Each sephirah maps to its canonical repo in _shared/repos/
REPO_MAP = {
    "keter":   "msn-core",           # Crown — MSN orchestration
    "chokmah": "sovereign-ai-skills",  # Wisdom — skill generation
    "binah":   "lilith-core",          # Form — core library
    "chesed":  "babe-unified-field",   # Mercy — memory expansion
    "geburah": "legal-evidence",       # Severity — audit/security
    "tiferet": "msn-engine-integration",  # Beauty — convergence
    "netzach": "business-strategy",    # Victory — expansion
    "hod":     "docs-public",          # Splendor — communication
    "yesod":   "toolkit",              # Foundation — interface layer
    "malkuth": "lilith-systems-website",  # Kingdom — public output
}

# --- Quick smoke test ---------------------------------------------------------

if __name__ == "__main__":
    print(f"🜏  Sovereign Root:   {SOVEREIGN_ROOT}")
    print(f"   Lilith Root:       {LILITH_ROOT}")
    print(f"   Council Bus Dir:   {COUNCIL_BUS_DIR}")
    print(f"   THRONE:            {THRONE_ROOT}")
    print()
    ensure_dirs()
    print("✓ All directories ensured.")
    for s in SEPHIROT:
        d = get_agent_dir(s)
        has_agent = (d / "agent.py").is_file()
        print(f"  {s:12} {'✓' if has_agent else '✗ agent.py missing'}  ({d})")