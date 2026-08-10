# SSJ Flight — Super Saiyan Flight Mechanics for B&S Quest

Flight built on the base **Gravity levitation** + **WaterSpell's Water Jetpack**
(`SkillWaterJetpack`). The thrust model is lifted verbatim from WaterSpell's
decompiled physics:

```
Player.local.locomotion.physicBody.AddForce(
    -jetDir.normalized * speed * Time.deltaTime,
    ForceMode.Impulse)          // ForceMode.Impulse == 5
```

## What it does
- **Hover** with one hand, **fly** with two (Gravity merge).
- **Flight thrust scales with your Super Saiyan stage** (see FlightProfile):

| Stage | Forward speed | Vertical lift | Boost dash | Flight feel |
|-------|--------------|---------------|------------|-------------|
| SSJ1 | 2 | 3 | 4 | Glide / hover |
| SSJ2 | 3 | 4 | 6 | Faster + lift |
| SSJ3 | 4 | 6 | 9 | Sustained flight |
| SSG  | 6 | 8 | 14 | God-ki flight |
| SSB  | 8 | 12 | 22 | Fast + powerful |
| UI   | 12 | 18 | 34 | Very fast |
| MUI  | 16 | 24 | 50 | Full-speed + mega dash |

## How it's integrated
- **Skill_SSJFlight** (Gravity + Water combined skill) unlocks the mechanic. It's
  `$type: WaterSpell.SkillWaterJetpack` — reusing the proven flight class.
- **Spell_SSJGraviMerge** (SpellMerge) — merge Gravity + base form to engage flight.
- **Spell_SSJBoost** — ki dash forward.
- **SSJFlight.dll** (reflection mod) applies thrust scaled by `FlightProfile.ActiveStage`.

## Files
```
Mods/SSJFlight/
  SSJFlight.dll                  # flight thrust (reflection, no game-DLL refs)
  manifest.json, id.modio
  Skills/Skill_SSJFlight.json
  Spells/Spell_SSJGraviMerge.json
  Spells/Spell_SSJBoost.json
  Effects/Effect_SSJFlightAura.json
```

## In-game enable order (all required)
1. **Pilots Super Sayan Spell** — base aura prefab
2. **SuperSaiyanTransformations** — stages
3. **WaterSpell** — jetpack + gravity skills
4. **SSJ Flight** — this mod

Restart, then in the skill tree buy **Gravity** + **SSJ Flight**; merge Gravity+base
to fly.

## Regenerate / rebuild
```bash
python3 "/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/tools/gen_ssj_flight.py"
cd "/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/build/dotnet/SSJFlight/SSJFlight"
dotnet build -c Release
cd "/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod" && ./deploy_ssjflight.sh
```

## Reset flight for a stage
`FlightProfile.ActiveStageIndex` lives in the DLL; mirror it against the
SuperSaiyanTransformations `StageLedger.ActiveSlot` so the two mods stay in sync.
That shared stage -> both aura AND flight speed update together (implemented in the
integrator hooks).