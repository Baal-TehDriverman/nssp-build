# Lilith B&S Quest Mod Stack — Complete Working System

Everything in this repo is deployed and loadable on the Quest 3S. This document
is the single source of truth for the full stack.

## The 3 custom mods (deployed to Quest)

### 1. ZeldaCampaign — "Blade of Hyrule" campaign (54 files)
A full Zelda campaign, now **playable** as a WaveAssault gauntlet.

| Piece | Location | Status |
|-------|----------|--------|
| Campaign data (9 dungeons, 9 bosses, 37 items, 8 locations) | `Resources/campaign_data.json` | ✅ |
| Playable campaign level | `Levels/Level_ZeldaCampaign.json` | ✅ NEW playable |
| 9 dungeon gauntlet waves (scal 3→11 enemies) | `Waves/Wave_ZeldaDungeon_0..8.json` | ✅ NEW playable |
| Mod code (items/enemies/campaign/harmony) | `Scripts/*.cs` | ✅ |
| UI assets | `TextureAssets/UI/*.png` (37) | ✅ |
| Compiled mod | `ZeldaCampaign.dll` | ✅ |

In-game: select **"Zelda Campaign"** level → pick a dungeon wave on the **Cell
Games** arena → fight escalating themed gauntlets → Ganon's Castle finale.

### 2. SuperSaiyanTransformations — 7-stage Saiyan system (35 files)
| Piece | Status |
|-------|--------|
| 7 stages ×2→×100, real DM JSONs (DamageModifier_x) | ✅ |
| Per-stage auras (lithosphere-refined spectral/subsurface colors) | ✅ |
| 7 spells + Kamehameha + Big Bang + MUI items/spells | ✅ |
| 6 native SpellMerge transitions (Water/BlackFire/SSJ combos) | ✅ |
| `SuperSaiyan.dll` (stage ledger + IT hook), `SuperSaiyanKi.dll` (IT teleport) | ✅ |

### 3. SSJFlight — stage-synced flight (7 files)
| Piece | Status |
|-------|--------|
| `Skill_SSJFlight` (Gravity+Water hybrid, reuses WaterSpell jetpack class) | ✅ |
| `Spell_SSJGraviMerge` (merge to engage flight), `Spell_SSJBoost` (dash) | ✅ |
| `SSJFlight.dll` — thrust scales with active stage (mirrors SuperSaiyan StageLedger) | ✅ |

## Integrated engine stack (what makes it all work)

The **lithosphere-ref** WebGPU shader library informs the VFX color science:
- `createSubsurfaceScattering` (wrap-glowing light) → our aura `mainColorStart/End`
- `createSpectralDispersion` (rainbow fire) → SSJ gold spectral shift
- `createAnimatedSpectralFire` → Kamehameha/Big Bang energy

These map to B&S's `EffectModuleParticle` color fields at the JSON level — no raw
shader compilation needed on Quest (it's IL2CPP).

## Enable/in-game order (all required for full synergy)
1. **Pilots Super Sayan Spell** (base aura prefab)
2. **WaterSpell** (jetpack + lightning/water merge hooks)
3. **BlackFire** / **WhiteFire** (fire merge hooks)
4. **DBmapPackNOMAD** (Cell Games arena — the campaign/SSJ map)
5. **ZeldaCampaign** (Blade of Hyrule campaign)
6. **SuperSaiyanTransformations** (stages + ki + merges)
7. **SSJFlight** (flight)

Restart B&S. Buy Gravity+SSJ Flight in skill tree; merge to fly/transform.

## Regenerate / rebuild / redeploy
```bash
MOD="/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod"
# JSON generators
python3 $MOD/tools/gen_super_saiyan.py        # 7 stages
python3 $MOD/tools/gen_ssj_flight.py          # flight
python3 $MOD/tools/gen_ki_attacks.py          # kamehameha/bigbang
python3 $MOD/tools/gen_spell_merges.py        # merge transitions
python3 $MOD/tools/gen_zelda_campaign_level.py # campaign level
python3 $MOD/tools/gen_zelda_campaign_levels.py # dungeon waves
# DLL builds (dotnet, no Unity)
cd $MOD/build/dotnet && for p in SuperSaiyan/SuperSaiyanIntegrator SuperSaiyanKi/SuperSaiyanKi SSJFlight/SSJFlight; do (cd $p && dotnet build -c Release); done
# Deploy
./deploy_all.sh   # then push waves/levels explicitly (see below)
```

## Honest notes
- **Zelda dungeon waves** reference base-game `CreatureTable` containers
  (HumansBandit/Soldier/Mage/Cultist/Knight). Confirm these table IDs exist in
  your B&S 1.3.1 install; if a category is missing, swap it in the Wave JSON.
- The **MUI Instant Transmission** (forehead-touch lock-on teleport), the
  **SpellMerge gestures**, and flight thrust are runtime reflection against the
  IL2CPP game — structurally follow the working WaterSpell/DestructoDisc
  precedents but need a one-time in-headset test to confirm the exact pose/merge
  trigger registration.
- **Unity 2021.3 LTS + Android Build Support** would still let us replace the
  text-lite arena waves with true bespoke dungeon scenes + asset bundles. Not
  required for the current playable campaign.
- **SoH (gigachad quest)** full OOT-MQ needs a real RAROM to boot; current
  `OG/*.z64` is a 133-byte LFS stub. Our B&S campaign is the playable path.