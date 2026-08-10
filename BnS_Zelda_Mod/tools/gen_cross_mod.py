#!/usr/bin/env python3
"""
Cross-mod content generator (2026-08-08).

Adds FOUR cross-cutting features to each of OUR FOUR B&S Quest mods, purely via
IL2CPP JSON content (no Unity, no game recompile):

  (1) CROSS-MOD SPELLMERGE COMBO  - a native SpellMerge pairing one of our own
      spells with a library catalyst to produce a new synergy spell.
  (2) NEW KI/ENERGY ATTACK         - a themed pooled projectile ItemData +
      SpellCastCharge per mod.
  (3) LOOT SYNERGY                 - a themed Lithosphere drop per mod.
  (4) SHARED POWER-TIER MODIFIER   - a DamageModifierData boost layer per mod.

All $type names are exact ThunderRoad/DBZ/WaterSpell types proven in the library.
JSON-only mods must ship ZERO catalog.json/bundle — we never write one here.
"""
import json, os

ROOT = os.path.join(os.path.dirname(__file__), "..", "Mods")
MODS = {
    "SuperSaiyanTransformations": {
        "id": "SuperSaiyanTransformations",
        "projectile": "SuperSaiyan_Kamehameha",   # reuse proven moon bullet
        "aura": "SuperSaiyan_SSJ1_Aura",
        "own": "SuperSaiyan_SSJ1",
        "catalyst": "Water",
        "merge_result": "SuperSaiyan_SSJ2",
        "color": (1.0, 0.92, 0.35),   # golden
        "mat": "quartz",
    },
    "ZeldaCampaign": {
        "id": "ZeldaCampaign",
        "projectile": "SuperSaiyan_Kamehameha",
        "aura": "Effect_Loot_ZeldaCampaign_Aura",
        "own": "SuperSaiyan_SSG",      # hero ki
        "catalyst": "BlackFire",
        "merge_result": "SuperSaiyan_SSB",
        "color": (0.9, 0.1, 0.1),      # crimson (Triforce edge)
        "mat": "amber",
    },
    "SSJFlight": {
        "id": "SSJFlight",
        "projectile": "SuperSaiyan_Kamehameha",
        "aura": "Effect_SSJFlightAura",
        "own": "SuperSaiyan_SSJ1",
        "catalyst": "Water",
        "merge_result": "SuperSaiyan_SSJ2",
        "color": (0.45, 0.6, 1.0),     # sky blue
        "mat": "opal",
    },
    "LithosphereLootPack": {
        "id": "LithosphereLootPack",
        "projectile": None,            # this mod stays loot/aura focused
        "aura": "Effect_Loot_DBmap_Aura",
        "own": None,
        "color": (0.85, 0.9, 1.0),
        "mat": "diamond",
    },
}

# Proven library catalyst spell IDs (grep-confirmed from installed mods).
# SpellMerge left/right must resolve to REAL spell ids in the Catalog.
LIBRARY_CATALYSTS = ["Water", "Lightning", "BlackFire", "Gravity"]

# Aim the merge couplets so neither side is itself a merge-result (avoid recursion
# where two merges fight). Each mod's intersection spell must be a REAL base cast.
MERGE_COUPLETS = {
    "SuperSaiyanTransformations": ("SuperSaiyan_SSJ1", "Water"),
    "ZeldaCampaign":              ("SuperSaiyan_SSG", "BlackFire"),
    "SSJFlight":                  ("SuperSaiyan_SSJ1", "Water"),
}


def clamp(v): return max(0.0, min(1.0, v))


def rgba(rgb, a=1.0):
    r, g, b = rgb
    return {"r": r, "g": g, "b": b, "a": a}


def kill_curve():
    return {
        "$type": "UnityEngine.AnimationCurve, UnityEngine.CoreModule",
        "keys": [
            {"$type": "UnityEngine.Keyframe, UnityEngine.CoreModule",
             "time": 0.0, "value": 0.0, "inTangent": 0.0, "outTangent": 0.0,
             "inWeight": 0.0, "outWeight": 0.0, "weightedMode": "None",
             "tangentMode": 0},
            {"$type": "UnityEngine.Keyframe, UnityEngine.CoreModule",
             "time": 1.0, "value": 1.0, "inTangent": 0.0, "outTangent": 0.0,
             "inWeight": 0.0, "outWeight": 0.0, "weightedMode": "None",
             "tangentMode": 0},
        ],
        "length": 2, "preWrapMode": "ClampForever", "postWrapMode": "ClampForever",
    }


# ---------------------------------------------------------------------------
# (1) CROSS-MOD SPELLMERGE COMBO
#     A merge that pairs our own castable with a library catalyst to yield a
#     synergy spell. $type = the game's native SpellMergeFire (same as BlackFire).
# ---------------------------------------------------------------------------
def gen_spell_merge(mod, key):
    left, right = MERGE_COUPLETS[key]
    result = MODS[key]["merge_result"]
    return {
        "$type": "ThunderRoad.Skill.SpellMerge.SpellMergeFire, ThunderRoad",
        "id": f"{key}_CrossMerge",
        "sensitiveContent": "None",
        "sensitiveFilterBehaviour": "Discard",
        "version": 0,
        "leftSpellId": left,
        "rightSpellId": right,
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
        "hapticIntensityCurve": kill_curve(),
        "requireSkill": "SuperSaiyan",
        "resultSpellId": result,
        "description": f"Cross-mod synergy: {left} + {right} -> {result}.",
        "_nssp_cross": True,
        "_nssp_result": result,
    }


# ---------------------------------------------------------------------------
# (2) NEW KI/ENERGY ATTACK SPELL PER MOD (except Lithosphere, loot-focused)
#     A themed pooled projectile + a SpellCastCharge that throws it.
# ---------------------------------------------------------------------------
def gen_energy_item(mod, key, idx):
    rgb = MODS[key]["color"]
    item_id = f"{key}_EnergyBlast_{idx}"
    return {
        "$type": "ThunderRoad.ItemData, ThunderRoad",
        "id": item_id,
        "sensitiveContent": "None",
        "sensitiveFilterBehaviour": "Discard",
        "version": 4,
        "displayName": f"{key.replace('Transformations','')} Energy Blast",
        "author": "Lilith",
        "valueType": "Gold",
        "value": 0.0,
        "rewardValue": 0.0,
        "tier": 3,
        "flags": 0,
        "levelRequired": 0,
        "category": "Misc",
        "iconEffectId": None,
        "preferredItemCenter": "Mass",
        "drainImbueWhenIdle": True,
        "prefabAddress": "Bas.Item.Misc.ProjectileMeteor",
        "iconAddress": None,
        "pooledCount": 48,
        "androidPooledCount": 24,
        "type": "Misc",
        "allowedStorage": 0,
        "despawnOnStoredInInventory": False,
        "isStackable": False,
        "consumableId": None,
        "inventoryAudioContainerAddress": None,
        "slot": None,
        "overrideMassAndDrag": True,
        "mass": 1.4,
        "drag": 1.0,
        "angularDrag": 0.05,
        "damagers": [
            {"$type": "ThunderRoad.ItemData+Damager, ThunderRoad",
             "transformName": "Damager", "damagerID": "SwordSharp1H"}
        ],
        "_nssp_note": f"Cross-mod energy blast ({key}), color {rgb}",
        "_nssp_aura": MODS[key]["aura"],
    }


def gen_energy_spell(mod, key, idx):
    item_id = f"{key}_EnergyBlast_{idx}"
    rgb = MODS[key]["color"]
    return {
        "$type": "DragonBall.SuperSayan, DBZ",
        "id": item_id,
        "sensitiveContent": "None",
        "sensitiveFilterBehaviour": "Discard",
        "version": 0,
        "castDescription": f"{key} energy blast - charge and release to fire.",
        "imbueDescription": None,
        "chargeEffectId": MODS[key]["aura"],
        "readyEffectId": MODS[key]["aura"],
        "closeHandPoseId": "ChargeClose",
        "openHandPoseId": "ChargeOpen",
        "doReadyHaptic": True,
        "orbVariationSpeed": 10.0,
        "orbVariationAmount": 0.2,
        "chargeSpeed": 0.6,
        "allowStaffBuff": False,
        "endOnGrip": False,
        "allowCharge": True,
        "chargeMinHaptic": 0.05,
        "chargeMaxHaptic": 0.3,
        "allowThrow": True,
        "throwEffectId": MODS[key]["aura"],
        "throwMinCharge": 0.5,
        "allowSpray": False,
        "imbueEnabled": True,
        "imbueRate": 1.0,
        "wallDisplayName": f"{key} Energy Blast",
        "hasOrder": True,
        "order": 20,
        "iconEffectId": "SpellOrbTest",
        "aiCastType": "CastSimple",
        "minMana": 12.0,
        "shardId": "Crystal_Small_01_Shard",
        "prefabAddress": "Bas.Item.Misc.SkillOrb",
        "allowSkill": True,
        "showInTree": True,
        "hideInSkillMenu": False,
        "skillTreeDisplayName": f"{key} Energy Blast",
        "description": "Charge both hands, release to fire a themed energy blast.",
        "isDefaultSkill": False,
        "primarySkillTreeId": "Gravity",
        "isTierBlocker": False,
        "ReadyThreshold": 0.5,
        "Ready": False,
        "Order": 20,
        "IsCombinedSkill": False,
        "nssp": {
            "projectileId": item_id,
            "spellKind": "EnergyBlast",
            "color": rgb,
        },
    }


# ---------------------------------------------------------------------------
# (3) LOOT SYNERGY - extend Lithosphere with a themed drop item per mod
# ---------------------------------------------------------------------------
def gen_loot_item(key, rgb, mat):
    item_id = f"Lithosphere_Synergy_{key}"
    return {
        "$type": "ThunderRoad.ItemData",
        "id": item_id,
        "sensitiveContent": "None",
        "version": 1,
        "name": f"Lithosphere Synergy ({key})",
        "category": "Misc",
        "itemType": "Prop",
        "description": f"A crystallized shard of synergistic power from the {key} stack.",
        "prefabAddress": None,
        "bundles": [],
        "addressableName": item_id,
        "contentAddress": None,
        "modules": [
            {
                "$type": "ThunderRoad.ItemModuleEffect",
                "effectId": f"Lithosphere_Synergy_{key}_Aura",
                "effectDuration": 0.0,
                "loop": True,
                "mainStart": rgba(rgb, 1.0),
                "mainEnd": rgba((rgb[0], rgb[1], rgb[2]), 1.0),
                "materialId": mat,
            }
        ],
        "drops": [],
        "damagers": [],
        "colliderGroup": "Blade",
        "dissolution": 0.2,
    }


def gen_loot_effect(key, rgb, mat):
    return {
        "$type": "ThunderRoad.EffectData",
        "id": f"Lithosphere_Synergy_{key}_Aura",
        "sensitiveContent": "None",
        "version": 1,
        "name": f"{key} Synergy ({mat})",
        "addressableName": f"Lithosphere_Synergy_{key}_Aura",
        "modules": [
            {
                "$type": "ThunderRoad.EffectModuleParticle, ThunderRoad",
                "loop": True,
                "duration": 0.0,
                "isStickToObject": True,
                "particleMaterial": "Additive",
                "mainGradient": {
                    "mainStart": rgba((rgb[0], rgb[1], rgb[2]), 0.9),
                    "mainEnd": rgba((min(1,rgb[0]+0.2), min(1,rgb[1]+0.2), min(1,rgb[2]+0.2)), 0.0),
                },
                "note": f"Lithosphere synergy effect: {mat}",
                "effectParticleAddress": "Pilot.DBZ.Spell.VFX.Main.AroundBody.prefab",
                "linkDestination": "Self",
                "linkRotationType": "Self",
                "linkScaleType": "World",
                "playParticle": True,
                "particleCount": 26,
                "localScale": {"x": 0.6, "y": 0.6, "z": 0.6},
            }
        ],
    }


# ---------------------------------------------------------------------------
# (4) SHARED POWER-TIER MODIFIER - a DamageModifierData boost layer per mod
# ---------------------------------------------------------------------------
def gen_modifier(key, mult):
    return {
        "$type": "ThunderRoad.DamageModifierData, ThunderRoad",
        "id": f"{key}_Booster_Modifier",
        "sensitiveContent": "None",
        "sensitiveFilterBehaviour": "Discard",
        "version": 1,
        "damageType": "Physical",
        "collisions": [
            {
                "$type": "ThunderRoad.DamageModifierData+Collision, ThunderRoad",
                "sourceMaterialIds": [],
                "targetMaterialIds": ["Flesh"],
                "modifiers": [
                    {
                        "$type": "ThunderRoad.DamageModifierData+Modifier, ThunderRoad",
                        "tierFilter": 0,
                        "imbuesFilterLogic": "NoneExcept",
                        "imbuesFilter": [],
                        "minVelocity": 0.0,
                        "damageMultiplier": mult,
                        "allowKnockout": True,
                        "allowPenetration": True,
                        "pressureAllowed": True,
                        "knockoutAllowedMinVelocity": "Infinity",
                        "knockoutForcedMinVelocity": "Infinity",
                        "knockoutThrowAllowedMinVelocity": "Infinity",
                        "knockoutThrowForcedMinVelocity": "Infinity",
                        "knockoutDurationMultiplier": 1.0,
                        "pushLevels": [
                            {"$type": "ThunderRoad.DamageModifierData+Modifier+PushLevel, ThunderRoad",
                             "hitVelocity": 2.0, "throwVelocity": 2.0},
                            {"$type": "ThunderRoad.DamageModifierData+Modifier+PushLevel, ThunderRoad",
                             "hitVelocity": 3.5, "throwVelocity": 3.5},
                            {"$type": "ThunderRoad.DamageModifierData+Modifier+PushLevel, ThunderRoad",
                             "hitVelocity": 5.0, "throwVelocity": 5.0},
                        ],
                    }
                ],
            }
        ],
    }


def main():
    written = 0
    for key, mod in MODS.items():
        moddir = os.path.join(ROOT, key)
        merges_dir = os.path.join(moddir, "SpellMerges")
        spells_dir = os.path.join(moddir, "Spells")
        items_dir = os.path.join(moddir, "Items")
        dmg_dir = os.path.join(moddir, "DamageModifiers")
        loot_dir = os.path.join(ROOT, "LithosphereLootPack", "Loot")
        eff_dir = os.path.join(ROOT, "LithosphereLootPack", "Effects")
        for d in (merges_dir, spells_dir, items_dir, dmg_dir, loot_dir, eff_dir):
            os.makedirs(d, exist_ok=True)

        # (1) Cross-mod SpellMerge
        if key in MERGE_COUPLETS:
            p = os.path.join(merges_dir, f"SpellMerge_{key}_Cross.json")
            with open(p, "w") as f:
                json.dump(gen_spell_merge(mod, key), f, indent=1)
            written += 1

        # (2) Energy attack (skip Lithosphere - loot-focused)
        idx = 1
        if mod["projectile"] is not None:
            ip = os.path.join(items_dir, f"Item_{key}_EnergyBlast_{idx}.json")
            sp = os.path.join(spells_dir, f"Spell_{key}_EnergyBlast_{idx}.json")
            with open(ip, "w") as f:
                json.dump(gen_energy_item(mod, key, idx), f, indent=1)
            with open(sp, "w") as f:
                json.dump(gen_energy_spell(mod, key, idx), f, indent=1)
            written += 2

        # (3) Loot synergy (into Lithosphere)
        if mod["mat"]:
            lp = os.path.join(loot_dir, f"Item_Lithosphere_Synergy_{key}.json")
            ep = os.path.join(eff_dir, f"Effect_Lithosphere_Synergy_{key}_Aura.json")
            with open(lp, "w") as f:
                json.dump(gen_loot_item(key, mod["color"], mod["mat"]), f, indent=1)
            with open(ep, "w") as f:
                json.dump(gen_loot_effect(key, mod["color"], mod["mat"]), f, indent=1)
            written += 2

        # (4) Power-tier modifier each mod
        mp = os.path.join(dmg_dir, f"DamageModifier_{key}_Booster.json")
        with open(mp, "w") as f:
            json.dump(gen_modifier(key, 3.0), f, indent=1)
        written += 1

    print(f"Cross-mod generator: wrote {written} JSON files across all 4 mods.")
    print("NO catalog.json/bundle emitted - JSON-only mods must ship none.")


if __name__ == "__main__":
    main()