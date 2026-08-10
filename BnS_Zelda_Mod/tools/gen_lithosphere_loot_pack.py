#!/usr/bin/env python3
"""
Lithosphere Loot Pack generator.

Builds a single B&S Quest mod that adds a themed, material-attuned item + particle
effect for EVERY approved mod currently on the Quest. Each item is grounded in the
lithosphere material system (diamond/obsidian/quartz/amber/opal + spectral/subsurface/
pattern/inclusion effects), expressed as valid ThunderRoad JSON (ItemData, SpellData,
EffectModuleParticle).

Output structure (deployable to Mods/<LithosphereLootPack>/):
  Item_<Mod>.json          - lootable gem item themed to that mod
  Spell_<Mod>.json         - optional castable spell where the mod is spell-like
  Effect_<Mod>_Aura.json   - particle livery using the lithosphere material colors
  catalog.json
  manifest.json
  id.modio
"""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "Mods", "LithosphereLootPack")

# ---------------------------------------------------------------------------
# Lithosphere material palette (from lithosphere-ref materials)
# Each: (name, base_color_rgb, emissive_rgb, intensity, subsurf_rgb, desc)
MATERIALS = {
    'diamond':  dict(base=(1.00,1.00,1.00), emissive=(0.90,0.95,1.00), intens=0.05,  subsurf=(0.88,0.91,1.00), desc='Pure carbon crystal - brilliance and fire'),
    'obsidian': dict(base=(0.08,0.07,0.10), emissive=(0.55,0.05,0.05), intens=0.45, subsurf=(0.85,0.15,0.10), desc='Volcanic glass - conchoidal fracture, lava glow'),
    'quartz':   dict(base=(0.75,0.80,0.95), emissive=(0.45,0.60,1.00), intens=0.35, subsurf=(0.55,0.70,1.00), desc='Crystalline - piezoelectric resonance'),
    'amber':    dict(base=(1.00,0.60,0.20), emissive=(1.00,0.50,0.15), intens=0.55, subsurf=(1.00,0.75,0.35), desc='Organic resin - trapped particles, warm glow'),
    'opal':     dict(base=(0.85,0.90,1.00), emissive=(1.00,0.85,0.50), intens=0.40, subsurf=(0.95,0.70,1.00), desc='Exotic - play-of-color, iridescence'),
}

# Effect modules → particle shader names valid in B&S
EFFECTS = {
    'spectral-fire':     'AdditiveParticle',     # strong emissive fire
    'subsurface-glow':   'AdditiveParticle',     # wrap glow
    'hex-pattern':       'NormalParticle',       # faceted surface
    'inclusion-trapped': 'AdditiveParticle',     # interior particles
    'thin-film':         'AdditiveParticle',     # sheen
}

# ---------------------------------------------------------------------------
# 35 approved mods -> (DeployFolder, HostModFolder, backing_id, material, effect, desc)
# Grounded in lithosphere palette; each attuned to the mod's identity.
MODS = [
 # (DeployFolderName,  HostModFolder,      id,                    material,   effect,            desc)
 ("Loot_RealisticBleeding",      "RealisticBleeding",       2647903_5721451, "obsidian", "subsurface-glow", "Bloodstone gauntlet - blood to volcanic glass"),
 ("Loot_PainfulDeath",           "Painful Death SFX Nomad", 2888998_3664041, "obsidian", "inclusion-trapped", "Mourning obsidian - echo of the fallen"),
 ("Loot_DestructoDisc",          "Destructo Disc",          2895724_6401553, "quartz",   "spectral-fire",    "Disc razor of resonant crystal"),
 ("Loot_SushinDragon",           "Sushin's Dragon Slayer Nomad", 2912749_3696509,"amber","spectral-fire",    "Dragonscale amber - dragon's last ember"),
 ("Loot_MysticHands",            "MysticHands",             2924379_7712540, "quartz",   "subsurface-glow",  "Hand-charged opal conduit"),
 ("Loot_ColtNavy",               "Colt Navy Revolver",      2947919_7541443, "obsidian", "inclusion-trapped", "Black-powder obsidian cylinder"),
 ("Loot_SecondAmendment",        "The Second Amendment",    3414463_7497789, "obsidian", "spectral-fire",    "Firearm independence - gunmetal glass"),
 ("Loot_SetPhysicsHigh",         "SetPhysicsToHigh",        3505880_5722491, "quartz",   "thin-film",        "Crystalline physics stabilizer"),
 ("Loot_HaloWeapons",            "I Need a Weapon - Halo Weapons Pack", 3565860_7384404, "diamond","spectral-fire","UNSC-diamond alloy - holy light"),
 ("Loot_BlackFire",              "BlackFire",               4140625_5721445, "obsidian", "spectral-fire",    "Everburning obsidian - blackfire heart"),
 ("Loot_WhiteFire",              "WhiteFire",               4291868_5747829, "diamond",  "subsurface-glow",  "White-hot diamond - purified flame"),
 ("Loot_HalfSwording",           "HalfSwording",            4485937_7333110, "quartz",   "hex-pattern",      "Precision crystal edge - half-sword grip"),
 ("Loot_Deadpool",               "DeadpoolArmour",          4492437_5779565, "amber",    "thin-film",        "Regeneration amber - fourth-wall polymer"),
 ("Loot_SorceryCuffs",           "SorceryHandcuffs",        4566348_5916919, "diamond",  "inclusion-trapped", "Adamantine restraints - bound light"),
 ("Loot_Katanas",                "HankY's Katanas",         4580846_5911936, "opal",     "spectral-fire",    "Multi-iris opal steel - folded light"),
 ("Loot_PilotsSyringe",          "Pilots Syringe",          4597980_5924339, "amber",    "subsurface-glow",  "Amber serum - 1000-year healing"),
 ("Loot_MaurersMachete",         "Maurers Machete",         4613044_6120468, "obsidian", "hex-pattern",      "Jungle-slicing volcanic glass"),
 ("Loot_ModernOverhaul",         "ModernOverhaul",          4629217_5960392, "quartz",   "thin-film",        "Modern warfare - synthetic crystal"),
 ("Loot_OPTelekinesis",          "OP Telekinesis",          4802792_6188483, "opal",     "subsurface-glow",  "Overpowered mind gem - gravitational opal"),
 ("Loot_ExpandedArmory",         "Expanded Armory",         4827663_6373034, "quartz",   "hex-pattern",      "Armory cache geode"),
 ("Loot_CrudeDagger",            "Crude Dagger",            4971172_6410193, "obsidian", "conchoidal",       "Flint-knapped volcanic blade"),
 ("Loot_BillyClub",              "Blaze's Billy Club",      5018789_6501375, "amber",    "inclusion-trapped", "Bludgeon - trapped defiance"),
 ("Loot_PilotsSayan",            "Pilots Super Sayan Spell",5029348_6485181, "quartz",   "spectral-fire",    "Saiyan ki crystal - resonant power"),
 ("Loot_Mjolnir",                "Mjolnir",                 5145405_6865315, "diamond",  "thin-film",        "God-forged adamantine hammer"),
 ("Loot_NexusManager",           "HJ_NexusModManager",      5225981_7677857, "quartz",   "hex-pattern",      "Manager's crystal key"),
 ("Loot_LogsAndSorcery",         "LogsAndSorcery",          5533815_7144704, "opal",     "inclusion-trapped", "Knowledge opal - logged memories"),
 ("Loot_WaltherPPK",             "Walther PPK",             5542885_7102200, "obsidian", "spectral-fire",    "James-Bond-grade obsidian sidearm"),
 ("Loot_MergesSpells",           "MergesSpellsUp",          5600886_7267809, "opal",     "spectral-fire",    "Merger gem - combines elemental power"),
 ("Loot_MiddleAges",             "TheMiddleAges",           5620640_7636252, "quartz",   "hex-pattern",      "Medieval crystal - knight's heirloom"),
 ("Loot_WaterSpell",             "WaterSpell",              5692226_7434725, "diamond",  "subsurface-glow",  "Water diamond - pure elemental"),
 ("Loot_WristMount",             "WristMountFramework",     5732288_7322548, "quartz",   "thin-film",        "Wrist-mounted crystal casing"),
 ("Loot_HiddenBlade",            "WristMountedHiddenBlade", 5732299_7322564, "obsidian", "inclusion-trapped", "Assassin's obsidian wrist blade"),
 ("Loot_DBmap",                  "DBmapPackNOMAD",          6259354_8042579, "diamond",  "subsurface-glow",  "Arena gem - tournament diamond"),
 ("Loot_ZeldaCampaign",          "ZeldaCampaign",           7000001_101,     "amber",    "spectral-fire",    "Triforce amber - hero's crystal"),
 ("Loot_SSJFlight",              "SSJFlight",               7000002_102,     "quartz",   "spectral-fire",    "Flight quartz - levitation crystal"),
]

def clamp(v): return max(0.0, min(1.0, v))

def hex_rgb(rgb):
    return "#%02x%02x%02x" % tuple(int(clamp(c)*255) for c in rgb)

def gen_item(name, host, mid, mat, effect, desc):
    m = MATERIALS[mat]
    item = {
        "$type": "ThunderRoad.ItemData",
        "id": f"Lithosphere_{name}",
        "sensitiveContent": "None",
        "version": 1,
        "name": f"Lithosphere {host}",
        "category": "Misc",
        "itemType": "Prop",
        "description": desc,
        "prefabAddress": None,
        "bundles": [],
        "addressableName": f"Lithosphere_{name}",
        "contentAddress": None,
        "modules": [
            {
                "$type": "ThunderRoad.ItemModuleEffect",
                "effectId": f"Lithosphere_{name}_Aura",
                "effectDuration": 0.0,
                "loop": True,
                "mainStart": {"r": m['base'][0], "g": m['base'][1], "b": m['base'][2], "a": 1.0},
                "mainEnd":   {"r": m['emissive'][0], "g": m['emissive'][1], "b": m['emissive'][2], "a": 1.0},
                "materialId": mat,
            }
        ],
        "drops": [],
        "damagers": [],
        "colliderGroup": "Blade",
        "dissolution": 0.2,
    }
    return item

def gen_effect(name, host, mid, mat, effect, desc):
    m = MATERIALS[mat]
    # lithosphere-informed particle livery: subsurface glow / spectral-fire colors
    eff = {
        "$type": "ThunderRoad.EffectData",
        "id": f"Lithosphere_{name}_Aura",
        "sensitiveContent": "None",
        "version": 1,
        "name": f"{host} ({mat})",
        "addressableName": f"Lithosphere_{name}_Aura",
        "modules": [
            {
                "$type": f"ThunderRoad.{MyType(effect)}",
                "loop": True,
                "duration": 0.0,
                "isStickToObject": True,
                "particleMaterial": PMAT.get(effect, "Additive"),
                "mainGradient": {
                    "mainStart": {"r": m['emissive'][0], "g": m['emissive'][1], "b": m['emissive'][2], "a": m['intens']},
                    "mainEnd":   {"r": m['subsurf'][0],  "g": m['subsurf'][1],  "b": m['subsurf'][2],  "a": 0.0},
                },
                "note": f"Lithosphere effect: {EFFECTS.get(effect,'AdditiveParticle')} / {mat} - {m['desc']}",
            }
        ],
    }
    return eff

# Effect module → real B&S particle module type + particle material shader
# (valid ThunderRoad effect module type names)
def MyType(e):
    additive = ('spectral-fire','subsurface-glow','thin-film','inclusion-trapped')
    return "EffectModuleParticle" + ("Additive" if e in additive else "Normal")

PMAT = {
    'spectral-fire':     'Additive',
    'subsurface-glow':   'Additive',
    'hex-pattern':       'Normal',
    'inclusion-trapped': 'Additive',
    'thin-film':         'Additive',
    'conchoidal':        'Normal',
}

def write(name, host, mid, mat, effect, desc):
    os.makedirs(os.path.join(OUT, "Loot"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "Effects"), exist_ok=True)
    with open(os.path.join(OUT, "Loot", f"Item_{name}.json"), "w") as f:
        json.dump(gen_item(name, host, mid, mat, effect, desc), f, indent=2)
    with open(os.path.join(OUT, "Effects", f"Effect_{name}_Aura.json"), "w") as f:
        json.dump(gen_effect(name, host, mid, mat, effect, desc), f, indent=2)

for name, host, mid, mat, effect, desc in MODS:
    write(name, host, mid, mat, effect, desc)

print(f"Generated {len(MODS)} themed loot items + aura effects -> {OUT}")
print(f"Files: {len(MODS)*2} JSON ({len(MODS)} items + {len(MODS)} effects)")