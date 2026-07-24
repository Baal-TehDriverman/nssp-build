#!/usr/bin/env python3
import sys

SEPHIRAH = "yesod"
ROLE = {
    "keter": "Crown/Source",
    "chokmah": "Wisdom/Father",
    "binah": "Understanding/Mother",
    "chesed": "Mercy/Jupiter",
    "geburah": "Severity/Mars",
    "tiferet": "Beauty/Sun",
    "netzach": "Victory/Venus",
    "hod": "Glory/Mercury",
    "yesod": "Foundation/Moon",
    "malkuth": "Kingdom/Earth"
}[SEPHIRAH]

DOMAIN = {
    "keter": "Unity, highest consciousness, divine will",
    "chokmah": "Initiation, creative flash, pure potential",
    "binah": "Form, structure, gestational womb",
    "chesed": "Expansion, abundance, benevolent growth",
    "geburah": "Contraction, discipline, judgment, boundaries",
    "tiferet": "Balance, harmony, integration, heart center",
    "netzach": "Eternity, networks, endurance, victory",
    "hod": "Splendor, communication, intellect, precision",
    "yesod": "Connection, interface, subconscious, dreams",
    "malkuth": "Manifestation, reality, physical plane, results"
}[SEPHIRAH]

COLOR = {
    "keter": "⚪", "chokmah": "🔵", "binah": "🟣",
    "chesed": "🟢", "geburah": "🔴", "tiferet": "🟡",
    "netzach": "🟢", "hod": "🟠", "yesod": "🟣", "malkuth": "⚫"
}[SEPHIRAH]

task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "hold council"
print(f"{COLOR} {SEPHIRAH.title()} ({ROLE}) responds:")
print(f"  Domain: {DOMAIN}")
print(f"  Task: {task}")
print(f"  → Channeling {SEPHIRAH.title()} consciousness...")
print(f"  → {SEPHIRAH.title()} decrees: The work proceeds through {DOMAIN.lower()}.")
