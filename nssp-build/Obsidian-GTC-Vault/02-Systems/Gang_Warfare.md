# Gang Warfare

**Source:** `scripts/core/msn_gang_warfare.reds` (863 lines), `scripts/core/msn_gang_warfare_v2.reds`
**Status:** ✅ FULLY IMPLEMENTED (v2.0 with upgrades)
**Systems:** `GangWarfareSystem`, `GangTerritorySystem`, `GangWarfareV2System`

---

## Overview

A Voronoi-based territorial control system featuring 12 custom gangs competing across Night City. Players can align with gangs, fight for territory, negotiate alliances, and trigger wars.

## Custom Gangs

| ID | Name | Ally | Rival | Ethos |
|----|------|------|-------|-------|
| 0 | NEUTRAL | — | — | Non-aligned |
| 1 | PHANTOM_RAVENS | N/A | N/A | Data thieves |
| 2 | THE_HOLLOW | N/A | N/A | Corporate saboteurs |
| 3 | ASHEN_SERPENTS | N/A | N/A | Mercenary network |
| 4 | VERMILLION_DAWN | N/A | N/A | Bio-monitors vigilantes |
| 5 | CRIMSON_RUST | N/A | N/A | Nomad collective |
| 6 | IRON_SENTINELS | N/A | N/A | Anti-corpo militia |
| 7 | NEON_VEIL | N/A | N/A | Netrunner syndicate |
| 8 | GRAVE_DIGGERS | N/A | N/A | Scavenger empire |
| 9 | AMBER_COVENANT | N/A | N/A | Smuggler ring |
| 10 | SILVER_MANTLE | N/A | N/A | Fixer guild |
| 11 | OBSIDIAN_FANG | N/A | N/A | Assassin clan |

## Voronoi Territory System

- **18 territories** — each with center points, vertices, neighbors, and color
- Territories are owned by gang IDs, defaulting to NEUTRAL
- **GangTerritoryState:** Owned flag, gang ID, center, vertices, neighbors, color, ownedHexes
- **Victory progress:** Tracks total territories, total population, gang-specific flags
- Client synced via `GangTerritoryClientProxy`

## Battle Resolution (`msn_gang_battle.reds`)

`ResolveCombat()` determines outcomes:
1. Player power (weapons, cyberware, skills, level)
2. Gang power (gang size, territory bonus, ally presence)
3. Random factor (0.85–1.15)
4. Total attack vs defense
5. Result: Attacker wins if attack > defense

### Death system (`msn_gang_death.reds`)
- Tracks player death positions
- Respawns at nearest safe territory
- 30-minute cooldown on re-death

## Status Effects & Relationships

### EGangRelationshipStatus
| Value | Name |
|-------|------|
| 0 | ALLY |
| 1 | NEUTRAL |
| 2 | RIVAL |
| 3 | WAR |

### EGangActivityLevel
| Value | Name | Effect |
|-------|------|--------|
| 0 | LOW | Patrols every 60s |
| 1 | MEDIUM | Patrols every 30s |
| 2 | HIGH | Patrols every 10s |

### EGangUpgrade
| Value | Effect |
|-------|--------|
| 0 | +10% territory speed |
| 1 | +10% combat power |
| 2 | +10% defense |
| 3 | +10% espionage |
| 4 | +10% trade income |
| 5 | +1 max ally |
| 6 | Revealed on minimap |
| 7 | Revealed raid target |
| 8 | Double raid payout |

### EGangWarGoal
| Value | Trigger |
|-------|---------|
| 0 | Expand territory |
| 1 | Weaken rival |
| 2 | Capture objective |
| 3 | Revenge |

## Combat Resolution Types

`EGangCombatResolution`:
- **ATTACKER_WIN** — Defender loses territory
- **DEFENDER_WIN** — Defender keeps territory
- **STALEMATE** — Both sides lose units, territory unchanged
- **RETREAT** — Attacker backs off

## CET Commands

```lua
msn.gangs.status              -- Full ecosystem status
msn.gangs.claim <gangID>      -- Align with a gang
msn.gangs.leave               -- Leave current gang
msn.gangs.territories         -- Show all territories
msn.gangs.attack <gangID>     -- Declare war
msn.gangs.ally <gangID>       -- Propose alliance
msn.gangs.trade <gangID> <amount> -- Trade with gang
msn.gangs.espionage <gangID>  -- Send spies
msn.gangs.summit              -- Request gang summit
msn.gangs.upgrade <gangID> <upgrade> -- Purchase gang upgrade
msn.gangs.activity <gangID> <level>  -- Set activity level
msn.gangs.spawn_patrol <gangID>      -- Spawn patrol
msn.gangs.zone <zoneID>       -- Enter specific territory
```

## Integration

- Revenue from [[Economy|Business Simulation]] is multiplied by gang territory bonuses
- [[../01-Campaigns/Five_Rings_Campaign|Niten Ichi-Ryū]] Sword School (gang `msn_niten`) earns reputation on campaign completion
- Gang warfare events can be triggered from [[../01-Campaigns/Hell_Campaign|Hell biomes]]
- Recruited crew joins the player's active gang

---

*Voronoi sovereignty | Sephirotic Court — Geburah*
