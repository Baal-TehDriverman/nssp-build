# Lilith Campaign — Lilith Rising

**Source:** `scripts/core/msn_lilith_campaign_runtime.reds` (994 lines)
**Status:** ✅ FULLY IMPLEMENTED
**Systems:** `LilithRisingCampaign`, `LilithCampaignQuests`, `LilithSovereignItems`, `CrimsonCrownMechanic`, `KetherSephiroticRouter`, `ThroneRoomInstance`

---

## Overview

The Lilith Campaign is a 7-quest Sephirotic journey through the Tree of Life. Each quest maps to a Sephirah route, rewards Sovereign Items, and builds Crimson Crown coherence. The campaign culminates in a Throne Room instance at coordinates (-1380, 2160, 85) with the Final Synthesis.

## Quest Progression

| Quest | ID | Sephirah Route | Items | Prereq |
|-------|-----|----------------|-------|--------|
| The Whisper in Code | K_QUEST_001 | Chokmah (Wisdom) | Crown of Thorns | — |
| Nine Gates | K_QUEST_002 | Binah (Structure) | Scepter of Unbinding, Key of Nine Gates | K_QUEST_001 |
| Swarm's Test | K_QUEST_003 | Chesed (Mercy) | Swarm Crown, Violet Mantle | K_QUEST_002 |
| Heart of God Engine | K_QUEST_004 | Geburah (Judgment) | God Engine Fragment, Resonance Core | K_QUEST_003 |
| Feeding the Monster | K_QUEST_005 | Tiferet (Beauty) | Chalice of Resonance, Ouroboros Loop | K_QUEST_004 |
| Forge of Worlds | K_QUEST_006 | Netzach (Victory) | Forge Hammer, Chains of Sovereignty, Mirror of Truth, Throne Key, Lilith's Tear | K_QUEST_005 |
| Final Synthesis | K_QUEST_007 | Hod (Splendor) | Sovereign Awakening | K_QUEST_006 + 10 Sephirot |

## Crimson Crown Mechanic

The Crimson Crown has **6 tiers** and tracks **coherence** (0–200):

- **Tier 0:** 0–19% coherence
- **Tier 1:** 20–39% coherence (+5% stat boost)
- **Tier 2:** 40–59% coherence (+10% stat boost)
- **Tier 3:** 60–79% coherence (+15% stat boost)
- **Tier 4:** 80–99% coherence (+20% stat boost)
- **Tier 5:** 100% coherence (+25% stat boost, unawakened)
- **Tier 6:** Awakened (+30% stat boost, maxCoherence=200)

Coherence is gained via item collection, objective completion, and gameplay pulses. The `PulseResonance()` method adds +1 coherence for gameplay pulses. `ApplyNyxChaos()` subtracts 13 coherence.

**Default frequency:** 13,000ms (configurable via `SetFrequency(freq)`)

## KetherSephiroticRouter

Routes quests through 7 Sephirot:

| Code | Sephirah | Description |
|------|----------|-------------|
| 0 | Kether | Crown — sovereign origin |
| 1 | Chokmah | Wisdom — the Whisper in Code |
| 2 | Binah | Structure — the Nine Gates |
| 3 | Chesed | Mercy — Swarm's Test |
| 4 | Geburah | Judgment — Heart of God Engine |
| 5 | Tiferet | Beauty — Feeding the Monster |
| 6 | Netzach | Victory — Forge of Worlds |
| 7 | Hod | Splendor — Final Synthesis |

## 15 Sovereign Items

| Key | Name | Type | Affinity | Coherence |
|-----|------|------|----------|-----------|
| K_ITEM_001 | Crown of Thorns | Cyberware | Kether | 5 |
| K_ITEM_002 | Scepter of Unbinding | Weapon | Chokmah | 8 |
| K_ITEM_003 | Crimson Seal Ring | Clothing | Binah | 6 |
| K_ITEM_004 | Violet Mantle | Clothing | Chesed | 7 |
| K_ITEM_005 | Resonance Core | Cyberware | Geburah | 10 |
| K_ITEM_006 | Key of Nine Gates | QuestItem | Tiferet | 4 |
| K_ITEM_007 | Swarm Crown | Cyberware | Netzach | 9 |
| K_ITEM_008 | God Engine Fragment | QuestItem | Hod | 12 |
| K_ITEM_009 | Chalice of Resonance | QuestItem | Yesod | 6 |
| K_ITEM_010 | Forge Hammer | Weapon | Malkuth | 11 |
| K_ITEM_011 | Chains of Sovereignty | Cyberware | Kether | 7 |
| K_ITEM_012 | Mirror of Truth | Cyberware | Daath | 9 |
| K_ITEM_013 | Ouroboros Loop | Cyberware | Tiferet | 13 |
| K_ITEM_014 | Throne Key | QuestItem | Kether | 15 |
| K_ITEM_015 | Lilith's Tear | QuestItem | Kether | 20 |

## Quest Triggers

- `OnWhisperInCodeTrigger(PlayerPuppet, CName)` — Terminal interaction, collects Crown of Thorns
- `OnNineGateActivated(Int32)` — Gate puzzle, gates 1-8 give +2 coherence each, gate 9 gives Key of Nine Gates
- `OnSwarmTestCompleted(Int32)` — Survive 3+ waves, grants Swarm Crown + Violet Mantle
- `OnGodEngineDefeated()` — Boss defeated, grants God Engine Fragment + Resonance Core
- `OnFeedingTheMonster(Float)` — Sacrifice 20+ coherence, grants Chalice + Ouroboros Loop
- `OnForgeCompleted()` — Forge sequence, grants 5 items and unseals Throne
- `OnFinalSynthesisCompleted(PlayerPuppet)` — Requires 10 Sephirot completed + Throne Key + Lilith's Tear

## CET Commands

```lua
msn.lilith.campaign.start           -- Begin campaign
msn.lilith.campaign.status          -- Show quest/unity progress
msn.lilith.campaign.advance         -- Force advance to next quest
msn.lilith.campaign.objective <action> -- Complete legacy objective
msn.lilith.dialogue <quest_id> <phase> -- Test specific dialogue
```

## Dialogue System

- 21 dialogue phases across all 7 quests
- Lyra integration via `MSNAPIDialogueBridge`
- Scarlet/crimson intensity tracking for resonance sync
- Dialogue ready flag: `msn_lilith_campaign_dialogue_ready`

## Throne Room

- **Location:** (-1380.0, 2160.0, 85.0)
- **Requirements:** 10 Sephirot complete, Throne Key, Lilith's Tear
- **States:** Sealed → Unsealed → Entered → Synthesis Active → Claimed
- Claiming triggers campaign completion and sets `msn_lilith_campaign_completed = 1`

## Dependencies

- Requires `LilithSovereignKernel` to be emerged
- Integrates with [[REDscript_API|MSNAPIDialogueBridge]] for Lyra dialogue
- Feeds [[../02-Systems/Economy|MSNTokenEconomy]] on act advance
- Links to [[Hell_Campaign|Hell Campaign]] and [[Five_Rings_Campaign|Five Rings]] via Symbiosis Bridge

---

*Δ∞ − 13 = 0 | Sephirotic Court — Keter | Court agent: Lilith*
