#!/usr/bin/env python3
"""
Generate SSJ Flight — spell-merge + skill definitions that integrate flight into
the Super Saiyan transformations and the B&S spell-merge system.

Flight model (mirrors WaterSpell's SkillWaterJetpack decompiled logic):
    Player.local.locomotion.physicBody.AddForce(-jetDir*speed*dt, ForceMode.Impulse)
Gated on: player HasSkill + airborne. Our stages scale the thrust (see FlightProfile).

Produces:
  - Skills/Skill_SSJFlight.json        (the enabling skill, Gravity+Water hybrid tree)
  - Spells/Spell_SSJGraviMerge.json    (Gravity merge spell -> flight engage)
  - Spells/Spell_SSJBoost.json         (boost spell)
  - Effects/ ... referenced aura velocity trail
"""
import json
from pathlib import Path

MOD = Path("/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods/SSJFlight")
for sub in ("Skills", "Spells", "Effects", "Items"):
    (MOD / sub).mkdir(parents=True, exist_ok=True)

# 1. Flight enabling skill (matches SkillWaterJetpack structure + Gravity secondary tree)
skill = {
    "$type": "WaterSpell.SkillWaterJetpack, WaterSpell",   # reuse the proven flight class
    "id": "Skill_SSJFlight",
    "sensitiveContent": "None",
    "sensitiveFilterBehaviour": "Discard",
    "version": 0,
    "shardId": "Crystal_Small_01_Shard",
    "prefabAddress": "Bas.Item.Misc.SkillOrb",
    "meshAddress": None,
    "meshSize": 1.0,
    "orbLinkEffectId": "SkillTreeOrbLink",
    "tier": 1,
    "allowSkill": True,
    "forceAllowRefund": False,
    "showInTree": True,
    "hideInSkillMenu": False,
    "skillTreeDisplayName": "SSJ Flight",
    "description": "Super Saiyan flight. Hover with one hand, fly with two. Thrust scales with your transformation stage: SSJ1 glide -> MUI full-speed flight. Combines Gravity levitation with Water-jet propulsion.",
    "imageAddress": "",
    "videoAddress": "",
    "buttonSpriteSheetAddress": "Bas.Ui.SkillTree.Icons",
    "buttonEnabledIconAddress": "Bas.Ui.SkillTree.Icons[Gravity_ButtonColor]",
    "buttonDisabledIconAddress": "Bas.Ui.SkillTree.Icons[Gravity_Button]",
    "orbIconAddress": "SSJFlightIcon",
    "tutorial": None,
    "costOverride": -1,
    "isDefaultSkill": True,
    "primarySkillTreeId": "Gravity",
    "secondarySkillTreeId": "Water",
    "isTierBlocker": False,
    "canSpawnAsReward": True,
    "allowInRouletteMode": True,
    "groupPath": None,
    "IsCombinedSkill": True,
    "classUnique": True
}
(MOD / "Skills" / "Skill_SSJFlight.json").write_text(json.dumps(skill, indent=1))

# 2. Gravity merge spell (flight engage) — merges Gravity+SSJ to activate flight
merge = {
    "$type": "ThunderRoad.SpellMergeData, ThunderRoad",
    "id": "Spell_SSJGraviMerge",
    "sensitiveContent": "None",
    "sensitiveFilterBehaviour": "Discard",
    "version": 0,
    "leftSpellId": "Gravity",
    "rightSpellId": "Base",
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
    "requireSkill": "Skill_SSJFlight",
    "spawnEffectId": "SSJFlightAura",
    "description": "Merge Gravity + base form to engage Super Saiyan flight.",
}
(MOD / "Spells" / "Spell_SSJGraviMerge.json").write_text(json.dumps(merge, indent=1))

# 3. Boost spell (dash forward)
boost = {
    "$type": "SpellCastCharge, ThunderRoad",
    "id": "Spell_SSJBoost",
    "sensitiveContent": "None",
    "sensitiveFilterBehaviour": "Discard",
    "version": 0,
    "shardId": "Crystal_Small_01_Shard",
    "prefabAddress": "Bas.Item.Misc.SkillOrb",
    "orbLinkEffectId": "SkillTreeOrbLink",
    "chargeEffectId": "SSJFlightAura",
    "allowCharge": True,
    "chargeSpeed": 0.5,
    "description": "Super Saiyan boost dash — propel forward with a burst of ki.",
    "skillTreeDisplayName": "SSJ Boost",
    "allowSkill": True,
    "hideInSkillMenu": False,
    "primarySkillTreeId": "Gravity",
    "minMana": 10.0,
}
(MOD / "Spells" / "Spell_SSJBoost.json").write_text(json.dumps(boost, indent=1))

# 4. Aura/trail effect (velocity trail during flight)
aura = {
    "$type": "ThunderRoad.EffectData, ThunderRoad",
    "id": "SSJFlightAura",
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
        "renderInLateUpdate": False,
        "mainColorStart": {"r":0.6,"g":0.72,"b":1.0,"a":1.0},
        "mainColorEnd": {"r":0.6,"g":0.72,"b":1.0,"a":1.0},
        "localScale": {"x":1.0,"y":1.0,"z":1.0},
        "useScaleCurve": False,
        "worldSpace": True,
        "playParticle": True,
        "playAudio": False,
        "playHaptics": False,
        "prewarm": True,
        "duration": 1.0,
        "loopEmission": True,
        "playOnce": False,
    }],
    "matchingModulesInRaycast": [],
}
(MOD / "Effects" / "Effect_SSJFlightAura.json").write_text(json.dumps(aura, indent=1))

print(f"SSJ Flight generated: {len(list((MOD/'Skills').glob('*')))+len(list((MOD/'Spells').glob('*')))+len(list((MOD/'Effects').glob('*')))} files into {MOD}")

# 5. manifest + id.modio + README
(MOD / "manifest.json").write_text(json.dumps({
    "Name": "SSJ Flight", "Description": "Super Saiyan flight — hover/fly/boost, thrust scales with transformation stage. Requires WaterSpell (jetpack) + SuperSaiyanTransformations.",
    "Author": "Lilith / Baal-TehDriverman", "ModVersion": "1.0.0", "GameVersion": "1.3.1", "Thumbnail": ""
}, indent=1))
(MOD / "id.modio").write_text(json.dumps({"id": 6000123, "lastChecked": "2026-08-08T15:00:00.000Z", "dependencies": []}, indent=1))
print("Wrote manifest + id.modio")