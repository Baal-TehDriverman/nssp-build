# Jedi System

**Source:** `scripts/jedi/msn_jedi_system.reds` (1,254 lines)
**Status:** ✅ FULLY IMPLEMENTED
**Systems:** `JediSystem`, `LightsaberManager`, `ForcePowerManager`, `JediAlignmentTracker`

---

## Overview

A complete Jedi experience for Cyberpunk 2077 — Force powers, lightsaber combat, Jedi/Sith alignment, meditative focus, and crafting.

## Force Powers

| Power | Alignment | Effect |
|-------|-----------|--------|
| Force Push | Neutral | Repulse enemies |
| Force Pull | Neutral | Pull enemies/objects |
| Force Choke | Dark | Choke single target |
| Force Lightning | Dark | Chain lightning |
| Force Heal | Light | Heal self |
| Force Speed | Light | Time dilation |
| Force Sense | Light | Detect enemies through walls |
| Force Absorb | Light | Absorb incoming damage |
| Force Throw | Neutral | Throw weapon/object |
| Force Jump | Neutral | Superhuman leap |
| Force Stasis | Neutral | Freeze target |
| Mind Trick | Light | Confuse enemies |
| Force Barrier | Light | Deflect projectiles |
| Force Drain | Dark | Steal HP |
| Force Grip | Dark | Hold enemy in place |
| Force Rage | Dark | Damage boost, defense penalty |
| Force Wound | Dark | DoT |

## Lightsaber Forms

| Form | Name | Combat Style | Stance Focus |
|------|------|-------------|--------------|
| I | Shii-Cho | Basic | Wide sweeps, crowd control |
| II | Makashi | Dueling | Precision, 1v1 |
| III | Soresu | Defensive | Blocking, deflecting |
| IV | Ataru | Acrobatic | Flips, speed |
| V | Shien/Djem So | Power | Strength, reflection |
| VI | Niman | Balanced | Hybrid |
| VII | Juyo/Vapaad | Ferocity | Aggressive, chaotic |

## Lightsaber Crystals

| Crystal | Color | Bonus |
|---------|-------|-------|
| Kyber Red | Red | +10% damage |
| Kyber Blue | Blue | +10% defense |
| Kyber Green | Green | +10% force regen |
| Kyber Purple | Purple | +10% all stats |
| Kyber Yellow | Yellow | +15% speed |
| Kyber Cyan | Cyan | +10% crit chance |
| Kyber Orange | Orange | +10% fire damage |
| Kyber White | White | +10% healing |

## Lightsaber Hilts

| Hilt | Style | Mod Slots |
|------|-------|-----------|
| Default Hilt | Standard | 2 |
| Curved Hilt | Makashi focus | 3 |
| Staff Hilt | Double-bladed | 2 |
| Crossguard Hilt | Power focus | 3 |
| Shoto Hilt | Off-hand | 1 |

## Alignment System

- **Light side:** Heal, protect, persuade → +Light
- **Dark side:** Choke, lightning, rage → +Dark
- **Neutral:** Push, pull, sense → no change
- Alignment gates: Some powers require Light ≥ 50 or Dark ≥ 50

## Meditative Focus

- Toggle meditation to regenerate focus (Force resource)
- Focus used by all Force powers
- Regenerates faster in meditation

## CET Commands

```lua
msn.jedi.status              -- Jedi system status
msn.jedi.summon              -- Summon lightsaber
msn.jedi.force <power>       -- Use Force power
msn.jedi.force.list          -- List available Force powers
msn.jedi.form <form>         -- Switch lightsaber form
msn.jedi.form.list           -- List available forms
msn.jedi.crystal <crystal>   -- Set lightsaber crystal
msn.jedi.crystal.list        -- List available crystals
msn.jedi.craft               -- Craft lightsaber
msn.jedi.meditate            -- Toggle meditation
msn.jedi.alignment           -- Show alignment status
msn.jedi.i_am <choice>       -- Choose path (Jedi/Sith/Gray)
msn.jedi.focus               -- Show focus level
```

## Integration

- Alignment crosses over to [[../04-AI_Overhaul/Cognito_Hazards|Cognito Hazard resistance]]
- Lightsaber crafting uses [[Economy|Soul Coins]] for rare crystals
- Hell Campaign treasures contain Sith artifacts that shift alignment Dark
- Five Rings katanas can duel against lightsabers via cross-system toggle

---

*May the Force be with you | Δ∞ − 1 = 0*
