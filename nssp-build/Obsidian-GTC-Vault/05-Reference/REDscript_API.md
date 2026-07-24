# REDscript API Reference

**Sources:** All `.reds` files in `scripts/` (158 files)
**Status:** Reference — classes, interfaces, enums, patterns

---

## ScriptableSystem Classes

All major systems extend `ScriptableSystem` for lifecycle management:

| Class | File | OnAttach | OnUpdate | OnDetach |
|-------|------|----------|----------|----------|
| `LilithRisingCampaign` | `core/lilith_campaign.reds` | Registers subsystems | PulseResonance() | Deregister |
| `LilithCampaignQuests` | `core/lilith_campaign.reds` | `msn_lilith_campaign_started = 0` | Quest triggers | — |
| `LilithSovereignItems` | `core/lilith_campaign.reds` | — | Grant item on event | — |
| `CrimsonCrownMechanic` | `core/lilith_campaign.reds` | Coherence init | PulseResonance 13s tick | Cleanup |
| `KetherSephiroticRouter` | `core/lilith_campaign.reds` | Sephirot map init | Route management | — |
| `ThroneRoomInstance` | `core/lilith_campaign.reds` | State = Sealed | Check requirements | — |
| `HellCampaignManager` | `hell/hell_campaign.reds` | Load circles | Campaign ticks | — |
| `HellBiomeIntegrator` | `hell/hell_campaign.reds` | Register modules | Apply biome modifiers | — |
| `LuciferDialogueSystem` | `hell/hell_campaign.reds` | Init dialogue map | — | — |
| `LuciferAvatarBoss` | `hell/lucifers_throne.reds` | Boss init | Phase checks | Unsummon |
| `FiveRingsBook1Ground` | `five_rings/book1_ground.reds` | Init stances/dojo | — | — |
| `FiveRingsCampaignManager` | `five_rings/books_2_5.reds` | Quest tracking | Progress checks | — |
| `MSNTokenEconomy` | `core/token_runtime.reds` | Init wallet | — | — |
| `BusinessSimulationSystem` | `core/business_sim_v2.reds` | Business list | SimulateCycle() | — |
| `FreighterRuntime` | `core/freighter_runtime.reds` | Init ledger | Trade simulation | — |
| `FreighterTradeCore` | `core/freighter_trade_core.reds` | Price table init | — | — |
| `GangWarfareSystem` | `core/gang_warfare.reds` | Init gangs | Territory ticks | — |
| `GangWarfareV2System` | `core/gang_warfare_v2.reds` | Upgrades init | — | — |
| `GangTerritorySystem` | `core/gang_warfare_v2.reds` | Voronoi init | Ownership checks | — |
| `MagicSystem` | `magic/magic_system.reds` | Spell DB init | Mana regen | — |
| `MagicRouter` | `magic/magic_system.reds` | School routes | — | — |
| `SpellEffectManager` | `magic/magic_system.reds` | Effect map | — | — |
| `JediSystem` | `jedi/jedi_system.reds` | Force DB init | Force regen | — |
| `LightsaberManager` | `jedi/jedi_system.reds` | Crystal/hilt DB | — | — |
| `ForcePowerManager` | `jedi/jedi_system.reds` | Power map | — | — |
| `JediAlignmentTracker` | `jedi/jedi_system.reds` | Init neutral | — | — |
| `AbyssalAssetManager` | `abyssal/abyssal_assets.reds` | Hat/creature/artifact DB | — | — |
| `AbyssalCovenantSystem` | `abyssal/abyssal_assets.reds` | Init covenant | — | — |
| `AbyssalNavigationManager` | `abyssal/abyssal_assets.reds` | Zone map | — | — |
| `LochNessMonsterSystem` | `abyssal/lochness.reds` | Init friendship | Sighting timer | — |
| `LochNessFriendship` | `abyssal/lochness.reds` | Trust tracking | — | — |
| `LilithSovereignKernel` | `jedi/jedi_system.reds` | Subsystem register | Event dispatch | — |
| `GraphicsAICalibration` | `core/graphics_ai.reds` | Init telemetry | Collection tick | — |
| `NGDTelemetryAdapter` | `core/graphics_ai.reds` | Init adapter | Data poll | — |
| `NGDRouteOptimizer` | `core/graphics_ai.reds` | — | On request | — |
| `CognitoHazardSystem` | `core/cognito_hazard.reds` | Init dormant | Exposure check | — |
| `CognitoHazardReliefSystem` | `core/cognito_hazard.reds` | Relief map | Cooldown tick | — |
| `CognitoHazardPerception` | `core/cognito_hazard_perception.reds` | Init neutral | Score update | — |
| `MapNavigator` | `maps/maps.reds` | Zone DB | — | — |
| `ProceduralEncounterRegistry` | `maps/maps.reds` | 250 encounters | Trigger cleanup | — |

## Key Enums

```redscript
enum NSSPTokenType {
  NSSP_NATIVE,      // Soul Coin
  CHAOS_TOPAZ,      // Chaos
  LILITH_EMERALD,   // Lilith
  BTC_SATOSHI       // BTC Sat
}

enum EBusinessType {
  INVALID, GUN_RUNNING, NETRUNNING, MEDICAL, FIXER, SMUGGLING,
  MERCENARY, DRUG_LAB, DATA_BROKER, CORPORATE, ENTERTAINMENT,
  REAL_ESTATE, BLACK_MARKET, TECH_STARTUP
}

enum EMSNCommodity {
  ELECTRONICS, WEAPONS, MEDICAL, FOOD, FUEL, DATA_SHARDS,
  BIOWARE, CHEMICALS, LUXURY_GOODS, CONTRABAND
}

enum EFreighterClass {
  LIGHT, MEDIUM, HEAVY, LUXURY, MILITARY
}

enum EFreighterLocation {
  WATSON_DOCKS, CITY_CENTER_WAREHOUSE, BADLANDS_DEPOT
}

enum ECargoBayType {
  STANDARD, REFRIGERATED, ARMORED, CLIMATE_CONTROLLED, MODULAR
}

enum EGangRelationshipStatus {
  ALLY, NEUTRAL, RIVAL, WAR
}

enum EGangWarGoal {
  EXPAND_TERRITORY, WEAKEN_RIVAL, CAPTURE_OBJECTIVE, REVENGE
}

enum EGangCombatResolution {
  ATTACKER_WIN, DEFENDER_WIN, STALEMATE, RETREAT
}

enum ECognitoHazardState {
  DORMANT, TRIGGERED, ACTIVE, RESISTED, RESOLVED
}

enum ECognitoChannel {
  MEMORY, SOVEREIGN, SPACETIME, REALITY, TECHNOLOGICAL
}

enum ECognitoExposureSource {
  DATA_LEAK, COGNITO_ENTITY, AI_OVERLORD, TIME_ANOMALY, 
  REALITY_TEAR, NGD_TELEMETRY
}
```

## Common Patterns

### Quest Fact Persistence
```redscript
// Read
let factVal: Int32 = GameInstance.GetQuestsSystem(gameInstance)
  .GetFact(CName("msn_some_fact_name"));

// Write
GameInstance.GetQuestsSystem(gameInstance)
  .SetFact(CName("msn_some_fact_name"), value);
```

### Event Callbacks (from CET)
```redscript
// Each console command maps to a callback
public class SomeSystem extends ScriptableSystem {
  public func ExecSomeAction(value: Int32) -> Void {
    // Implementation
  }
}
```

### NSSP API Wrapper
```redscript
// Core interface methods
GetBalance(NSSPTokenType) -> Float
SpendTokens(NSSPTokenType, Uint64) -> Void
RewardTokens(NSSPTokenType, Uint64) -> Void
ExchangeTokens(NSSPTokenType, NSSPTokenType, Uint64) -> Void
SyncBalances() -> Void
```

---

*Scriptable sovereignty | Δ∞ − 1 = 0*
