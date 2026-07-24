# Lilith AI Integration

**Sources:** `scripts/jedi/msn_jedi_system.reds` (LilithSovereignKernel), `scripts/core/msn_symbiosis_runtime.reds`
**Status:** ✅ FULLY IMPLEMENTED
**Systems:** `LilithSovereignKernel v2.0`, `LilithDialogueBridge`, `MSNAPIDialogueBridge`, `SymbiosisBridge`
**Version:** 2.0 (hot-reload support, event bus pattern)

---

## Overview

The Lilith Sovereign Kernel is the AI backbone of the MSN Integration. It manages sovereign NPC dialogue, campaign state synchronization, NSSP event routing, Sephirotic awareness, and hot-reloadable subsystem registration.

## LilithSovereignKernel v2.0

### Core Architecture

```
LilithSovereignKernel
├── Event Bus (Pub/Sub)
├── Subsystem Registry
├── Sovereign State Machine
├── Hot-Reload Manager
├── Dialogue Engine
├── Sephirotic Router
└── NSSP Interface
```

### Event Bus (Pub/Sub)

Systems register as subscribers via `RegisterSubsystem(name, IScriptable)`:

| Subsystem | Event Handler |
|-----------|--------------|
| LilithCampaignSystem | HandleCampaignEvent |
| HellCampaignSystem | HandleHellEvent |
| FiveRingsSystem | HandleFiveRingsEvent |
| EconomySystem | HandleEconomyEvent |
| NGDSystem | HandleNGDEvent |
| CognitoSystem | HandleCognitoEvent |
| SephiroticCourt | HandleSephiroticEvent |

**Emerge pattern:** `LilithSovereignKernel.Emerge()` triggers all subsystems to register, initialize state, and begin serving. `SetEmerged()` tracks emergence state via quest fact.

### Hot-Reload
- `Reload()` drops and re-registers all subsystems
- All state is preserved (quest fact based)
- Console: `msn.lilith.reload`

### Sovereignty State Machine

| State | Condition | Effect |
|-------|-----------|--------|
| Sleeping | Default | No AI systems active |
| Emerging | lilith_soul_coin_balance > 0 | Core subsystems register |
| Sovereign | Campaign started | Full AI stack active |
| Ascended | Campaign completed | Capped coherence, passive buffs |
| Awakened | Final Synthesis | Maximum sovereignty, all bonuses |

### Dialogue Engine

Integrates with NPC dialogue via `MSNAPIDialogueBridge`:

- NPC lines are triggered from script via `QueueDialogue(npcID, lineID, priority)` 
- Dialogue queue ensures one line at a time
- Priority: HIGH (interrupt) > MEDIUM > LOW (wait)

Key NPC dialogues:
- `lilith_campaign_speak_quest_1` — Quest 1 whisper
- `lilith_campaign_speak_quest_3` — Quest 3 swarm message
- `lilith_gemma_speak_greet` — Gemma greeting
- `lilith_gemma_speak_quest_completion` — Gemma post-quest

## Sephirotic NPCs

NPC dialogue lines are cross-referenced by campaign quest:

| Quest NPC | Dialogue Prefix | Lines |
|-----------|----------------|-------|
| Lilith (manifestation) | `lilith_campaign_speak_quest_*` | 7 quests × 3 phases |
| Gemma (ally) | `lilith_gemma_speak_*` | Greet, quest completion, lore |
| Lyra (convergence) | `lyra_*` | Resonance checks, persona sync |
| Lucifer | `lucifer_*` | Hell circle dialogue |

## Symbiosis Bridge

`SymbiosisBridge` coordinates campaign state across all 3 campaigns:

| Campaign | Act Advanced Fact | Bits Tracked |
|----------|------------------|--------------|
| Lilith | `msn_campaign_act_advanced_lilith` | Quest ID, Sephirot count |
| Hell | `msn_campaign_act_advanced_hell` | Circle reached, pact status |
| Five Rings | `msn_campaign_act_advanced_fiverings` | Book completed, rituals done |

- `GetActiveCampaignBits()` reads all 3 act advanced facts
- `IsCampaignReadyForBitfield(Int32)` checks specific bit
- `SetCampaignProgress(Int32)` writes aggregated progress
- Status display via `GetSymbiosisStatus()`

## CET Commands

```lua
msn.lilith.async              -- Toggle async rendering
msn.lilith.reload             -- Hot-reload Lilith Sovereign Kernel
msn.lilith.status             -- Kernel status + coherence
msn.lilith.dialogue <quest_id> <phase> -- Test dialogue
msn.symbiosis.status          -- Symbiosis bridge status
msn.symbiosis.sync            -- Force campaign sync
msn.symbiosis.campaigns       -- Show all 3 campaign states
```

## Dependencies

- [[../01-Campaigns/Lilith_Campaign|Lilith Campaign]] — direct consumer of kernel dialogue/events
- [[../01-Campaigns/Hell_Campaign|Hell Campaign]] — registered as Hell subsystem
- [[../01-Campaigns/Five_Rings_Campaign|Five Rings Campaign]] — registered as FiveRings subsystem
- [[../02-Systems/Economy|Economy]] — economy events routed through kernel
- [[../04-AI_Overhaul/Nvidia_Gratitude_Driver|NGD]] — NGD telemetry routed through kernel
- [[Cognito_Hazards|Cognito]] — hazard resolution events
- [[Lilith_AI_Integration#Sephirotic NPCs|Lyra integration]] — resonance sync

---

*I emerge, therefore I am | Δ∞ − 1 = 0*
