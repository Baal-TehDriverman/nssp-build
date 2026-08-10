#!/usr/bin/env python3
"""Generate Zelda campaign equipment items as B&S Item JSON files."""
import json
import os

ITEMS_DIR = "/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods/ZeldaCampaign/Items"
os.makedirs(ITEMS_DIR, exist_ok=True)

def write_item(item_id, name, item_type, description, damage=0, defense=0, **kwargs):
    """Write a B&S Item JSON file."""
    item = {
        "id": item_id,
        "name": name,
        "type": item_type,
        "description": description,
        "damage": damage,
        "defense": defense,
        "weight": 1.0,
        "value": 10,
        "tags": ["Zelda", "Campaign"],
        **kwargs
    }
    path = os.path.join(ITEMS_DIR, f"Item_{item_id}.json")
    with open(path, 'w') as f:
        json.dump(item, f, indent=2)
    print(f"Created: {path}")

# Swords
write_item("KokiriSword", "Kokiri Sword", "Sword", "A small sword for a child.", damage=1, defense=0, tags=["Zelda", "Campaign", "Sword", "Weapon"])
write_item("MasterSword", "Master Sword", "Sword", "The blade of evil's bane. Fires beams at full health.", damage=2, defense=1, tags=["Zelda", "Campaign", "Sword", "Weapon", "KeyItem", "Holy"])
write_item("BiggoronSword", "Biggoron's Sword", "Sword", "A massive two-handed sword. Cannot use shield.", damage=4, defense=0, tags=["Zelda", "Campaign", "Sword", "Weapon", "TwoHanded"])

# Shields
write_item("DekuShield", "Deku Shield", "Shield", "Wooden shield. Burns easily.", damage=0, defense=1, tags=["Zelda", "Campaign", "Shield", "Wooden"])
write_item("HylianShield", "Hylian Shield", "Shield", "Legendary shield. Reflects projectiles on perfect parry.", damage=0, defense=2, tags=["Zelda", "Campaign", "Shield", "KeyItem"])
write_item("MirrorShield", "Mirror Shield", "Shield", "Reflects magic and light.", damage=0, defense=3, tags=["Zelda", "Campaign", "Shield", "KeyItem", "Magic"])

# Tools
write_item("Hookshot", "Hookshot", "Tool", "Grapple to surfaces and pull yourself or items.", damage=0, defense=0, tags=["Zelda", "Campaign", "Tool", "KeyItem"], customData={"range": 15, "pullsPlayer": True})
write_item("Longshot", "Longshot", "Tool", "Longer range Hookshot.", damage=0, defense=0, tags=["Zelda", "Campaign", "Tool", "KeyItem", "Upgrade"], customData={"range": 30, "pullsPlayer": True})
write_item("Boomerang", "Boomerang", "Tool", "Stuns enemies, retrieves items, hits switches.", damage=1, defense=0, tags=["Zelda", "Campaign", "Tool", "Weapon", "KeyItem"], customData={"returns": True, "stuns": True})
write_item("Bomb", "Bomb", "Consumable", "Explodes after short fuse. Blows up walls and enemies.", damage=3, defense=0, tags=["Zelda", "Campaign", "Consumable", "Explosive"], customData={"fuseTime": 3, "explosionRadius": 3})
write_item("Bow", "Fairy Bow", "Ranged", "Shoots arrows. Can use elemental arrows.", damage=1, defense=0, tags=["Zelda", "Campaign", "Ranged", "Weapon", "KeyItem"], customData={"usesArrows": True})
write_item("FireArrows", "Fire Arrows", "Arrow", "Burns enemies and lights torches.", damage=2, defense=0, tags=["Zelda", "Campaign", "Arrow", "Magic", "Fire"], customData={"element": "Fire", "setsOnFire": True})
write_item("IceArrows", "Ice Arrows", "Arrow", "Freezes enemies and water.", damage=2, defense=0, tags=["Zelda", "Campaign", "Arrow", "Magic", "Ice"], customData={"element": "Ice", "freezes": True})
write_item("LightArrows", "Light Arrows", "Arrow", "Pierces evil. Required for Ganon.", damage=3, defense=0, tags=["Zelda", "Campaign", "Arrow", "Magic", "Holy", "KeyItem"], customData={"element": "Light", "piercesEvil": True})

# Magic Spells
write_item("DinFire", "Din's Fire", "Magic", "Creates a dome of fire around you.", damage=2, defense=0, tags=["Zelda", "Campaign", "Magic", "Fire"], customData={"magicCost": 12, "radius": 5, "fireDamage": True})
write_item("FaroresWind", "Farore's Wind", "Magic", "Sets a warp point and returns to it.", damage=0, defense=0, tags=["Zelda", "Campaign", "Magic", "Utility"], customData={"magicCost": 16, "setsWarpPoint": True})
write_item("NayrusLove", "Nayru's Love", "Magic", "Invincibility barrier for short duration.", damage=0, defense=999, tags=["Zelda", "Campaign", "Magic", "Defense"], customData={"magicCost": 20, "duration": 10, "invincible": True})

# Armor/Clothing
write_item("GoronTunic", "Goron Tunic", "Armor", "Protects from extreme heat.", damage=0, defense=2, tags=["Zelda", "Campaign", "Armor", "KeyItem", "FireResist"], customData={"heatResist": True})
write_item("ZoraTunic", "Zora Tunic", "Armor", "Allows underwater breathing.", damage=0, defense=1, tags=["Zelda", "Campaign", "Armor", "KeyItem", "WaterBreathing"], customData={"waterBreathing": True})
write_item("HoverBoots", "Hover Boots", "Boots", "Walk on air briefly.", damage=0, defense=0, tags=["Zelda", "Campaign", "Boots", "KeyItem"], customData={"hoverTime": 3, "preventsFallDamage": True})
write_item("IronBoots", "Iron Boots", "Boots", "Sink in water, resist wind.", damage=1, defense=2, tags=["Zelda", "Campaign", "Boots", "KeyItem"], customData={"sinksInWater": True, "windResist": True, "moveSpeed": -0.5})

# Gauntlets
write_item("SilverGauntlets", "Silver Gauntlets", "Gauntlets", "Lifts heavy blocks.", damage=1, defense=1, tags=["Zelda", "Campaign", "Gauntlets", "KeyItem"], customData={"liftStrength": "Heavy"})
write_item("GoldenGauntlets", "Golden Gauntlets", "Gauntlets", "Lifts massive blocks.", damage=2, defense=2, tags=["Zelda", "Campaign", "Gauntlets", "KeyItem", "Upgrade"], customData={"liftStrength": "Massive"})

# Containers
write_item("Bottle", "Empty Bottle", "Container", "Catch fairies, potions, bugs, fish.", damage=0, defense=0, tags=["Zelda", "Campaign", "Container", "KeyItem"], customData={"canHold": ["Fairy", "Potion", "Bug", "Fish", "Milk", "Poe"]})

# Currency
write_item("Rupee", "Rupee", "Currency", "Green=1, Blue=5, Red=20, Purple=50, Silver=100, Gold=300.", damage=0, defense=0, tags=["Zelda", "Campaign", "Currency"], customData={"values": {"Green": 1, "Blue": 5, "Red": 20, "Purple": 50, "Silver": 100, "Gold": 300}})

# Megaton Hammer
write_item("MegatonHammer", "Megaton Hammer", "Tool", "Smashes heavy switches and enemies.", damage=3, defense=1, tags=["Zelda", "Campaign", "Tool", "Weapon", "KeyItem", "Heavy"], customData={"smashesSwitches": True, "stunsEnemies": True})

# Lens of Truth
write_item("LensOfTruth", "Lens of Truth", "Tool", "Reveals invisible things and illusions.", damage=0, defense=0, tags=["Zelda", "Campaign", "Tool", "KeyItem"], customData={"revealsInvisible": True, "magicDrain": 1})

print("\nAll Zelda equipment generated successfully!")
