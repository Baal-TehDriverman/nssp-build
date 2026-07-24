# Magic & Thaumaturgy

**Sources:** `scripts/magic/msn_magic_system.reds` (936 lines), `scripts/abyssal/msn_abyssal_assets.reds` (728 lines)
**Status:** ✅ FULLY IMPLEMENTED
**Systems:** `MagicSystem`, `MagicRouter`, `SpellEffectManager`, `RitualManager`

---

## Overview

A full magic system with 8 schools of magic, 40+ spells, ritual mechanics, mana management, and overcharge. Integrated with TweakDB for balance tuning.

## Magic Schools

| # | School | Alignment | Keywords |
|---|--------|-----------|----------|
| 1 | Elemental | Neutral | fire, frost, lightning, earth |
| 2 | Necromancy | Dark | life drain, soul harvest, decay |
| 3 | Illusion | Light | phantasm, blinding, shadow dance |
| 4 | Abjuration | Neutral | barrier, nullify, purge, vitality surge |
| 5 | Divination | Light | reveal, foresight, analyze |
| 6 | Enchantment | Light | charm, fury, pacify |
| 7 | Conjuration | Dark | summon, bind, banish |
| 8 | Transmutation | Neutral | morph, enhance, alchemy |

## Spells (40+)

### Elemental
| Spell | Effect |
|-------|--------|
| flamebur | Fire blast |
| icethrower | Frost beam |
| lightningcall | Lightning strike |
| stoneshape | Earth manipulation |
| fireball | AoE fire |
| frostnova | AoE freeze |
| lightningstorm | Multi-target lightning |
| earthquake | AoE earth damage |

### Necromancy
| Spell | Effect |
|-------|--------|
| lifedrain | HP steal |
| soulharvest | Soul fragment extraction |
| decaywave | AoE degeneration |
| bonearmor | Skeletal defense |
| deathgrip | Pull enemy |
| necroticpulse | AoE necrotic damage |

### Illusion
| Spell | Effect |
|-------|--------|
| phantasm | Create illusion |
| blind | Blind target |
| shadowdance | Evasion boost |
| mirrordance | Create decoys |
| noise | Distraction |

### Abjuration
| Spell | Effect |
|-------|--------|
| barrier | Shield |
| nullify | Dispel magic |
| purge | Cleanse debuffs |
| vitalitysurge | Heal |
| spellreflect | Reflect spells |

### Divination
| Spell | Effect |
|-------|--------|
| reveal | Detect hidden |
| foresight | Predict attacks |
| analyze | Scan target |
| threatscan | Threat assessment |

### Enchantment
| Spell | Effect |
|-------|--------|
| charm | Control NPC |
| fury | Enrage |
| pacify | Calm |
| suggestion | Influence |

### Conjuration
| Spell | Effect |
|-------|--------|
| summon | Summon entity |
| bind | Bind entity |
| banish | Banish entity |
| gate | Portal |

### Transmutation
| Spell | Effect |
|-------|--------|
| morph | Transform |
| enhance | Buff |
| alchemy | Craft |
| crystallize | Create crystal |

## Mana System

- **Base mana:** 100 (configurable via TweakDB)
- **Regen:** 5/sec base, modified by skills/cyberware
- **Overcharge:** Spells cost 2x mana when below 10%
- **Spell cost:** Auto-decrements from `mana`, controlled by `StatsSystem`

## Ritual System

Triggers from `msn_ritual_init` fact. Flow:
1. **Initiate** → `msn_ritual_init = 1`
2. **Gather materials** → Check items in inventory
3. **Channel** → Time-based (TweakDB duration)
4. **Complete** → Effect fires, `msn_ritual_active = 0`

Ritual items checked via `TransactionSystem`:
- Check by item category (e.g., `msn_magic_ritual_item`)
- Can specify tag for different ritual types

## Spell Learning

- Learn spells by finding tomes/loot/[[../01-Campaigns/Lilith_Campaign|campaign rewards]]
- Each school has a `learntSpells` tracking array (Int32 mask)
- `LearnSpell(school, spellIndex)` sets the bit
- All spells can also be auto-unlocked via `msn.master.godmode`

## Spell Tree (TweakDB)

```tweakdb
msn.magic.mana.max           = 100.0
msn.magic.mana.regen.base    = 5.0
msn.magic.ritual.duration    = 5.0
msn.magic.overcharge.threshold = 0.1
msn.magic.cast.time          = 1.0
msn.magic.cooldown.global    = 0.5
msn.magic.spell.power.mod    = 1.0
msn.magic.spell.cost.mod     = 1.0
msn.nssp.magic.unlock.cost   = 1000
```

## CET Commands

```lua
msn.magic.status                 -- Magic system status
msn.magic.cast <school> <spell>  -- Cast specific spell
msn.magic.cast <school>          -- Cast default spell for school
msn.magic.schools                -- List all 8 schools
msn.magic.spells <school>        -- List spells for school
msn.magic.ritual                 -- Initiate ritual
msn.magic.learn <school> <spell> -- Learn a specific spell
```

## Integration

- [[../01-Campaigns/Five_Rings_Campaign|Five Rings Earth completion]] unlocks Malkuth Thaumaturgy path
- [[../01-Campaigns/Lilith_Campaign|Lilith Campaign Sovereign Items]] include magic-boosting cyberware
- Hell Campaign rewards include unique spell tomes per circle
- Abyssal covenants grant ritual power bonuses

---

*Reality is a canvas | Sephirotic Court — Tiferet*
