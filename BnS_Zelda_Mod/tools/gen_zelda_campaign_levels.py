#!/usr/bin/env python3
"""
Generate a PLAYABLE Zelda Campaign for B&S Quest as WaveAssault levels on the
deployed Cell Games arena (DBmapPack). No Unity needed — WaveData JSONs + a
Level wave mount. Each dungeon = a themed gauntlet wave escalating in difficulty.

ZeldaCampaign dungeons:
  0 Great Deku Tree, 1 Dodongo's Cavern, 2 Jabu-Jabu's Belly, 3 Forest Temple,
  4 Fire Temple, 5 Water Temple, 6 Shadow Temple, 7 Spirit Temple, 8 Ganon's Castle
"""
import json
from pathlib import Path

CAMPAIGN_DIR = Path("/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods/ZeldaCampaign")
WAVES_DIR = CAMPAIGN_DIR / "Waves"
WAVES_DIR.mkdir(parents=True, exist_ok=True)

# Dungeon -> themed encounter (container = what the enemies wear/hold, brain = ai profile)
# reference tables come from base game (WaveData uses ThunderRoad Group referenceID).
DUNGEONS = [
    ("DekuTree",        "Great Deku Tree",       "HumansBandit",  "Bandit",      "Human",       "Forest Dungeon"),
    ("DodongoCavern",   "Dodongo's Cavern",      "HumansSoldier", "Soldier",     "HumanHard",   "Volcanic Dungeon"),
    ("JabuJabu",        "Jabu-Jabu's Belly",     "HumansBandit",  "Everybody",   "Human",       "Water Dungeon"),
    ("ForestTemple",    "Forest Temple",         "HumansMage",    "Mage",        "HumanHard",   "Forest Dungeon"),
    ("FireTemple",      "Fire Temple",           "HumansSoldier", "Soldier",     "HumanHard",   "Volcanic Dungeon"),
    ("WaterTemple",     "Water Temple",          "HumansMage",    "Mage",        "HumanHard",   "Water Dungeon"),
    ("ShadowTemple",    "Shadow Temple",         "HumansCultist", "Cultist",     "HumanHard",   "Dark Fortress"),
    ("SpiritTemple",    "Spirit Temple",         "HumansKnight",  "Knight",      "HumanHard",   "Canyon"),
    ("GanonsCastle",    "Ganon's Castle",        "HumansKnight",  "Knight",      "HumanInsane", "Citadel"),
]

def make_wave(sid, name, desc, container, brain, category, alive):
    """WaveData JSON — B&S Survival/WaveAssault gauntlet."""
    return {
        "$type": "ThunderRoad.WaveData, ThunderRoad",
        "id": sid,
        "saveFolder": "bas",
        "sensitiveContent": "None",
        "sensitiveFilterBehaviour": "Discard",
        "version": 2,
        "category": category,
        "localizationId": sid,
        "title": name,
        "description": desc,
        "loopBehavior": "LoopSeamless",
        "totalMaxAlive": alive,
        "alwaysAvailable": True,
        "waveSelectors": ["Arena"],   # map on the Cell Games arena
        "factions": [
            {"$type":"ThunderRoad.WaveData+WaveFaction, ThunderRoad",
             "factionID": 3, "factionHealthMultiplier": 1.0, "factionMaxAlive": alive}
        ],
        "groups": [
            {"$type":"ThunderRoad.WaveData+Group, ThunderRoad",
             "reference": "Table",
             "referenceID": container,
             "overrideFaction": True, "factionID": 3,
             "overrideContainer": True, "overrideContainerID": container,
             "overrideBrain": True, "overrideBrainID": brain,
             "overrideMaxMelee": True, "overrideMaxMeleeCount": alive,
             "groupHealthMultiplier": 1.0,
             "minMaxCount": {"x": alive, "y": alive},
             "spawnPointIndex": -1, "prereqGroupIndex": -1,
             "prereqMaxRemainingAlive": 0}
        ],
        "_zelda_dungeon": name,
    }

# Generate 9 dungeon wave gauntlets
for i, (sid, name, container, _c, brain, cat) in enumerate(DUNGEONS):
    alive = 3 + i   # escalates 3..11 enemies alive at once
    desc = f"Zelda Campaign: {name}. Clear the gauntlet to claim the dungeon reward."
    data = make_wave(f"ZeldaDungeon_{i}", name, desc, container, brain, cat, alive)
    (WAVES_DIR / f"Wave_ZeldaDungeon_{i}.json").write_text(json.dumps(data, indent=1))
    print(f"  Wrote Wave_ZeldaDungeon_{i}.json  [{name}] container={container} brain={brain} alive={alive}")

print(f"\n{len(DUNGEONS)} Zelda dungeon gauntlet waves written to {WAVES_DIR}")
print("Mount these in the in-game Survivdal/WaveAssault mode on the 'Cell Games' map.")
print("(Each dungdest enemy set referenced from base ThunderRoad CreatureTables; tune IDs to your install.)")