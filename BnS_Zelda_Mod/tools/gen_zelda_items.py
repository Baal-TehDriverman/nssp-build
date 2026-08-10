#!/usr/bin/env python3
"""Generate Zelda campaign items as B&S Item JSON files."""
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

# Ocarina of Time
write_item(
    "OcarinaOfTime",
    "Ocarina of Time",
    "Instrument",
    "Play songs to warp, change time, control weather, and more.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "Instrument", "KeyItem"],
    slot="OffHand",
    customData={
        "songs": [
            "SongOfTime", "SongOfStorms", "EponasSong", 
            "SunsSong", "ZeldasLullaby", "MinuetOfForest",
            "BoleroOfFire", "SerenadeOfWater", "NocturneOfShadow",
            "RequiemOfSpirit", "PreludeOfLight"
        ],
        "usesMagic": True,
        "magicCost": 5
    }
)

# Important Chest Items
write_item(
    "BossKey",
    "Boss Key",
    "Key",
    "Opens the boss door in dungeons.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "KeyItem", "Dungeon"],
    customData={"singleUse": False}
)

write_item(
    "SmallKey",
    "Small Key",
    "Key",
    "Opens locked doors in dungeons.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "KeyItem", "Dungeon"],
    customData={"singleUse": True}
)

write_item(
    "DungeonMap",
    "Dungeon Map",
    "Map",
    "Reveals the full dungeon layout.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "KeyItem", "Dungeon"],
    customData={"revealsAllRooms": True}
)

write_item(
    "Compass",
    "Compass",
    "Tool",
    "Shows location of chests and boss.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "KeyItem", "Dungeon"],
    customData={"showsChests": True, "showsBoss": True}
)

# Spiritual Stones
write_item(
    "KokiriEmerald",
    "Kokiri Emerald",
    "SpiritualStone",
    "Spiritual Stone of the Forest.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "KeyItem", "SpiritualStone"],
    value=1000,
    customData={"element": "Forest", "opens": "DoorOfTime"}
)

write_item(
    "GoronRuby",
    "Goron Ruby",
    "SpiritualStone",
    "Spiritual Stone of Fire.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "KeyItem", "SpiritualStone"],
    value=1000,
    customData={"element": "Fire", "opens": "DoorOfTime"}
)

write_item(
    "ZoraSapphire",
    "Zora Sapphire",
    "SpiritualStone",
    "Spiritual Stone of Water.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "KeyItem", "SpiritualStone"],
    value=1000,
    customData={"element": "Water", "opens": "DoorOfTime"}
)

# Medallions
write_item(
    "ForestMedallion",
    "Forest Medallion",
    "Medallion",
    "Medallion of the Forest Sage.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "KeyItem", "Medallion"],
    value=500,
    customData={"sage": "Saria", "element": "Forest"}
)

write_item(
    "FireMedallion",
    "Fire Medallion",
    "Medallion",
    "Medallion of the Fire Sage.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "KeyItem", "Medallion"],
    value=500,
    customData={"sage": "Darunia", "element": "Fire"}
)

write_item(
    "WaterMedallion",
    "Water Medallion",
    "Medallion",
    "Medallion of the Water Sage.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "KeyItem", "Medallion"],
    value=500,
    customData={"sage": "Ruto", "element": "Water"}
)

write_item(
    "ShadowMedallion",
    "Shadow Medallion",
    "Medallion",
    "Medallion of the Shadow Sage.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "KeyItem", "Medallion"],
    value=500,
    customData={"sage": "Impa", "element": "Shadow"}
)

write_item(
    "SpiritMedallion",
    "Spirit Medallion",
    "Medallion",
    "Medallion of the Spirit Sage.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "KeyItem", "Medallion"],
    value=500,
    customData={"sage": "Nabooru", "element": "Spirit"}
)

write_item(
    "LightMedallion",
    "Light Medallion",
    "Medallion",
    "Medallion of the Light Sage.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "KeyItem", "Medallion"],
    value=500,
    customData={"sage": "Zelda", "element": "Light"}
)

# Songs as individual items for Ocarina
songs = [
    ("SongOfTime", "Song of Time", "Opens Door of Time, moves blocks"),
    ("SongOfStorms", "Song of Storms", "Summons rain, reveals secrets"),
    ("EponasSong", "Epona's Song", "Calls Epona, wakes animals"),
    ("SunsSong", "Sun's Song", "Changes day to night, freezes ReDeads"),
    ("ZeldasLullaby", "Zelda's Lullaby", "Opens royal paths, proves identity"),
    ("MinuetOfForest", "Minuet of Forest", "Warps to Forest Temple"),
    ("BoleroOfFire", "Bolero of Fire", "Warps to Fire Temple"),
    ("SerenadeOfWater", "Serenade of Water", "Warps to Water Temple"),
    ("NocturneOfShadow", "Nocturne of Shadow", "Warps to Shadow Temple"),
    ("RequiemOfSpirit", "Requiem of Spirit", "Warps to Spirit Temple"),
    ("PreludeOfLight", "Prelude of Light", "Warps to Temple of Time"),
]

for song_id, song_name, song_desc in songs:
    write_item(
        song_id,
        song_name,
        "Song",
        song_desc,
        damage=0,
        defense=0,
        tags=["Zelda", "Campaign", "Song", "KeyItem"],
        customData={"ocarinaSong": True, "magicCost": 10}
    )

# Important chest loot items
write_item(
    "HeartContainer",
    "Heart Container",
    "Upgrade",
    "Increases max health by 1 heart.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "Upgrade", "ChestLoot"],
    value=200,
    customData={"heartContainers": 1}
)

write_item(
    "PieceOfHeart",
    "Piece of Heart",
    "Upgrade",
    "Collect 4 for a Heart Container.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "Upgrade", "ChestLoot"],
    value=50,
    customData={"heartPieces": 1}
)

write_item(
    "MagicJar",
    "Magic Jar",
    "Consumable",
    "Restores magic power.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "Consumable", "ChestLoot"],
    value=20,
    customData={"magicRestore": 50}
)

write_item(
    "Fairy",
    "Fairy",
    "Consumable",
    "Revives you on death or heals fully.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "Consumable", "ChestLoot"],
    value=100,
    customData={"autoRevive": True, "healAmount": 100}
)

write_item(
    "GoldSkulltula",
    "Gold Skulltula Token",
    "Collectible",
    "Proof of defeating a Gold Skulltula. Collect 100 for a reward.",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "Collectible", "ChestLoot"],
    value=10,
    customData={"skulltulaCount": 1}
)

write_item(
    "BombBag",
    "Bomb Bag",
    "Upgrade",
    "Carry more bombs. (20 -> 30 -> 40)",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "Upgrade", "ChestLoot"],
    value=200,
    customData={"capacity": 30}
)

write_item(
    "Quiver",
    "Quiver",
    "Upgrade",
    "Carry more arrows. (30 -> 40 -> 50)",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "Upgrade", "ChestLoot"],
    value=200,
    customData={"capacity": 40}
)

write_item(
    "Wallet",
    "Adult's Wallet",
    "Upgrade",
    "Carry more Rupees. (200 -> 500 -> 999)",
    damage=0,
    defense=0,
    tags=["Zelda", "Campaign", "Upgrade", "ChestLoot"],
    value=300,
    customData={"capacity": 500}
)

print("\nAll Zelda items generated successfully!")
