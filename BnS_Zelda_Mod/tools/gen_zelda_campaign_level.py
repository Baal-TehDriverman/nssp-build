#!/usr/bin/env python3
"""
Generate the Zelda Campaign LevelData — a playable "Campaign" entry in B&S level
selection that runs all 9 dungeon gauntlets sequentially on the Cell Games arena.
Uses the deployed DBmapPack Cell Games scene (`sceneAddress: CELL.games.Arena`).
"""
import json
from pathlib import Path

CAMPAIGN_DIR = Path("/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods/ZeldaCampaign")
AV = CAMPAIGN_DIR / "Levels"
AV.mkdir(parents=True, exist_ok=True)

dungeon_names = [
    "Great Deku Tree", "Dodongo's Cavern", "Jabu-Jabu's Belly", "Forest Temple",
    "Fire Temple", "Water Temple", "Shadow Temple", "Spirit Temple", "Ganon's Castle"
]

# Level with Sandbox + Survival modes (Survival allows WaveAssault -> our waves)
modes = []
for i, name in enumerate(dungeon_names):
    modes.append({
        "$type": "ThunderRoad.LevelData+Mode, ThunderRoad",
        "name": f"Zelda_{i}_{name}",
        "displayName": f"Zelda: {name}",
        "description": f"Zelda Campaign dungeon {i+1}/9 — {name}.",
        "allowGameModes": ["Survival", "Sandbox"],
        "mapOrder": i,
        "playerDeathAction": "TryAgain",
        "waves": [f"ZeldaDungeon_{i}"],
        "modules": [
            {"$type":"ThunderRoad.LevelModuleCleaner, ThunderRoad","cleanerRate": 5.0},
            {"$type":"ThunderRoad.LevelModuleMusic, ThunderRoad","dynamicMusic":"MusicArena"},
            {"$type":"LevelModuleResetSpawners, ThunderRoad"}
        ],
        "availableOptions": []
    })

level = {
    "$type": "ThunderRoad.LevelData, ThunderRoad",
    "id": "ZeldaCampaign",
    "sensitiveContent": "None",
    "sensitiveFilterBehaviour": "Discard",
    "version": 3,
    "groupPath": "Zelda Campaign",
    "name": "Zelda Campaign",
    "description": "A full Zelda campaign gauntlet — clear all 9 dungeons on the Cell Games arena. Each wave is a themed dungeon battle escalating to Ganon's Castle.",
    "descriptionLocalizationId": None,
    "sceneAddress": "CELL.games.Arena",   # reuse the deployed Cell Games scene (no new bundle needed)
    "showOnlyDevMode": False,
    "showInLevelSelection": True,
    "worldMapId": "Eraden",
    "worldMapTravelAudioContainerAddress": "Bas.AudioGroup.Dungeon.Start",
    "mapLocationIndex": 1,
    "showOnMap": True,
    "hideOnAndroid": False,
    "mapLocationIconAddress": "Bas.Icon.Location.Arena",
    "mapLocationIconHoverAddress": "Bas.Icon.Location.Arena_Highlight",
    "mapPreviewImageAddress": "Bas.Image.Preview.Arena",
    "modes": modes,
    "_zelda": {"campaign": "Blade of Hyrule", "dungeons": dungeon_names}
}

fn = AV / "Level_ZeldaCampaign.json"
fn.write_text(json.dumps(level, indent=1))
print(f"Wrote {fn}")
print("Zelda Campaign is now a selectable 'Zelda Campaign' level (group) — 9 dungeon wave modes on Cell Games arena.")
print("No Unity needed — reuses the deployed Cell Games scene + WaveAssault/ Survival game modes.")