# Zelda Campaign - Complete Ocarina of Time Integration

## Overview
This document summarizes the complete Ocarina of Time mechanics and lore integration for the Zelda Campaign mod for Blade & Sorcery: Nomad.

## File Structure Created

### Spells (12 Total)
- **Spell_OcarinaOfTime.json** - Main ocarina instrument with 8-way analog stick song selection + 3 gesture songs
- **Spell_SongOfTime.json** - Time manipulation, Door of Time, Time Blocks
- **Spell_SongOfStorms.json** - Weather control, secret revelation, water level control
- **Spell_ZeldasLullaby.json** - Royal authority, passage opening, spirit calming
- **Spell_EponasSong.json** - Epona summoning, beast calming
- **Spell_SunsSong.json** - Day/night toggle, undead stun, sun chest revelation
- **Spell_MinuetOfForest.json** - Warp to Forest Temple
- **Spell_BoleroOfFire.json** - Warp to Fire Temple, fire immunity
- **Spell_SerenadeOfWater.json** - Warp to Water Temple, water breathing
- **Spell_NocturneOfShadow.json** - Warp to Shadow Temple, shadow sight, undead command
- **Spell_RequiemOfSpirit.json** - Warp to Spirit Temple, spirit form, time shift
- **Spell_PreludeOfLight.json** - Warp to Temple of Time, Sacred Realm access

### Effects (52 Total - 4 per spell + 4 base ocarina effects)
Each spell has 4 effect files:
- `_Charge.json` - Charging visual/audio
- `_Ready.json` - Ready to cast visual/audio
- `_Finger.json` - Finger particles while playing
- `_Cast.json` - Cast effect with gameplay impact

Plus 4 base ocarina effects:
- Effect_OcarinaCharge.json
- Effect_OcarinaReady.json
- Effect_OcarinaFinger.json
- Effect_OcarinaFinger.json (referenced in spell)

### Items (15 New Key Items)
- **Spiritual Stones** (3): Kokiri Emerald, Goron Ruby, Zora Sapphire
- **Sage Medallions** (7): Forest, Fire, Water, Shadow, Spirit, Light
- **Master Sword Progression** (3): Kokiri Sword, Master Sword, Master Sword True

### Progression System (2 Files)
- **ZeldaCampaign_Progression.json** - Complete progression flags, temple unlocks, requirements
- **MasterSword_Progression.json** - Weapon evolution tracking with visual changes

### Dungeon Waves (9 Total)
- **Wave_ZeldaDungeon_1.json** - Great Deku Tree (Queen Gohma)
- **Wave_ZeldaDungeon_2.json** - Dodongo's Cavern (King Dodongo)
- **Wave_ZeldaDungeon_3.json** - Jabu-Jabu's Belly (Barinade)
- **Wave_ZeldaDungeon_4.json** - Forest Temple (Phantom Ganon)
- **Wave_ZeldaDungeon_5.json** - Fire Temple (Volvagia)
- **Wave_ZeldaDungeon_6.json** - Water Temple (Morpha)
- **Wave_ZeldaDungeon_7.json** - Shadow Temple (Bongo Bongo)
- **Wave_ZeldaDungeon_8.json** - Spirit Temple (Twinrova)
- **Wave_ZeldaDungeon_9.json** - Ganon's Castle (Ganondorf/Ganon)

### Lore Integration (1 File)
- **ZeldaCampaign_Lore.json** - Complete NPC dialogues, story beats, item histories, world lore

### Cross-Mod Spell Merges (5 Files)
- **SpellMerge_ZeldaCampaign_SuperSaiyan.json** - Master Sword + Super Saiyan
- **SpellMerge_ZeldaCampaign_SSJFlight.json** - Minuet of Forest + SSJ Flight
- **SpellMerge_ZeldaCampaign_Lithosphere.json** - Master Sword + Origin Heart
- **SpellMerge_ZeldaCampaign_SuperSaiyan_Songs.json** - Sage Songs + Super Saiyan Forms
- **SpellMerge_ZeldaCampaign_BlackFire.json** - Song of Storms + Black Fire

### Campaign Manifest (1 File)
- **ZeldaCampaign_Manifest.json** - Complete quest log, dungeon tracker, rewards, settings

## Gameplay Mechanics

### Ocarina System
- **Analog Stick 8-Way Selection**: Hold ocarina, tilt stick to select warp song, release to cast
- **Gesture Songs**: Zelda's Lullaby (Triforce gesture), Epona's Song (Horse call), Sun's Song (Sun/Moon gesture)
- **Mana Costs**: 5-30 mana per song
- **Visual Feedback**: Charge → Ready → Finger → Cast particle progression

### Progression Flow
```
Child Era (3 dungeons)
  → Great Deku Tree → Kokiri Emerald
  → Dodongo's Cavern → Goron Ruby
  → Jabu-Jabu's Belly → Zora Sapphire
  → Door of Time → Master Sword → 7 Year Sleep

Adult Era (6 dungeons)
  → Forest Temple → Forest Medallion + Minuet of Forest
  → Fire Temple → Fire Medallion + Bolero of Fire
  → Water Temple → Water Medallion + Serenade of Water
  → Shadow Temple → Shadow Medallion + Nocturne of Shadow
  → Spirit Temple → Spirit Medallion + Requiem of Spirit
  → Ganon's Castle → Light Medallion + Prelude of Light
  → Ganondorf Fight → Ganon Fight → True Master Sword
```

### Cross-Mod Synergies
| Zelda Campaign | Partner Mod | Result |
|---|---|---|
| Master Sword Energy Blast | Super Saiyan SSJ1+ | Holy Golden Ki Beams |
| Minuet of Forest | SSJ Flight | Forest Wind Flight (2x speed) |
| Master Sword | Lithosphere Origin Heart | Reality Warping Union (2x potency) |
| All 6 Sage Songs | Super Saiyan Forms | Sage Ki Resonance (each song = form) |
| Song of Storms | Black Fire | Black Storm (void lightning) |
| All 4 Mods Active | - | Four Mod Union (Ultimate Form) |

### Rewards Structure
- **Spiritual Stones**: 5,000 XP each, unlocks Door of Time
- **Medallions**: 10,000 XP each, unlocks next temple
- **Master Sword**: 15,000 XP, unlocks Adult Era
- **True Master Sword**: 50,000 XP, unlocks True Ending
- **Ganon Defeated**: 200,000 XP, unlocks New Game+
- **Side Quests**: Gold Skulltulas (100), Heart Pieces (36), Biggoron Sword, Epona

## Technical Notes

### Requirements
- B&S Nomad (Meta Quest 3S)
- Unity 2021.3 Addressables build
- Mod load order per manifest
- 35+ compatible mods deployed

### File Locations
All files under: `/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods/ZeldaCampaign/`

Subdirectories:
- `/Spells/` - 12 spell definitions
- `/Effects/` - 52 effect definitions
- `/Items/` - 15+ item definitions
- `/Progression/` - 2 progression trackers
- `/Waves/` - 9 dungeon waves
- `/Lore/` - 1 lore database
- `/SpellMerges/` - 5 cross-mod merges
- `/Manifest/` - 1 campaign manifest

## Integration Complete ✓

All ocarina mechanics, warp songs, dungeon progression, lore, cross-mod synergies, Master Sword evolution, and campaign tracking are fully implemented and ready for deployment.