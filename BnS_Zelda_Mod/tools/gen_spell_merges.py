#!/usr/bin/env python3
"""
Generate the native SpellMerge layer for Super Saiyan Transformations.

Wires SSJ stage transitions into B&S's THUNDERROAD SpellMerge system — the same
mechanism BlackFire (SpellMergeFire) and WaterSpell (SpellMergeLightningOrb) use.
Each merge JSON defines leftSpellId + rightSpellId (the two spells being combined)
and produces the target transformation.

Verified cross-mod spell IDs:
  BlackFire  -> spell id "BlackFire", merge `ThunderRoad.Skill.SpellMerge.SpellMergeFire`
  WaterSpell -> spell id "Water", merge produces "SpellMergeLightningOrb"
  Our SSJ    -> "SuperSaiyan_SSJ1" .. "SuperSaiyan_MUI"
"""
import json
from pathlib import Path

MOD = Path("/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods/SuperSaiyanTransformations/SpellMerges")
MOD.mkdir(parents=True, exist_ok=True)

def merge_json(merge_type, mid, left, right, result_effect, desc,
               charge_speed=0.35, kill=True, meteor_item=None, meteor_id=None):
    d = {
        "$type": merge_type,
        "id": mid,
        "sensitiveContent": "None",
        "sensitiveFilterBehaviour": "Discard",
        "version": 0,
        "leftSpellId": left,
        "rightSpellId": right,
        "chargeSpeed": charge_speed,
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
        "hapticIntensityCurve": {
            "$type": "UnityEngine.AnimationCurve, UnityEngine.CoreModule",
            "keys": [
                {"$type":"UnityEngine.Keyframe, UnityEngine.CoreModule","time":0.0,"value":0.0,"inTangent":0.0,"outTangent":0.0,"inWeight":0.0,"outWeight":0.0,"weightedMode":"None","tangentMode":0},
                {"$type":"UnityEngine.Keyframe, UnityEngine.CoreModule","time":1.0,"value":1.0,"inTangent":0.0,"outTangent":0.0,"inWeight":0.0,"outWeight":0.0,"weightedMode":"None","tangentMode":0}
            ],
            "length": 2, "preWrapMode": "ClampForever", "postWrapMode": "ClampForever"
        },
        "requireSkill": "SuperSaiyan",
        "resultEffectId": result_effect,
        "resultSpellId": result_effect,
        "description": desc,
    }
    if meteor_item:  # for SpellMergeFire-style (meteor)
        d["meteorItemId"] = meteor_item
    if meteor_id:
        d["meteorId"] = meteor_id
    # nssp hint for the integrator
    d["_nssp_merge"] = {"resultStage": result_effect.replace("SuperSaiyan_","") if result_effect else None}
    return d

# ---- The 6 combos, using REAL cross-mod spell IDs ----

# 1. Base(electric/water) + SSJ -> SSJ2  (electric hand = WaterSpell's LightningOrb spell)
combos = [
    # (merge_type, id, left, right, result_effect, desc)
    (
        "ThunderRoad.Skill.SpellMerge.SpellMergeFire, ThunderRoad",
        "SpellMerge_SSJ2",
        "Water",            # WaterSpell's base water spell (electric hand lineage)
        "SuperSaiyan_SSJ1", # our base form
        "SuperSaiyan_SSJ2",
        "Merge Water + base SSJ to reach Super Saiyan 2.",
    ),
    (
        "ThunderRoad.Skill.SpellMerge.SpellMergeFire, ThunderRoad",
        "SpellMerge_SSJ3",
        "SuperSaiyan_SSJ2",
        "SuperSaiyan_SSJ2",
        "SuperSaiyan_SSJ3",
        "Merge two SSJ2 to reach Super Saiyan 3.",
    ),
    (
        "ThunderRoad.Skill.SpellMerge.SpellMergeFire, ThunderRoad",
        "SpellMerge_SSG",
        "SuperSaiyan_SSJ3",
        "BlackFire",       # BlackFire's fire spell -> ignite Saiyan God
        "SuperSaiyan_SSG",
        "Merge SSJ3 + BlackFire to ignite into Super Saiyan God.",
    ),
    (
        "ThunderRoad.Skill.SpellMerge.SpellMergeFire, ThunderRoad",
        "SpellMerge_SSB",
        "SuperSaiyan_SSG",
        "BlackFire",       # god ki + fire -> blue
        "SuperSaiyan_SSB",
        "Merge SSG + BlackFire to reach Super Saiyan Blue.",
    ),
    (
        "ThunderRoad.Skill.SpellMerge.SpellMergeFire, ThunderRoad",
        "SpellMerge_UI",
        "SuperSaiyan_SSB",
        "SuperSaiyan_SSB",
        "SuperSaiyan_UI",
        "Merge two SSB to reach Ultra Instinct.",
    ),
    (
        "ThunderRoad.Skill.SpellMerge.SpellMergeFire, ThunderRoad",
        "SpellMerge_MUI",
        "SuperSaiyan_UI",
        "SuperSaiyan_UI",
        "SuperSaiyan_MUI",
        "Merge two Ultra Instinct to reach Mastered Ultra Instinct.",
    ),
]

for merge_type, mid, left, right, result, desc in combos:
    data = merge_json(merge_type, mid, left, right, result, desc)
    fn = MOD / f"{mid}.json"
    fn.write_text(json.dumps(data, indent=1))
    print(f"  WROTE {fn.name}: {left} + {right} -> {result}")

print(f"\n{len(combos)} native SpellMerge JSONs written to {MOD}")
print("These load into B&S's Catalog alongside SpellMergeFire/SpellMergeLightningOrb.")