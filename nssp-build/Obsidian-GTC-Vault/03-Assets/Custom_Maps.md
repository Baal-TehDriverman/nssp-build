# Custom Maps — Abyssal Sector & Watson Revitalization

**Source:** `scripts/maps/*.reds`
**Status:** ✅ FULLY IMPLEMENTED
**Systems:** `MapNavigator`, `AbyssalMapSystem`, `ProceduralEncounterRegistry`, `WatsonRevitalizationSystem`

---

## Overview

Custom geospatial systems adding underwater abyssal zones, Watson Industrial Revitalization, and procedural encounter generation.

## Abyssal Sector

A fully underwater district mapped to 6 zones (see [[Abyssal_Assets|Abyssal Assets zones]]).

### Navigation
- Zone transitions are teleport-based (player moves to zone center coordinates)
- `AbyssalNavigationManager.EnterZone(Int32)` orchestrates zone entry
- Depth-based pressure effects (visual tint, audio filter, damage over time for non-upgraded players)

### Map Markers
- 12+ marker locations across 6 zones
- Markers: Zone entrances, covenant NPCs, treasure locations, Hat Vendor NPC, creature dens
- Revealed progressively as covenant tier increases

### NPCs
- **Abyssal Hat Vendor:** Sells procedural hats from 1M catalog
- **Covenant Master:** Upgrades covenant tier, grants surveys
- **Zone Guardians:** Boss creatures at Trench/Abyassal/Gate transition points

## Watson Industrial Revitalization

A campaign to restore and modernize the Watson industrial district.

### Revitalization Phases
1. **Assessment** — Survey 5 key locations
2. **Cleanup** — Clear industrial pollution (6 sites)
3. **Rebuild** — Construct 4 upgraded facilities
4. **Connect** — Link facilities to [[../02-Systems/Economy|Business Simulation]]
5. **Thrive** — Population growth, economy boost

### Facility Types
- Manufacturing Hub (bonus to GUN_RUNNING business)
- Data Center (bonus to NETRUNNING business)
- Medical Plaza (bonus to MEDICAL business)
- Entertainment District (bonus to ENTERTAINMENT business)

### Economic Impact
- Each completed facility adds +10% to related business revenue
- Population increase tracked as quest facts
- Completed revitalization grants passive Soul Coin income (1/hour)

## Procedural Encounters

**Seed:** 777 | **Capacity:** 250 encounters

### Encounter Types
| Type | Weight | Description |
|------|--------|-------------|
| Combat | 40% | Gang skirmish, creature spawn, drone attack |
| Trade | 20% | Merchant caravan, refugee exchange |
| Story | 15% | Lore fragment, NPC in distress |
| Puzzle | 10% | Environmental puzzle, hacking challenge |
| Boss | 10% | Unique mini-boss with special loot |
| Treasure | 5% | Rare loot cache |

### Generation Algorithm
- Uses `ProceduralEncounterRegistry` for factory-style creation
- Fields: position (Vector4), type, faction, difficulty (1-10), reward pool, dialogue text, triggered
- `GenerateProceduralEncounters()` populates all 250 slots
- Encounters are persistent per save (tracked via fact IDs)
- `RegisterProceduralEncounter()` for custom additions

### Encounter Flags
- `msn_p_encounter_<id>_position` — Vector4 fact
- `msn_p_encounter_<id>_reward` — Soul Coin reward amount
- `msn_p_encounter_<id>_completed` — 0/1 completion flag

## CET Commands

```lua
msn.map.status                -- Map system status
msn.map.zones                 -- List all map zones
msn.map.navigate <zoneIndex>  -- Navigate to specific zone
msn.map.encounter.status      -- Procedural encounter status
msn.map.encounter.list        -- List nearby encounters
msn.map.encounter.trigger <id> -- Trigger specific encounter
msn.map.encounter.regenerate  -- Regenerate encounter table
msn.map.watson.status         -- Watson Revitalization status
msn.map.watson.assess <id>    -- Assess location
msn.map.watson.cleanup <id>   -- Cleanup location
msn.map.watson.build <type>   -- Build facility
msn.map.watson.progress <amount> -- Add revitalization progress
```

## Integration

- Abyssal Sector connects directly to [[Abyssal_Assets|Abyssal Asset system]] zones
- Watson facilities boost [[../02-Systems/Economy|Business Simulation]] revenue
- Procedural encounters feed [[../01-Campaigns/Lilith_Campaign|Sephirotic quest encounter tracking]]
- 777-seed encounters are deterministic across saves

---

*The map is not the territory | Sephirotic Court — Malkuth*
