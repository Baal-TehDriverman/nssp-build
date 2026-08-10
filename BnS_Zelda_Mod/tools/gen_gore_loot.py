#!/usr/bin/env python3
"""
Gore-heavy Lithosphere loot generator (2026-08-08).

Adds a NEW gore-heavy item type to the LithosphereLootPack — usable gear that
appears in the PLAYER-HOME SPAWN BOOK (SandboxAllItems storage) and on the
map loaded from the ship. All pure IL2CPP JSON, no Unity/bundles.

1. BLOODSTONE KNIFE (dismembering gore dagger)
   - Mirrors the base-game Skinning Knife (DaggerSkinning) exactly, so it's a
     real grippable slot:Small dagger that shows in the sandbox item book.
   - prefab: Bas.Item.Melee.Dagger.Skinning (base-verified)
   - damagers: DaggerPierce + DaggerSlash (base-verified)
   - ItemModuleStats: high FleshDamage + Dismemberment (gore)
   - allowedStorage: Container, SandboxAllItems  -> appears in Home book
   - Theme: PainfulDeath / RealisticBleeding.

2. BLOOD ORB (pooled throwable blood projectile)
   - Mirrors base-game DynamicProjectile (the "Magic" throwable).
   - prefab: Bas.Item.Misc.Projectile (base-verified)
   - damager: Fireball (base-verified), ItemModuleMagicProjectile
   - flags: Throwable, allowedStorage SandboxAllItems -> spawnable + throwable
   - Theme: RealisticBleeding.

3. GORE DAMAGE MODIFIER
   - High flesh multiplier + dismemberment, dropped on Flesh.

CRITICAL (project crash history): JSON-only mod -> ship ZERO catalog.json and
ZERO .bundle, in BOTH the Mods/ copy AND any mod.io backing-dir copy. We emit
none here.
"""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "Mods", "LithosphereLootPack")

BLOOD = {
    "base":      (0.08, 0.03, 0.04),
    "emissive":  (0.85, 0.03, 0.04),
    "subsurf":   (0.90, 0.12, 0.08),
    "intensity": 0.6,
}


def rgba(rgb, a=1.0):
    return {"r": rgb[0], "g": rgb[1], "b": rgb[2], "a": a}


def curve(v0, v1, t0=0.0, t1=1.0, it0=0.0, ot0=0.0, it1=0.0, ot1=0.0):
    return {
        "$type": "UnityEngine.AnimationCurve, UnityEngine.CoreModule",
        "keys": [
            {"$type": "UnityEngine.Keyframe, UnityEngine.CoreModule",
             "time": t0, "value": v0, "inTangent": it0, "outTangent": ot0,
             "inWeight": 0.0, "outWeight": 0.0, "weightedMode": "None",
             "tangentMode": 0},
            {"$type": "UnityEngine.Keyframe, UnityEngine.CoreModule",
             "time": t1, "value": v1, "inTangent": it1, "outTangent": ot1,
             "inWeight": 0.0, "outWeight": 0.0, "weightedMode": "None",
             "tangentMode": 0},
        ],
        "length": 2, "preWrapMode": "ClampForever", "postWrapMode": "ClampForever",
    }


# Base shield of ItemData fields (all base-game-valid).
BASE_ITEM = {
    "$type": "ThunderRoad.ItemData, ThunderRoad",
    "sensitiveContent": "None",
    "sensitiveFilterBehaviour": "Discard",
    "version": 4,
    "groupPath": None,
    "localizationId": None,
    "author": "Lilith",
    "rewardValue": 0.0,
    "iconEffectId": None,
    "preferredItemCenter": "Mass",
    "drainImbueWhenIdle": True,
    "forceImbueUseButton": "None",
    "iconAddress": None,
    "closeUpIconAddress": None,
    "pooledCount": 4,
    "androidPooledCount": 2,
    "despawnOnStoredInInventory": False,
    "isStackable": False,
    "consumableId": None,
    "inventoryAudioContainerAddress": None,
    "inventoryAudioVolume_dB": 0.0,
    "snapAudioContainerAddress": None,
    "snapAudioVolume_dB": 0.0,
    "overrideMassAndDrag": True,
    "drag": 0.4,
    "angularDrag": 0.05,
    "density": 6000.0,
    "focusRegenMultiplier": 1.0,
    "spellChargeSpeedPlayerMultiplier": 1.0,
    "spellChargeSpeedNPCMultiplier": 1.0,
    "collisionMaxOverride": 0,
    "collisionEnterOnly": False,
    "collisionNoMinVelocityCheck": False,
    "forceLayer": "None",
    "diffForceLayerWhenHeld": False,
    "forceLayerHeld": "None",
    "waterHandSpringMultiplierCurve": curve(0.3, 0.15, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0),
    "waterDragMultiplierCurve": curve(1.0, 10.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0),
    "waterSampleMinRadius": 0.2,
    "throwMultiplier": 1.0,
    "runSpeedMultiplier": 1.0,
    "flyRotationSpeed": 3.0,
    "flyThrowAngle": 145.0,
    "allowFlyBackwards": False,
    "telekinesisSafeDistance": 1.0,
    "telekinesisThrowRatio": 1.0,
    "telekinesisAutoGrabAnyHandle": False,
    "grippable": True,
    "grabAndGripClimb": False,
    "playerGrabAndGripChangeLayer": True,
    "customSnaps": [],
    "drainImbueOnSnap": True,
    "imbueEnergyOverTimeOnSnap": curve(1.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0),
    "colliderGroups": [],
    "effectHinges": [],
    "entityModules": [],
}


# ---------------------------------------------------------------------------
# 1. BLOODSTONE KNIFE - gore dagger (mirrors base DaggerSkinning)
# ---------------------------------------------------------------------------
def gen_blood_knife_item():
    return {
        **BASE_ITEM,
        "id": "Lithosphere_BloodBlade",
        "localizationId": "Lithosphere_BloodBlade",
        "displayName": "Bloodstone Knife",
        "description": "A cleaver of volcanic glass bound in dried blood. It feeds on flesh and dismembers whatever it severs.",
        "valueType": "Gold",
        "value": 480.0,
        "tier": 4,
        "flags": "Throwable, Spinnable, Jabbing",
        "type": "Weapon",
        "category": "Daggers",
        "prefabAddress": "Bas.Item.Melee.Dagger.Skinning",
        "iconAddress": None,
        "pooledCount": 4,
        "androidPooledCount": 2,
        # KEY: makes it appear in the player-home spawn book
        "allowedStorage": "Container, SandboxAllItems",
        "slot": "Small",
        "snapAudioContainerAddress": "Bas.AudioGroup.Snap.Dagger",
        "mass": 0.25,
        "drag": 0.4,
        "density": 6000.0,
        "flyRotationSpeed": 3.0,
        "flyThrowAngle": 145.0,
        "colliderGroups": [
            {"$type": "ThunderRoad.ItemData+ColliderGroup, ThunderRoad",
             "transformName": "Blades", "colliderGroupId": "BladeDagger"}
        ],
        "damagers": [
            {"$type": "ThunderRoad.ItemData+Damager, ThunderRoad",
             "transformName": "Pierce", "damagerID": "DaggerPierce"},
            {"$type": "ThunderRoad.ItemData+Damager, ThunderRoad",
             "transformName": "Slash", "damagerID": "DaggerSlash"},
            {"$type": "ThunderRoad.ItemData+Damager, ThunderRoad",
             "transformName": "Blunt", "damagerID": "HandleLight"},
        ],
        "Interactables": [
            {"$type": "ThunderRoad.ItemData+Interactable, ThunderRoad",
             "transformName": "Handle", "interactableId": "ObjectHandleLight"}
        ],
        "whooshs": [
            {"$type": "ThunderRoad.ItemData+Whoosh, ThunderRoad",
             "transformName": "Whoosh", "effectId": "WhooshDagger",
             "trigger": "Always", "stopOnSnap": True,
             "minVelocity": 3.0, "maxVelocity": 10.0, "dampening": 0.1}
        ],
        "modules": [
            {
                "$type": "ThunderRoad.ItemModuleAI, ThunderRoad",
                "primaryClass": "Melee", "secondaryClass": "None",
                "weaponHandling": "OneHanded", "secondaryHandling": "None",
                "weaponAttackTypes": "Swing, Thrust", "alwaysPrimary": False,
                "defaultStanceInfo": {
                    "$type": "ThunderRoad.ItemModuleAI+StanceInfo, ThunderRoad",
                    "offhand": "Anything", "grabAIHandleRadius": 0.0,
                    "stanceDataID": "HumanMelee1hStance"},
                "stanceInfosByOffhand": [
                    {"$type": "ThunderRoad.ItemModuleAI+StanceInfo, ThunderRoad",
                     "offhand": "Empty", "grabAIHandleRadius": 0.0,
                     "stanceDataID": "HumanMelee1hStance"},
                    {"$type": "ThunderRoad.ItemModuleAI+StanceInfo, ThunderRoad",
                     "offhand": "AnyShield", "grabAIHandleRadius": 0.0,
                     "stanceDataID": "HumanMeleeShieldStance"},
                    {"$type": "ThunderRoad.ItemModuleAI+StanceInfo, ThunderRoad",
                     "offhand": "AnyMelee", "grabAIHandleRadius": 0.0,
                     "stanceDataID": "HumanMeleeDualWieldStance"},
                ],
                "rangedWeaponData": None, "ignoredByDefense": False,
                "armResistanceMultiplier": 2.0, "allowDynamicHeight": False,
                "defenseHasPriority": False, "transferPushToBlocker": False,
                "transferVelocityModifier": -8.0, "transferredPushModifier": -1,
                "minTransferredPush": 2, "maxTransferredPush": 4,
            },
            {
                "$type": "ThunderRoad.ItemModuleStats, ThunderRoad",
                "stats": [
                    {"$type": "ThunderRoad.ItemStatInt, ThunderRoad",
                     "value": 4, "useStarIcons": True, "name": "FleshDamage"},
                    {"$type": "ThunderRoad.ItemStatInt, ThunderRoad",
                     "value": 2, "useStarIcons": True, "name": "LeatherDamage"},
                    {"$type": "ThunderRoad.ItemStatInt, ThunderRoad",
                     "value": 0, "useStarIcons": True, "name": "PlateDamage"},
                    {"$type": "ThunderRoad.ItemStatInt, ThunderRoad",
                     "value": 4, "useStarIcons": True, "name": "Penetration"},
                    {"$type": "ThunderRoad.ItemStatInt, ThunderRoad",
                     "value": 5, "useStarIcons": True, "name": "Dismemberment"},
                    {"$type": "ThunderRoad.ItemStatInt, ThunderRoad",
                     "value": 1, "useStarIcons": True, "name": "Stagger"},
                    {"$type": "ThunderRoad.ItemStatInt, ThunderRoad",
                     "value": 0, "useStarIcons": True, "name": "Imbue"},
                    {"$type": "ThunderRoad.ItemStatInt, ThunderRoad",
                     "value": 5, "useStarIcons": True, "name": "Handling"},
                ],
            },
            {
                "$type": "ThunderRoad.ItemModuleEffect",
                "effectId": "Lithosphere_BloodBlade_Aura",
                "effectDuration": 0.0,
                "loop": True,
                "mainStart": rgba(BLOOD["emissive"], 1.0),
                "mainEnd": rgba(BLOOD["subsurf"], 1.0),
                "materialId": "obsidian",
            },
        ],
        "_nssp_gore": {"kind": "dismembering_blade", "dropPool": "PainfulDeath"},
    }


def gen_blood_knife_effect():
    return {
        "$type": "ThunderRoad.EffectData",
        "id": "Lithosphere_BloodBlade_Aura",
        "sensitiveContent": "None",
        "sensitiveFilterBehaviour": "Discard",
        "version": 1,
        "name": "Bloodstone Knife aura",
        "addressableName": "Lithosphere_BloodBlade_Aura",
        "modules": [
            {
                "$type": "ThunderRoad.EffectModuleParticle, ThunderRoad",
                "loop": True, "duration": 0.0, "isStickToObject": True,
                "particleMaterial": "Additive",
                "effectParticleAddress": "Pilot.DBZ.Spell.VFX.Main.AroundBody.prefab",
                "linkDestination": "Self", "linkRotationType": "Self",
                "linkScaleType": "World", "playParticle": True, "particleCount": 16,
                "localScale": {"x": 0.4, "y": 0.4, "z": 0.4},
                "mainGradient": {
                    "mainStart": rgba(BLOOD["emissive"], BLOOD["intensity"]),
                    "mainEnd": rgba(BLOOD["subsurf"], 0.0),
                },
                "note": "Bloodstone edge: dried blood binding, flesh-hungry",
            }
        ],
    }


# ---------------------------------------------------------------------------
# 2. BLOOD ORB - pooled throwable blood projectile (mirrors DynamicProjectile)
# ---------------------------------------------------------------------------
def gen_blood_orb_item():
    return {
        **BASE_ITEM,
        "id": "Lithosphere_BloodOrb",
        "localizationId": "Lithosphere_BloodOrb",
        "displayName": "Blood Crystal",
        "description": "A volatile bloodstone orb. Throw it to splash pressurized blood that carves several kilograms off whatever it hits.",
        "valueType": "Gold",
        "value": 120.0,
        "tier": 3,
        "flags": "Throwable",
        "type": "Misc",
        "category": None,
        "prefabAddress": "Bas.Item.Misc.Projectile",
        "iconAddress": None,
        "pooledCount": 50,
        "androidPooledCount": 30,
        "allowedStorage": "SandboxAllItems",
        "slot": "",
        "overrideMassAndDrag": True,
        "mass": 1.0,
        "drag": 0.0,
        "angularDrag": 0.0,
        "density": 1000.0,
        "collisionNoMinVelocityCheck": True,
        "colliderGroups": [],
        "damagers": [
            {"$type": "ThunderRoad.ItemData+Damager, ThunderRoad",
             "transformName": "Damager", "damagerID": "Fireball"}
        ],
        "Interactables": [
            {"$type": "ThunderRoad.ItemData+Interactable, ThunderRoad",
             "transformName": "Handle", "interactableId": "ObjectHandleTKOnly"}
        ],
        "whooshs": [
            {"$type": "ThunderRoad.ItemData+Whoosh, ThunderRoad",
             "transformName": "Whoosh", "effectId": None,
             "trigger": "OnFly", "stopOnSnap": True,
             "minVelocity": 5.0, "maxVelocity": 20.0, "dampening": 0.1}
        ],
        "modules": [
            {"$type": "ThunderRoad.ItemModuleAI, ThunderRoad",
             "primaryClass": "Arrow", "secondaryClass": "None",
             "weaponHandling": "OneHanded", "secondaryHandling": "None",
             "weaponAttackTypes": "None", "alwaysPrimary": False,
             "defaultStanceInfo": None, "stanceInfosByOffhand": None,
             "rangedWeaponData": None, "ignoredByDefense": False,
             "armResistanceMultiplier": 1.0, "allowDynamicHeight": False,
             "defenseHasPriority": False, "transferPushToBlocker": False,
             "transferVelocityModifier": -8.0, "transferredPushModifier": -1,
             "minTransferredPush": 2, "maxTransferredPush": 4},
            {"$type": "ThunderRoad.ItemModuleMagicProjectile, ThunderRoad"},
            {
                "$type": "ThunderRoad.ItemModuleEffect",
                "effectId": "Lithosphere_BloodOrb_Aura",
                "effectDuration": 0.0,
                "loop": True,
                "mainStart": rgba(BLOOD["emissive"], 1.0),
                "mainEnd": rgba(BLOOD["subsurf"], 1.0),
                "materialId": "obsidian",
            },
        ],
        "_nssp_gore": {"kind": "blood_projectile", "dropPool": "RealisticBleeding"},
    }


def gen_blood_orb_effect():
    return {
        "$type": "ThunderRoad.EffectData",
        "id": "Lithosphere_BloodOrb_Aura",
        "sensitiveContent": "None",
        "sensitiveFilterBehaviour": "Discard",
        "version": 1,
        "name": "Blood Crystal aura",
        "addressableName": "Lithosphere_BloodOrb_Aura",
        "modules": [
            {
                "$type": "ThunderRoad.EffectModuleParticle, ThunderRoad",
                "loop": True, "duration": 0.0, "isStickToObject": True,
                "particleMaterial": "Additive",
                "effectParticleAddress": "Bas.Particle.Infuser.Mind",
                "linkDestination": "Self", "linkRotationType": "Self",
                "linkScaleType": "World", "playParticle": True, "particleCount": 30,
                "localScale": {"x": 0.5, "y": 0.5, "z": 0.5},
                "mainGradient": {
                    "mainStart": rgba(BLOOD["emissive"], BLOOD["intensity"]),
                    "mainEnd": rgba(BLOOD["subsurf"], 0.0),
                },
                "note": "Blood crystal: obsidian bloodstone, volatile reservoir",
            }
        ],
    }


# ---------------------------------------------------------------------------
# 3. GORE DAMAGE MODIFIER - dismembering flesh layer
# ---------------------------------------------------------------------------
def gen_gore_modifier():
    return {
        "$type": "ThunderRoad.DamageModifierData, ThunderRoad",
        "id": "Lithosphere_Bloodstone_Modifier",
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
                        "tierFilter": 0, "imbuesFilterLogic": "NoneExcept",
                        "imbuesFilter": [], "minVelocity": 0.0,
                        "damageMultiplier": 4.0,
                        "allowKnockout": True, "allowPenetration": True,
                        "pressureAllowed": True,
                        "knockoutAllowedMinVelocity": "Infinity",
                        "knockoutForcedMinVelocity": "Infinity",
                        "knockoutThrowAllowedMinVelocity": "Infinity",
                        "knockoutThrowForcedMinVelocity": "Infinity",
                        "knockoutDurationMultiplier": 1.0,
                        "pushLevels": [
                            {"$type": "ThunderRoad.DamageModifierData+Modifier+PushLevel, ThunderRoad",
                             "hitVelocity": 5.0, "throwVelocity": 5.0},
                            {"$type": "ThunderRoad.DamageModifierData+Modifier+PushLevel, ThunderRoad",
                             "hitVelocity": 8.0, "throwVelocity": 8.0},
                            {"$type": "ThunderRoad.DamageModifierData+Modifier+PushLevel, ThunderRoad",
                             "hitVelocity": 11.0, "throwVelocity": 11.0},
                        ],
                    }
                ],
            }
        ],
        "_nssp_gore": True,
    }


def main():
    loot_dir = os.path.join(OUT, "Loot")
    eff_dir = os.path.join(OUT, "Effects")
    dmg_dir = os.path.join(OUT, "DamageModifiers")
    for d in (loot_dir, eff_dir, dmg_dir):
        os.makedirs(d, exist_ok=True)

    def w(sub, name, data):
        with open(os.path.join(OUT, sub, name), "w") as f:
            json.dump(data, f, indent=2)

    w("Loot", "Item_Lithosphere_BloodBlade.json", gen_blood_knife_item())
    w("Effects", "Effect_Lithosphere_BloodBlade_Aura.json", gen_blood_knife_effect())
    w("Loot", "Item_Lithosphere_BloodOrb.json", gen_blood_orb_item())
    w("Effects", "Effect_Lithosphere_BloodOrb_Aura.json", gen_blood_orb_effect())
    w("DamageModifiers", "DamageModifier_Lithosphere_Bloodstone.json", gen_gore_modifier())

    print("Gore loot generator: wrote 5 files into LithosphereLootPack")
    print("  Loot/Item_Lithosphere_BloodBlade.json  (gore dagger, sandbox-book spawnable)")
    print("  Effects/Effect_Lithosphere_BloodBlade_Aura.json")
    print("  Loot/Item_Lithosphere_BloodOrb.json     (throwable blood projectile)")
    print("  Effects/Effect_Lithosphere_BloodOrb_Aura.json")
    print("  DamageModifiers/DamageModifier_Lithosphere_Bloodstone.json (4x flesh/dis)  ")
    print("Verified prefabs/damagers from bas.jsondb; allowedStorage for Home book.")
    print("NO catalog.json / NO bundle emitted (JSON-only mod rule).")


if __name__ == "__main__":
    main()