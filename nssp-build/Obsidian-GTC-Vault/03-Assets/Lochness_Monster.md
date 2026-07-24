# Loch Ness Monster

**Source:** `scripts/abyssal/msn_lochness_monster.reds` (571 lines)
**Status:** ✅ FULLY IMPLEMENTED
**Systems:** `LochNessMonsterSystem`, `LochNessFriendship`, `LochNessTreasury`

---

## Overview

A friendship-based companion system. Track sightings, build trust, earn treasury marks, sea-scan for hidden treasures, and eventually unlock Nessie as a rideable mount in abyssal zones.

## Friendship Tiers

| Tier | Title | Trust Required | Benefits |
|------|-------|---------------|----------|
| 0 | Stranger | — | Nessie flees |
| 1 | Acquaintance | 100 | Nessie approaches, sighting log |
| 2 | Friend | 500 | Follows player, marks 1st treasure |
| 3 | Close Friend | 1500 | Sea-scan unlocked, rideable | 
| 4 | Companion | 3000 | Full combat assist, telepathic link |
| 5 | Bonded | 5000 | Summon anywhere, treasury access |

## Sighting Locations (7)

| Location | Coordinates | Frequency |
|----------|-------------|-----------|
| Shallow NW | (-500, 2000, -15) | Common |
| Twilight Ridge | (-300, 1800, -35) | Common |
| Deep Basin | (0, 1500, -80) | Uncommon |
| Trench Wall | (200, 1200, -160) | Uncommon |
| Abyssal Plain | (500, 800, -320) | Rare |
| Void Rift | (800, 400, -500) | Rare |
| Gate of the Deep | (1000, 0, -600) | Very Rare |

### Sighting Mechanics
- Random cooldown between sightings (60-180 min real time)
- Current zone + friendship tier affect spawn chance
- `OnSighting(Int32)` tracks total sightings count
- Each sighting awards trust points
- Rare sightings (Void Rift, Deep Gate) grant bonus trust

## Trust Mechanics

Primary trust gains:
- **Sighting:** +20-100 trust (scales with zone rarity)
- **Feeding:** +50 trust (uses fish items from inventory)
- **Grooming:** +30 trust (cleansing cyberware)
- **Playing:** +40 trust (sonar ping game)
- **Treasury Mark redemption:** +500 trust (once per week)

## Treasury Marks

- Hidden treasure chests in abyssal zones
- Only visible after Friend tier (tier 2+)
- Map revealed on Close Friend tier (tier 3)
- Contains: Soul Coins, rare abyssal items, cosmetic rewards
- Tracked via `msn_nessie_treasure_marks` quest fact

## Sea-Scan Ability

- Unlocked at Friend tier (tier 3)
- Scans surroundings for hidden treasures
- Highlighted items on minimap
- Consumes 20 mana (from [[../02-Systems/Magic_Thaumaturgy|magic system]])

## Combat Assist

- Unlocked at Companion tier (tier 4)
- Nessie surfaces to attack enemies near water
- Attack types: Tail Slap (AoE), Water Jet (ranged), Lullaby (stun)
- Scales with friendship tier

## Summon

- Unlocked at Bonded tier (tier 5)
- `msn.nessie.summon` — spawn Nessie anywhere she can path
- Valid in: Shallow, Twilight, Deep zones (locked in Trench+ due to depth)
- Follows player for 60 seconds, then despawns

## CET Commands

```lua
msn.nessie.status              -- Nessie covenant status
msn.nessie.sighting            -- Record a sighting (manual)
msn.nessie.feed                -- Feed Nessie from inventory
msn.nessie.groom               -- Groom Nessie
msn.nessie.play                -- Play with Nessie
msn.nessie.scan                -- Sea-scan for treasures
msn.nessie.mark <markID>       -- Check specific treasury mark
msn.nessie.treasures           -- List all found treasures
msn.nessie.summon              -- Summon Nessie (tier 5)
msn.nessie.come                -- Call Nessie to player
msn.nessie.flee                -- Dismiss Nessie
msn.nessie.whisper             -- Telepathic message (tier 4)
msn.nessie.callback <data>     -- Internal event callback
```

## Interaction Rules

- `EFishInteractionRule`: FRIENDLY (tier 1) triggers approach animation
- `EFishFeedingRule`: FEEDABLE after tier 1
- `EScanningRule`: SCANNABLE after tier 0 (always visible)
- `EFishGroomingRule`: GROOMABLE after tier 2
- `EFishPlayingRule`: PLAYABLE after tier 3

## Integration

- Sightings tracked in [[Abyssal_Assets|Abyssal zone]] exploration data
- Treasury marks contribute to [[Economy|Soul Coin]] farming
- Combat assist in water zones for [[../01-Campaigns/Hell_Campaign|Hell campaign]] 
- Bonded tier reward links to [[../02-Systems/Magic_Thaumaturgy|water magic]] buffs

---

*Love is the deepest ocean | Sephirotic Court — Chesed*
