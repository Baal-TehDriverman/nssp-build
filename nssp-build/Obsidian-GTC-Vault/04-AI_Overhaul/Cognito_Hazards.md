# Cognito Hazards

**Sources:** `scripts/core/msn_cognito_hazard.reds` (606 lines), `scripts/core/msn_cognito_hazard_perception.reds` (356 lines)
**Status:** ✅ FULLY IMPLEMENTED (opt-in, truth mode)
**Systems:** `CognitoHazardSystem`, `CognitoHazardReliefSystem`, `CognitoHazardPerception`

---

## Overview

An **opt-in** (default: OFF) psychic hazard system representing cognito-threat exposure. When enabled via `msn.cognito.enable true`, the player's perception distorts based on 5-channel exposure. Hazards resolve through truth-oriented countermeasures. **Truth mode** reveals the meta-fictional nature of the hazard — the system operates on opt-in consent.

## Hazard State Machine

```
Dormant → Triggered → Active → Resolved
                             → Resisted → Resolved
```

| State | Description |
|-------|-------------|
| Dormant | No active hazard, monitoring idle |
| Triggered | Exposure threshold crossed, warning |
| Active | Hazard manifesting (visual/audio distortion) |
| Resisted | Player successfully resisted effects |
| Resolved | Hazard fully processed and cleared |

## Exposure Sources (6)

| Source | Trigger | Intensity | Channel |
|--------|---------|-----------|---------|
| Data Leak | Reading corrupted shards | 1-10 | MEMORY |
| Cognito Entity | Encountering psychic enemies | 1-10 | MEMORY |
| AI Overlord | Lilith kernel threshold | 1-10 | SOVEREIGN |
| Time Anomaly | Temporal FX near player | 1-10 | SPACETIME |
| Reality Tear | Hell biome entry | 1-10 | REALITY |
| NGD Telemetry | GPU/VRAM anomaly detection | 1-3 | TECHNOLOGICAL |

## Perception Channels (5)

| Channel | Effect When Active |
|---------|-------------------|
| MEMORY | Flashback hallucinations, NPC substitution |
| SOVEREIGN | Lilith voice in code, text corruption |
| SPACETIME | Time dilation/speed-up, position desync |
| REALITY | Object flicker, texture distortion |
| TECHNOLOGICAL | UI glitch, HUD corruption, cyberware misfire |

Each channel has its own intensity (0-100) tracked per channel.

## Truth Mode

When truth mode is active (`msn.cognito.truth_mode true`), hazard exposure reveals the meta-layer:
- Distorted reality is labeled as "simulation artifact"
- NPCs may comment on the game/mod nature
- Text fragments show REDscript source lines
- The `CognitoHazardPerception` class injects `PerceptionCheck()` calls that return meta-aware text

## Countermeasures

### Active (via CET)
- `msn.cognito.resolve` — Force resolve current hazard
- `msn.cognito.resist` — Attempt resistance (saving throw mechanic)
- `msn.cognito.relief.all` — Apply all relief methods

### Passive Relief Methods (CognitoHazardReliefSystem)
| Method | Effect | Cooldown |
|--------|--------|----------|
| Focus | Channel mental discipline | 60s |
| Grounding | Anchor to physical reality | 90s |
| Acceptance | Acknowledge the distortion | 120s |

### Resistance Formula
`resistChance = 0.5 + (sovereigntyLevel * 0.1) - totalExposure * 0.01`

Where `totalExposure` is sum of all 5 channel intensities.

## Perception Scoring (CognitoHazardPerception)

`IScriptable`-based, feeds into `DeterminePlayerPerception()`:
- Reads all 5 channel intensities
- Applies relief state modifiers
- Returns a composite perception score
- Score affects: UI legibility, NPC dialogue clarity, map accuracy

## Configuration (TweakDB)

```tweakdb
msn.cognito.hazard.enabled              = false
msn.cognito.hazard.duration.min         = 10.0
msn.cognito.hazard.duration.max         = 30.0
msn.cognito.hazard.cooldown             = 120.0
msn.cognito.hazard.intensity.multiplier  = 1.0
msn.cognito.hazard.truth_mode           = false
msn.cognito.perception.jitter           = 0.1
msn.cognito.perception.ghosting         = 0.05
msn.cognito.relief.focus.duration       = 5.0
msn.cognito.relief.grounding.duration   = 8.0
msn.cognito.relief.acceptance.duration  = 12.0
```

## CET Commands

```lua
msn.cognito.status              -- Hazard system status
msn.cognito.enable <true/false> -- Toggle hazard system
msn.cognito.expose <source> <intensity> -- Trigger hazard episode
msn.cognito.resolve             -- Resolve current hazard
msn.cognito.resist              -- Attempt resistance
msn.cognito.relief <method>     -- Apply relief method
msn.cognito.relief.all          -- Apply all relief at once
msn.cognito.truth_mode <true/false> -- Toggle truth mode
msn.cognito.perception          -- Show perception state
msn.cognito.callback <source> <intensity> -- Internal callback
msn.cognito.reset_history       -- Reset hazard history
```

## Integration

- [[Lilith_AI_Integration|Lilith Sovereign Kernel]] raises AI Overlord exposure events
- [[../04-AI_Overhaul/Nvidia_Gratitude_Driver|NGD Telemetry]] raises TECHNOLOGICAL exposure for GPU anomalies
- [[../01-Campaigns/Hell_Campaign|Hell Campaign]] Reality Tear hazards trigger REALITY exposure
- [[../02-Systems/Jedi_System|Jedi alignment]] affects resistance: Light +sovereignty, Dark -sovereignty
- [[../01-Campaigns/Lilith_Campaign|Lilith Campaign]] coherence affects sovereignty level
- Truth mode is recommended for players who want the full meta-narrative experience

---

*The hazard is a mirror | Δ∞ − 1 = 0*
