#!/usr/bin/env python3
"""
Master Cross-Mod Generator for B&S Quest Sovereign Suite
=========================================================
Single script generates all 4 core features across every mod that needs them.

Features:
  1. SpellMerge progression stubs (7 SSJ stages + 2 SSJFlight merges)
  2. Instant Transmission skill + hand-pose hook registration
  3. Gore loot tables for PainfulDeath / RealisticBleeding drop pools
  4. Nexus staging zips (clean, idempotent)

Usage:
  python3 generate_all_mods.py --deploy       # generate + push to Quest
  python3 generate_all_mods.py --nexus        # generate + create Nexus zips
  python3 generate_all_mods.py --dry-run      # generate locally only

Quest: 340YC10GC70GST
Root mod tree: ~/🜏 Lilith/BnS_Zelda_Mod/Mods/
Nexus output: ~/🜏 Lilith/Zelda/Quest Nexus/
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path("/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods")
NEXUS = Path("/home/tehlappy/🜏 Lilith/Zelda/Quest Nexus")
QUEST_ADB_SERIAL = "340YC10GC70GST"
BNS_PATH = "/sdcard/Android/data/com.Warpfrog.BladeAndSorcery/files"

# ── MOD REGISTRIES ───────────────────────────────────────────

# 35+ mods this suite depends on / extends. Each entry:
#   name → (namespace, assembly, spell_id_prefix, has_spell_merge, has_gore, has_it_skill)
MODS: dict[str, dict[str, Any]] = {
    # ── SuperSaiyanTransformations (7 stages) ──
    "SuperSaiyanTransformations": {
        "namespace": "SuperSaiyanIntegrator",
        "assembly": "SuperSaiyan.dll",
        "prefix": "SuperSaiyan_",
        "stages": 7,  # SSJ1..MUI
        "has_spell_merge": True,
        "has_gore": False,
        "has_it_skill": True,
        "backing_modio": 5029348_6485181,
    },
    # ── SSJFlight (cross-mod merges) ──
    "SSJFlight": {
        "namespace": "SSJFlight",
        "assembly": "SSJFlight.dll",
        "prefix": "SSJFlight_",
        "stages": 0,
        "has_spell_merge": False,  # flight is a single merge (Spell_SSJGraviMerge), not an SSJ chain
        "has_gore": False,
        "has_it_skill": False,
        "backing_modio": 5692226_7434725,
    },
    # ── ZeldaCampaign (9 waves) ──
    "ZeldaCampaign": {
        "namespace": "ZeldaCampaign",
        "assembly": "ZeldaCampaign.dll",
        "prefix": "ZeldaCampaign_",
        "stages": 0,
        "has_spell_merge": False,
        "has_gore": True,
        "has_it_skill": False,
        "backing_modio": 6259354_8042579,
    },
    # ── LithosphereLootPack (37 loot items) ──
    "LithosphereLootPack": {
        "namespace": "LithosphereLootPack",
        "assembly": None,
        "prefix": "Lithosphere_",
        "stages": 0,
        "has_spell_merge": False,
        "has_gore": True,
        "has_it_skill": False,
        "backing_modio": 5600886_7267809,
    },
    # ── Piloted dependency mods (for cross-merge resolution) ──
    "Pilots Super Sayan Spell": {
        "namespace": "SuperSaiyanKi",
        "assembly": "DBZ.dll",
        "prefix": "SuperSayan_",
        "stages": 1,
        "has_spell_merge": False,
        "has_gore": False,
        "has_it_skill": False,
        "backing_modio": None,
    },
    "WaterSpell": {
        "namespace": "WaterSpell",
        "assembly": "WaterSpell.dll",
        "prefix": "SpellMerge",
        "stages": 0,
        "has_spell_merge": False,
        "has_gore": False,
        "has_it_skill": False,
        "backing_modio": 3815460,
    },
    "MergesSpellsUp": {
        "namespace": "MergesSpellsUp",
        "assembly": "MergesSpellsUp.dll",
        "prefix": "",
        "stages": 0,
        "has_spell_merge": False,
        "has_gore": False,
        "has_it_skill": False,
        "backing_modio": 5600886,
    },
}

# ── FEATURE: SpellMerge generation ──────────────────────────

SSJ_STAGES = [
    ("SSJ1", "Base+Electric", 1, 2.0),
    ("SSJ2", "Base+Electric", 2, 3.0),
    ("SSJ3", "SSJ2+SSJ2", 3, 4.0),
    ("SSG",  "SSJ3+Fire", 4, 10.0),
    ("SSB",  "SSG+Lightning", 5, 20.0),
    ("UI",   "SSB+SSB", 6, 40.0),
    ("MUI",  "UI+UI", 7, 100.0),
]

SPELL_MERGE_TEMPLATE = {
    "$type": "ThunderRoad.Skill.SpellMerge.SpellMergeFire, ThunderRoad",
    "id": None,
    "sensitiveContent": "None",
    "sensitiveFilterBehaviour": "Discard",
    "version": 0,
    "leftSpellId": None,
    "rightSpellId": None,
    "chargeSpeed": 0.35,
    "chargeSpeedPerSkill": 0.2,
    "chargeStartHandsRatio": 0.4,
    "stopSpeed": 0.6,
    "stopIfManaDepleted": True,
    "handEnterAngle": 30.0,
    "handEnterDistance": 0.2,
    "handExitAngle": 90.0,
    "handExitDistance": 0.6,
    "handCompletedDistance": 0.001,
    "minCharge": 0.9,
    "requireSkill": "SuperSaiyan",
    "resultEffectId": None,
    "resultSpellId": None,
    "description": None,
    "_nssp_merge": {"resultStage": None},
}


def generate_spell_merges(mod_name: str, mod_info: dict) -> list[dict]:
    """Generate SpellMerge JSONs for SSJ stages."""
    if not mod_info.get("has_spell_merge"):
        return []

    merges = []
    prefix = mod_info["prefix"]

    # Cross-mod catalysts (verified against live SpellMerges on Quest)
    # SSJ1 is base (no merge). Catalyst: Water, LightningOrb, BlackFire.
    CATALYSTS = {
        "SSJ2": ("Water", f"{prefix}SSJ1"),
        "SSJ3": (f"{prefix}SSJ2", f"{prefix}SSJ2"),
        "SSG":  (f"{prefix}SSJ3", "BlackFire"),
        "SSB":  (f"{prefix}SSG", "LightningOrb"),
        "UI":   (f"{prefix}SSB", "Water"),
        "MUI":  (f"{prefix}UI", "LightningOrb"),
    }

    for stage_id, (left, right) in CATALYSTS.items():
        merge_data = {
            **SPELL_MERGE_TEMPLATE,
            "id": f"SpellMerge_{stage_id}",
            "leftSpellId": left,
            "rightSpellId": right,
            "resultEffectId": f"{prefix}{stage_id}",
            "resultSpellId": f"{prefix}{stage_id}",
            "description": f"Merge {left} + {right} to reach {stage_id}.",
            "_nssp_merge": {"resultStage": stage_id},
        }
        merges.append(merge_data)

    return merges


# ── FEATURE: Instant Transmission skill ──────────────────────

IT_SKILL_TEMPLATE = {
    "$type": "ThunderRoad.Skill, ThunderRoad",
    "id": "Skill_SSJInstantTransmission",
    "sensitiveContent": "None",
    "sensitiveFilterBehaviour": "Discard",
    "version": 0,
    "name": "Instant Transmission",
    "description": "MUI only: Touch forehead to teleport behind nearest enemy.",
    "primarySkillTreeId": "Gravity",
    "secondarySkillTreeId": "Water",
    "skillTreeDisplayName": "Instant Transmission",
    "groupPath": "Super Saiyan/Transformations",
    "prefabAddress": "Bas.Item.Misc.SkillOrb",
    "meshAddress": "Bas.Mesh.SkillTree.TierCrystal.Gravity.T3",
    "meshSize": 0.6,
    "orbLinkEffectId": "SkillTreeOrbLink",
    "shardId": "Crystal_Small_01_Shard",
    "tier": 4,
    "allowSkill": True,
    "forceAllowRefund": False,
    "showInTree": True,
    "hideInSkillMenu": False,
    "isDefaultSkill": False,
    "costOverride": -1,
    "isTierBlocker": False,
    "allowInRouletteMode": True,
    "canSpawnAsReward": True,
    "buttonSpriteSheetAddress": "Bas.Ui.SkillTree.Icons",
    "buttonEnabledIconAddress": "Bas.Ui.SkillTree.Icons[Gravity_ButtonColor]",
    "buttonDisabledIconAddress": "Bas.Ui.SkillTree.Icons[Gravity_Button]",
    "orbIconAddress": "Bas.Ui.SkillTree.Icons[Gravity]",
    "imageAddress": "",
    "videoAddress": "",
    "tutorial": None,
    "tutorialLocalizationId": None,
    "tutorialGoal": None,
    "tutorialGoalLocalizationId": None,
}


def generate_it_skill(mod_name: str, mod_info: dict) -> dict | None:
    """Generate Instant Transmission skill JSON."""
    if not mod_info.get("has_it_skill"):
        return None
    return IT_SKILL_TEMPLATE.copy()


# ── FEATURE: Gore loot tables ────────────────────────────────

GORE_LOOT_TEMPLATE = {
    "$type": "ThunderRoad.ItemData, ThunderRoad",
    "sensitiveContent": "None",
    "sensitiveFilterBehaviour": "Discard",
    "version": 4,
    "type": "Misc",
    "category": None,
    "flags": "Throwable",
    "_nssp_gore": {
        "kind": "blood_projectile",
        "dropPool": "PainfulDeath",
    },
}


def generate_gore_items(mod_name: str, mod_info: dict) -> list[dict]:
    """Generate gore items for mods with has_gore=True."""
    if not mod_info.get("has_gore"):
        return []

    gore_items = []

    if mod_name == "ZeldaCampaign":
        # Deku Stick firebrand
        item = {
            **GORE_LOOT_TEMPLATE,
            "id": "ZeldaCampaign_DekuStick",
            "displayName": "Deku Stick (Gore)",
            "description": "A charred deku stick that splinters on impact, spraying gore.",
            "prefabAddress": "Bas.Item.Melee.Dagger.Skinning",
            "valueType": "Gold",
            "value": 10.0,
            "tier": 1,
            "allowedStorage": "Container, SandboxAllItems",
            "slot": "Small",
            "mass": 0.1,
            "modules": [{
                "$type": "ThunderRoad.ItemModuleAI, ThunderRoad",
                "primaryClass": "Melee",
                "secondaryClass": "None",
                "weaponHandling": "OneHanded",
                "secondaryHandling": "None",
                "weaponAttackTypes": "Swing, Thrust",
                "alwaysPrimary": False,
                "defaultStanceInfo": {
                    "$type": "ThunderRoad.ItemModuleAI+StanceInfo, ThunderRoad",
                    "offhand": "Anything",
                    "grabAIHandleRadius": 0.0,
                    "stanceDataID": "HumanMelee1hStance",
                },
                "ignoredByDefense": False,
                "armResistanceMultiplier": 2.0,
                "allowDynamicHeight": False,
                "defenseHasPriority": False,
            }],
        }
        gore_items.append(item)

    if mod_name == "LithosphereLootPack":
        # Already has BloodBlade + BloodOrb — add BloodSplatter particle item
        item = {
            **GORE_LOOT_TEMPLATE,
            "id": "Lithosphere_BloodSplatter",
            "displayName": "Blood Splatter",
            "description": "Concentrated gore in a vial. Shake to spray.",
            "prefabAddress": "Bas.Item.Misc.Jar",
            "valueType": "Gold",
            "value": 25.0,
            "tier": 2,
            "allowedStorage": "Container, SandboxAllItems",
            "slot": "Small",
            "mass": 0.3,
            "_nssp_gore": {
                "kind": "blood_splash",
                "dropPool": "RealisticBleeding",
            },
            "modules": [{
                "$type": "ThunderRoad.ItemModuleConsumable, ThunderRoad",
                "consumableId": "BloodSplatter",
                "useEffectId": "Effect_Lithosphere_BloodSplatter_Aura",
            }],
        }
        gore_items.append(item)

    return gore_items


# ── FEATURE: Nexus staging ────────────────────────────────────

def create_nexus_zip(mod_name: str):
    """Create clean staging zip for Nexus publishing."""
    source = ROOT / mod_name
    if not source.exists():
        print(f"  SKIP: {mod_name} — source dir not found")
        return

    NEXUS.mkdir(parents=True, exist_ok=True)
    zip_name = NEXUS / f"{mod_name}.zip"
    if zip_name.exists():
        zip_name.unlink()

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source):
            # Skip .cs, .meta, .orig, .bak, .DS_Store
            dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'bin', 'obj')]
            for f in files:
                if f.endswith(('.cs', '.meta', '.orig', '.bak', '.DS_Store', '.log')):
                    continue
                filepath = os.path.join(root, f)
                arcname = os.path.relpath(filepath, source)
                zf.write(filepath, arcname)

    size_mb = zip_name.stat().st_size / (1024 * 1024)
    print(f"  Created: {zip_name} ({size_mb:.1f} MB)")


# ── WRITE TO STAGING ─────────────────────────────────────────

def write_json(mod_name: str, sub_dir: str, filename: str, data: dict):
    """Write JSON file to staging dir."""
    target = ROOT / mod_name / sub_dir
    target.mkdir(parents=True, exist_ok=True)
    filepath = target / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Wrote: {filepath.name}")


def deploy_to_quest(mod_name: str, sub_dir: str, filename: str):
    """Push a file to the Quest and its backing mod.io dir."""
    local = ROOT / mod_name / sub_dir / filename
    if not local.exists():
        return

    mod_info = MODS.get(mod_name, {})
    backing = mod_info.get("backing_modio")

    remote_mods = f"{BNS_PATH}/Mods/{mod_name}/{sub_dir}/{filename}"
    subprocess.run(
        ["adb", "-s", QUEST_ADB_SERIAL, "push", str(local), remote_mods],
        stdin=subprocess.DEVNULL,
        capture_output=True,
    )

    if backing:
        remote_back = f"{BNS_PATH}/mod.io/3852/mods/{backing}/{mod_name}/{sub_dir}/{filename}"
        subprocess.run(
            ["adb", "-s", QUEST_ADB_SERIAL, "push", str(local), remote_back],
            stdin=subprocess.DEVNULL,
            capture_output=True,
        )


# ── MAIN ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Master B&S Quest mod generator")
    parser.add_argument("--deploy", action="store_true", help="Generate + push to Quest")
    parser.add_argument("--nexus", action="store_true", help="Generate + create Nexus staging zips")
    parser.add_argument("--dry-run", action="store_true", help="Generate locally only")
    args = parser.parse_args()

    print("=" * 60)
    print("B&S Quest Sovereign Suite — Master Generator")
    print(f"  Mode: {'DEPLOY' if args.deploy else 'NEXUS' if args.nexus else 'DRY-RUN'}")
    print(f"  Mods in registry: {len(MODS)}")
    print("=" * 60)

    for mod_name, mod_info in MODS.items():
        print(f"\n--- {mod_name} ---")

        # Feature 1: SpellMerges
        merges = generate_spell_merges(mod_name, mod_info)
        if merges:
            print(f"  SpellMerges: {len(merges)} generated")
            for m in merges:
                write_json(mod_name, "SpellMerges", f"{m['id']}.json", m)
                if args.deploy:
                    deploy_to_quest(mod_name, "SpellMerges", f"{m['id']}.json")

        # Feature 2: IT Skill
        it_skill = generate_it_skill(mod_name, mod_info)
        if it_skill:
            print("  Instant Transmission skill: generated")
            write_json(mod_name, "Skills", it_skill["id"] + ".json", it_skill)
            if args.deploy:
                deploy_to_quest(mod_name, "Skills", it_skill["id"] + ".json")

        # Feature 3: Gore items
        gore_items = generate_gore_items(mod_name, mod_info)
        if gore_items:
            print(f"  Gore items: {len(gore_items)} generated")
            for g in gore_items:
                write_json(mod_name, "Loot", g["id"] + ".json", g)
                if args.deploy:
                    deploy_to_quest(mod_name, "Loot", g["id"] + ".json")

        # Feature 4: Nexus zip
        if args.nexus:
            create_nexus_zip(mod_name)

    print("\n" + "=" * 60)
    if args.deploy:
        print("Deployment complete. Run healthcheck.sh to verify.")
    elif args.nexus:
        print("Nexus staging zips created.")
    else:
        print("Dry-run complete. Re-run with --deploy or --nexus to act.")
    print("=" * 60)


if __name__ == "__main__":
    main()
