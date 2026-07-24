# Abyssal Assets

**Sources:** `scripts/abyssal/msn_abyssal_assets.reds` (728 lines), `scripts/core/msn_nssp_runtime.reds`
**Status:** ✅ FULLY IMPLEMENTED (12 hat seed, 15 creatures, 10 artifacts, 6 zones, 5 covenants)
**Systems:** `AbyssalAssetManager`, `AbyssalHatCatalog`, `AbyssalCovenantSystem`, `AbyssalNavigationManager`

---

## Overview

The Abyssal Asset system is an NSSP-integrated collection mechanic. Explore 6 underwater zones, catalog creatures, collect artifacts, buy procedurally generated hats, and rise through 5 covenant tiers. Each hat out of 1M possible variants is a unique NFT-class collectible.

## Hat Catalog (Procedural)

**Seed:** 12 | **Total variants:** 1,000,000 (12^6 combinations)

Each hat has 6 component axes:
1. **Style:** Fedora, Top Hat, Beanie, Crown, Beret, Sombrero, Cowboy, Cap, Boater, Headband, Tiara, Fez
2. **Color:** Red, Blue, Green, Gold, Purple, Silver, Cyan, Pink, White, Black, Orange, Teal
3. **Pattern:** Solid, Striped, Polka Dot, Plaid, Camo, Gradient, Holographic, Neon, Glow, Metallic, Matte, Pearl
4. **Brim:** Straight, Curved, Wide, Narrow, No Brim, Upturned, Flared, Flat, Rolled, Pointed, Asymmetrical, Double
5. **Accessory:** Feather, Flower, Gem, Pin, Badge, Ribbon, Chain, Goggles, Patch, Spike, Crystal, None
6. **Enchantment:** None, Glowing, Fire, Frost, Lightning, Poison, Shadow, Holy, Chaos, Time, Soul, Void

### Price tiers
- Common (no enchantment): 10 SC
- Uncommon (basic enchantment): 50 SC
- Rare (elemental enchantment): 250 SC
- Epic (time/soul/void): 1,000 SC
- Legendary (chaos enchantment): 5,000 SC

## Creature Catalog (15)

| ID | Name | Zone | Rarity | Special |
|----|------|------|--------|---------|
| 0 | Abyssal Scout | Shallow | Common | Basic reconnaissance |
| 1 | Gloom Eel | Deep | Common | Poisonous, bioluminescent |
| 2 | Void Jelly | Shallow | Common | Electric shock |
| 3 | Abyssal Serpent | Trench | Rare | Venomous, hypnotic gaze |
| 4 | Abyssal Leviathan | Trench | Epic | Massive AoE attacks |
| 5 | Void Kraken | Abyssal | Epic | Tentacle grab, ink cloud |
| 6 | Crystal Crab | Shallow | Common | Diamond-hard shell |
| 7 | Abyssal Manta | Twilight | Uncommon | Graceful, speed boost |
| 8 | Gloom Leviathan | Deep | Rare | Sonar blast |
| 9 | Void Wyrm | Void | Legendary | Reality warp |
| 10 | Abyssal Phoenix | Gate | Mythic | Resurrection aura |
| 11 | Abyssal Siren | Deep | Uncommon | Mind control song |
| 12 | Abyssal Guardian | Trench | Epic | Shield projection |
| 13 | Void Reaver | Abyssal | Legendary | Dimensional rift |
| 14 | Abyssal Worm | Shallow | Common | Burrow ambush |

## 10 Artifacts

| ID | Name | Zone | Bonus |
|----|------|------|-------|
| 0 | Echo Stone | Shallow | Sonar mapping +20% scan range |
| 1 | Soul Anchor | Twilight | Covenant power +1 |
| 2 | Abyssal Core | Deep | All resistances +10% |
| 3 | Void Crystal | Trench | Damage +15% to abyssal entities |
| 4 | Leviathan Bone | Abyssal | Health +25% |
| 5 | Siren Pearl | Void | Charm resistance +50% |
| 6 | Guardian Plate | Gate | Armor +100 |
| 7 | Phoenix Feather | Gate | Auto-revive 1/combat |
| 8 | Kraken Tentacle | Abyssal | Grab immunity |
| 9 | Wyrm Scale | Void | Elemental resistance +20% |

## Zone Navigation

| Index | Name | Prereq | Depth | Hazards | Enemies |
|-------|------|--------|-------|---------|---------|
| 0 | Shallow | — | 0-20m | None | Scouts, Jellies, Crabs, Worms |
| 1 | Twilight Depths | Shallow cleared | 20-50m | Low pressure | Mantas, Sirens |
| 2 | Deep Reaches | Twilight cleared | 50-150m | Pressure | Eels, Leviathans |
| 3 | Trench | Deep cleared | 150-300m | High pressure, dark | Serpents, Leviathans, Guardians |
| 4 | Abyssal Void | Trench cleared | 300-500m | Extreme pressure | Krakens, Reavers |
| 5 | Abyssal Gate | Void cleared (requires covenant tier 5+) | 500m+ | Reality tears, void exposure | Wyrms, Phoenixes |

## Covenant Tiers

| Tier | Title | Requirement | Benefits |
|------|-------|-------------|----------|
| 0 | Unaffiliated | — | None |
| 1 | Initiate | Visit Shallow | Basic hat purchase, creature scanning |
| 2 | Adept | Collect 3 artifacts + 5 creatures | Survey unlocks, Trench access |
| 3 | Explorer | 5 artifacts + 10 creatures | Abyssal access, rare hat options |
| 4 | Master | 8 artifacts + 12 creatures | Gate access, legendary hat crafting |
| 5 | Abyssal Lord | All artifacts + all creatures | Mythic creature summon, zone teleport |

## CET Commands

```lua
msn.abyssal.status                -- Full abyssal catalog
msn.abyssal.survey <zoneIndex>    -- Survey zone (0-5)
msn.abyssal.buyhat <hatID>        -- Purchase hat by ID
msn.abyssal.auth <zoneIndex>      -- Enter zone (covenant-gated)
msn.abyssal.covenant.upgrade      -- Upgrade covenant tier
msn.abyssal.artifact <artifactID> -- Examine artifact
msn.abyssal.creature <creatureID> -- Examine creature
msn.abyssal.summon <creatureID>   -- Summon creature (tier 5)
msn.abyssal.tp <zoneIndex>        -- Teleport to zone (tier 5)
msn.abyssal.reset_hats            -- Reset hat displays
```

## Integration

- Covenant tiers grant bonuses that affect [[../01-Campaigns/Hell_Campaign|Hell biome]] resistance
- Hat enchantments interact with [[../02-Systems/Magic_Thaumaturgy|magic system]] (fire hat + fire spells)
- [[Lochness_Monster|Nessie]] is found in Twilight Depths zone
- [[Economy|NSSP token economy]] used for all purchases
- Abyssal creatures can be summoned in [[../01-Campaigns/Lilith_Campaign|Lilith campaign]] areas

---

*1M hats, 1 ocean, ∞ covenants | Sephirotic Court — Yesod*
