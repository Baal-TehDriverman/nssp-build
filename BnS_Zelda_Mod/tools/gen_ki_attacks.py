#!/usr/bin/env python3
"""
Generate the MUI Instant Transmission + Kamehameha + Big Bang Attack spells
for the Super Saiyan mod. Follows the DestructoDiscNomad precedent:
  - ItemData projectile (pooled, thrown) for the energy attacks
  - SpellCastCharge JSONs referencing those projectiles
  - The Instant Transmission teleport logic goes in SSJMod.dll (see build)
"""
import json
from pathlib import Path

MOD = Path("/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods/SuperSaiyanTransformations")
for sub in ("Spells", "Items", "Effects", "Skills"):
    (MOD / sub).mkdir(parents=True, exist_ok=True)

# ---------- ItemData projectiles (pooled, thrown energy attacks) ----------

def make_projectile(pid, display, prefab, damage, tier, mass=2.0):
    return {
        "$type": "ThunderRoad.ItemData, ThunderRoad",
        "id": pid,
        "sensitiveContent": "None",
        "sensitiveFilterBehaviour": "Discard",
        "version": 4,
        "localizationId": None,
        "displayName": display,
        "description": None,
        "author": "Lilith",
        "valueType": "Gold",
        "value": 0.0,
        "rewardValue": 0.0,
        "tier": tier,
        "flags": 0,
        "levelRequired": 0,
        "category": "Misc",
        "iconEffectId": None,
        "preferredItemCenter": "Mass",
        "drainImbueWhenIdle": True,
        "prefabAddress": prefab,
        "iconAddress": None,
        "pooledCount": 64,
        "androidPooledCount": 30,
        "type": "Misc",
        "allowedStorage": 0,
        "despawnOnStoredInInventory": False,
        "isStackable": False,
        "consumableId": None,
        "inventoryAudioContainerAddress": None,
        "slot": None,
        "overrideMassAndDrag": True,
        "mass": mass,
        "drag": 1.0,
        "angularDrag": 0.05,
        "damagers": [
            {
                "$type": "ThunderRoad.ItemData+Damager, ThunderRoad",
                "transformName": "Damager",
                "damagerID": "SwordSharp1H",  # sharp, modifiable via our DM later
            }
        ],
        "_nssp_note": f"Energy attack projectile (prefab {prefab})",
    }

# Kamehameha energy beam projectile (fast, high-damage)
kame = make_projectile("SuperSaiyan_Kamehameha", "Kamehameha Wave",
                       "Bas.Item.Misc.ProjectileMeteor", 30, 3, mass=1.5)
(MOD / "Items" / "Item_SuperSaiyan_Kamehameha.json").write_text(json.dumps(kame, indent=1))

# Big Bang Attack energy sphere
bigbang = make_projectile("SuperSaiyan_BigBang", "Big Bang Attack",
                          "Bas.Item.Misc.ProjectileFireball", 45, 4, mass=2.5)
(MOD / "Items" / "Item_SuperSaiyan_BigBang.json").write_text(json.dumps(bigbang, indent=1))

# ---------- Spells ----------

def make_spell(sid, name, item_id, charge_effect, desc, order, mana=10.0):
    return {
        "$type": "DragonBall.SuperSayan, DBZ",  # reuse base cast type so orb casts work
        "id": sid,
        "sensitiveContent": "None",
        "sensitiveFilterBehaviour": "Discard",
        "version": 0,
        "castDescription": desc,
        "imbueDescription": None,
        "chargeEffectId": charge_effect,
        "readyEffectId": charge_effect,
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
        "allowThrow": True,        # throw spawns the projectile
        "throwEffectId": charge_effect,
        "throwMinCharge": 0.5,
        "allowSpray": False,
        "imbueEnabled": True,
        "imbueRate": 1.0,
        "wallDisplayName": name,
        "hasOrder": True,
        "order": order,
        "iconEffectId": "SpellOrbTest",
        "aiCastType": "CastSimple",
        "minMana": mana,
        "shardId": "Crystal_Small_01_Shard",
        "prefabAddress": "Bas.Item.Misc.SkillOrb",
        "allowSkill": True,
        "showInTree": True,
        "hideInSkillMenu": False,
        "skillTreeDisplayName": name,
        "description": desc,
        "isDefaultSkill": False,
        "primarySkillTreeId": "Gravity",
        "isTierBlocker": False,
        "ReadyThreshold": 0.5,
        "Ready": False,
        "Order": order,
        "IsCombinedSkill": False,
        # Runtime hooks (read by SSJMod.dll)
        "nssp": {
            "projectileId": item_id,
            "spellKind": sid,
        },
    }

(MOD / "Spells" / "Spell.SuperSaiyan_Kamehameha.json").write_text(
    json.dumps(make_spell("SuperSaiyan_Kamehameha", "Kamehameha",
                          "SuperSaiyan_Kamehameha", "SuperSaiyan_SSB_Aura",
                          "Charge both hands, release to fire a devastating Kamehameha wave.",
                          11, mana=15.0), indent=1))

(MOD / "Spells" / "Spell.SuperSaiyan_BigBang.json").write_text(
    json.dumps(make_spell("SuperSaiyan_BigBang", "Big Bang Attack",
                          "SuperSaiyan_BigBang", "SuperSaiyan_SSG_Aura",
                          "One-handed concentrated ki sphere — the Big Bang Attack.",
                          12, mana=12.0), indent=1))

print(f"Kamehameha + Big Bang spells + projectiles written to {MOD}")
print("Instant Transmission (MUI teleport) logic goes into the DLL build next.")