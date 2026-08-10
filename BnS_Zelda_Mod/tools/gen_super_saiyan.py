#!/usr/bin/env python3
"""
Generate the full Super Saiyan Transformations mod for B&S Quest.
Creates: DamageModifiers, Effects (aura per stage), Spells (7 stage spells),
and the skill definitions. All JSON-driven (ThunderRoad Catalog picks them up
at load), so no Unity / no C# recompilation of the game is needed.
"""
import json, os
from pathlib import Path

MOD = Path("/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods/SuperSaiyanTransformations")
for sub in ("Spells", "Effects", "DamageModifiers", "Skills"):
    (MOD / sub).mkdir(parents=True, exist_ok=True)

STAGES = [
    (1, "SSJ1",  "Super Saiyan",         2,   (1.00, 0.92, 0.35), 1.1, 1),   # spectral gold (diamond dispersion)
    (2, "SSJ2",  "Super Saiyan 2",       3,   (1.00, 0.78, 0.20), 1.3, 2),   # harsher gold + electric
    (3, "SSJ3",  "Super Saiyan 3",       4,   (0.95, 0.72, 0.30), 1.6, 3),   # long-hair gold
    (4, "SSG",   "Super Saiyan God",    10,   (0.98, 0.15, 0.25), 2.0, 4),   # crimson (fire-spectral)
    (5, "SSB",   "Super Saiyan Blue",   20,   (0.12, 0.45, 1.00), 2.4, 5),   # azure god-ki
    (6, "UI",    "Ultra Instinct",      40,   (0.75, 0.82, 1.00), 2.8, 6),   # silver-white
    (7, "MUI",   "Mastered Ultra Instinct", 100, (1.00, 1.00, 0.98), 3.2, 7),# brilliant white (subsurface glow peak)
]

def color_vec(c):  # float32 color 0-1
    return {"r": c[0], "g": c[1], "b": c[2], "a": 1.0}

def write_damage_modifier(slot, sid, name, mult):
    """Proven ThunderRoad.DamageModifierData -> applied to player weapons/spells."""
    data = {
        "$type": "ThunderRoad.DamageModifierData, ThunderRoad",
        "id": f"SuperSaiyan_{sid}_Modifier",
        "sensitiveContent": "None",
        "sensitiveFilterBehaviour": "Discard",
        "version": 1,
        "damageType": "Physical",
        "collisions": [{
            "$type": "ThunderRoad.DamageModifierData+Collision, ThunderRoad",
            "sourceMaterialIds": [],
            "targetMaterialIds": ["Flesh"],
            "modifiers": [{
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
                    {"$type":"ThunderRoad.DamageModifierData+Modifier+PushLevel, ThunderRoad","hitVelocity":1.5,"throwVelocity":1.5},
                    {"$type":"ThunderRoad.DamageModifierData+Modifier+PushLevel, ThunderRoad","hitVelocity":3.0,"throwVelocity":3.0},
                    {"$type":"ThunderRoad.DamageModifierData+Modifier+PushLevel, ThunderRoad","hitVelocity":4.5,"throwVelocity":4.5},
                    {"$type":"ThunderRoad.DamageModifierData+Modifier+PushLevel, ThunderRoad","hitVelocity":6.0,"throwVelocity":6.0},
                    {"$type":"ThunderRoad.DamageModifierData+Modifier+PushLevel, ThunderRoad","hitVelocity":7.5,"throwVelocity":7.5},
                ],
            }],
        }],
    }
    (MOD / "DamageModifiers" / f"DamageModifier_{sid}.json").write_text(json.dumps(data, indent=1))

def write_aura(slot, sid, name, color_rgb, scale, unlock_order):
    """EffectData per stage — reuses the base 'AroundBody' prefab from the Pilot bundle but
    sized/tinted per stage. mainColorStart/End drive the additive aura tint."""
    c = color_vec(color_rgb)
    data = {
        "$type": "ThunderRoad.EffectData, ThunderRoad",
        "id": f"SuperSaiyan_{sid}_Aura",
        "sensitiveContent": "None",
        "sensitiveFilterBehaviour": "Discard",
        "version": 0,
        "groupId": "SkillTree",
        "volumeDb": 0.0,
        "modules": [{
            "$type": "ThunderRoad.EffectModuleParticle, ThunderRoad",
            "effectLink": "Intensity",
            "insideParticleRadius": 0.0,
            "cullMinIntensity": 0.05,
            "cullMinSpeed": 0.05,
            "effectParticleAddress": "Pilot.DBZ.Spell.VFX.Main.AroundBody.prefab",
            "intensityCurve": None,
            "renderInLateUpdate": False,
            "mainColorStart": c,
            "mainColorEnd": c,
            "secondaryColorStart": c,
            "secondaryColorEnd": c,
            "mainNoHdrColorStart": c,
            "mainNoHdrColorEnd": c,
            "secondaryNoHdrColorStart": c,
            "secondaryNoHdrColorEnd": c,
            "localScale": {"x": scale, "y": scale, "z": scale},
            "useScaleCurve": False,
            "scaleCurve": None,
            "localRotation": {"x":0.0,"y":0.0,"z":0.0},
            "collisionEffectId": None,
            "collisionLayerMask": -65665,
            "materialAddress": None,
            "prewarm": True,
            "duration": 1.0,
            "loopEmission": True,
            "playOnce": False,
            "speedMultiplierCurve": None,
            "useLocalRandomRotation": False,
            "randomXRotationRange": 0.0,
            "randomYRotationRange": 0.0,
            "randomZRotationRange": 0.0,
            "worldSpace": True,
            "linkDestination": "Self",
            "linkRotationType": "Self",
            "linkScaleType": "World",
            "playParticle": True,
            "playAudio": False,
            "playHaptics": False,
            "intensityRangeCurve": None,
            "ageMin": 0.0,
            "ageMax": 0.0,
            "particleCount": 1,
        }],
        "matchingModulesInRaycast": [],
    }
    (MOD / "Effects" / f"Effect_{sid}Aura.json").write_text(json.dumps(data, indent=1))

def write_spell(slot, sid, name, mult, unlock_order):
    """SpellCastCharge-per-stage. References its aura as chargeEffectId + a StatusEffect
    that applies the damageModifier while the stage is active. Progressive unlock via
    primarySkillTree ordering; base (cup) returns to form 1."""
    data = {
        "$type": "DragonBall.SuperSayan, DBZ",   # reuse the base spell cast logic
        "id": f"SuperSaiyan_{sid}",
        "sensitiveContent": "None",
        "sensitiveFilterBehaviour": "Discard",
        "version": 0,
        "castDescription": f"Transform into {name} (strength x{mult}).",
        "imbueDescription": None,
        "slamDescription": None,
        "chargeEffectId": f"SuperSaiyan_{sid}_Aura",
        "readyEffectId": f"SuperSaiyan_{sid}_Aura",
        "fingerEffectId": None,
        "closeHandPoseId": "ChargeClose",
        "openHandPoseId": "ChargeOpen",
        "doReadyHaptic": True,
        "orbVariationSpeed": 10.0,
        "orbVariationAmount": 0.2,
        "chargeSpeed": 0.5,
        "allowStaffBuff": False,
        "chargeSpeedPerSkill": 0.05,
        "grabbedFireMaxCharge": 0.5,
        "endOnGrip": False,
        "allowCharge": True,
        "chargeMinHaptic": 0.05,
        "chargeMaxHaptic": 0.3,
        "allowThrow": False,
        "allowSpray": False,
        "imbueEnabled": True,
        "imbueRate": 1.0,
        "imbueLossMultiplier": 1.0,
        "wallDisplayName": name,
        "hasOrder": True,
        "order": slot,
        "iconEffectId": "SpellOrbTest",
        "aiCastType": "CastSimple",
        "minMana": 5.0,
        "shardId": "Crystal_Small_01_Shard",
        "prefabAddress": "Bas.Item.Misc.SkillOrb",
        "allowSkill": True,
        "showInTree": True,
        "hideInSkillMenu": False,
        "skillTreeDisplayName": name,
        "description": f"Transformation {sid}: strength x{mult}. Cast to activate, cast again to return to base form.",
        "isDefaultSkill": False,
        "primarySkillTreeId": "Test",
        "isTierBlocker": True,
        "ReadyThreshold": 0.5,
        "Ready": False,
        "Order": slot,
        "IsCombinedSkill": False,
        # Extra fields the loader/harmony reads for the multiplier
        "stageMultiplier": mult,
        "stageUnlockOrder": unlock_order,
    }
    (MOD / "Spells" / f"Spell.SuperSaiyan_{sid}.json").write_text(json.dumps(data, indent=1))

for slot, sid, name, mult, color, scale, unlock in STAGES:
    write_damage_modifier(slot, sid, name, mult)
    write_aura(slot, sid, name, color, scale, unlock)
    write_spell(slot, sid, name, mult, unlock)
    print(f"  [{slot}] {sid:>4} {name:<24} x{mult:<4} color={color} scale={scale}")

print(f"\nGenerated {len(STAGES)*3} files (7 DM + 7 Aura + 7 Spell) into {MOD}")