# Freighter Space

**Source:** `scripts/core/msn_freighter_runtime.reds` (587 lines), `scripts/core/msn_freighter_trade_core.reds`
**Status:** ✅ FULLY IMPLEMENTED
**Systems:** `FreighterRuntime`, `FreighterTradeCore`, `FreighterLedger`

---

## Overview

A virtual cargo trading system. Buy low, sell high across 3 Night City locations. Manage cargo, fuel, and route timing.

## Freighter System

### Freighter Classes (EFreighterClass)

| Class | Slots | Speed | Fuel Cap | Buy Cost |
|-------|-------|-------|----------|----------|
| LIGHT | 50 | 1.0 | 100 | $50,000 |
| MEDIUM | 150 | 0.8 | 250 | $200,000 |
| HEAVY | 400 | 0.5 | 500 | $500,000 |
| LUXURY | 100 | 0.9 | 200 | $150,000 |
| MILITARY | 300 | 0.6 | 400 | $350,000 |

### Cargo Bay Types (ECargoBayType)

| Type | Cost | Bonus |
|------|------|-------|
| STANDARD | $10,000 | — |
| REFRIGERATED | $25,000 | +20% food value |
| ARMORED | $50,000 | +30% weapon/contraband safety |
| CLIMATE_CONTROLLED | $35,000 | +15% luxury/medical |
| MODULAR | $75,000 | +10% all cargo |

### Locations (EFreighterLocation)

| Value | Name |
|-------|------|
| 0 | WATSON_DOCKS |
| 1 | CITY_CENTER_WAREHOUSE |
| 2 | BADLANDS_DEPOT |

### 10 Commodities (EMSNCommodity)
ELECTRONICS, WEAPONS, MEDICAL, FOOD, FUEL, DATA_SHARDS, BIOWARE, CHEMICALS, LUXURY_GOODS, CONTRABAND

## Trade Loop

1. **Acquire freighter** — Choose class + cargo bay
2. **Check prices** — Each location has different buy/sell prices
3. **Buy cargo** — Must have fuel and available cargo slots
4. **Travel** — Timed routes between locations (fuel consumption)
5. **Sell cargo** — Profit from price differences
6. **Refuel** — Fuel is consumed per route unit

### Route Simulation
- **Real-time based:** Routes take real wall time (configurable via TweakDB)
- `StartRoute()` initiates timed journey
- `CompleteRoute()` triggers arrival events
- Combat during transit is possible

## Freighter Ledger

Tracks all financial activity:
- **Total profit:** From all completed trades
- **Total trades:** Count of completed buy/sell cycles
- **Commodities traded:** Per-commodity breakdown
- **Best run:** Highest single-run profit
- Persisted via `questFactService`

## CET Commands

```lua
msn.freighter.status              -- Freighter ledger
msn.freighter.prices              -- Current commodity quotes
msn.freighter.routes              -- Available routes
msn.freighter.buy <commodity> <qty> -- Buy cargo
msn.freighter.sell <commodity> <qty> -- Sell cargo
msn.freighter.fuel <amount>       -- Refuel
msn.freighter.start <from> <to> <commodity> <qty> -- Full route
msn.freighter.callback <data>     -- Route result callback
msn.freighter.trade <commodity> <qty> -- Execute trade
```

## Integration

- Prices fluctuate based on [[Gang_Warfare|Gang Warfare]] activity in territory
- [[../01-Campaigns/Hell_Campaign|Hell campaign Greed circle]] has special market events with boosted prices
- NSSP [[Economy|Token Economy]] can be exchanged for freighter funds

---

*Trade routes of the sovereign | Sephirotic Court — Netzach*
