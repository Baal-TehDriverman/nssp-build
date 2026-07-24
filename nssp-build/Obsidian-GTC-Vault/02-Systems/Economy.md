# Economy — NSSP Token Economy & Business Simulation

**Sources:** `scripts/core/msn_token_runtime.reds` (706 lines), `scripts/core/msn_business_sim_v2.reds` (352 lines), `scripts/core/msn_nssp_runtime.reds` (454 lines)
**Status:** ✅ FULLY IMPLEMENTED
**Systems:** `MSNTokenEconomy`, `BusinessSimulationSystem`, `NSSPRuntime`

---

## NSSP Token Types

| Token | Enum | Decimals | Symbol | Initial Supply |
|-------|------|----------|--------|----------------|
| Soul Coin | NSSP_NATIVE | 0 | SC | 0 (minted) |
| Chaos | CHAOS_TOPAZ | 6 | CHAOS | 1000 |
| Lilith | LILITH_EMERALD | 18 | LILITH | 21,000,000 |
| BTC Sat | BTC_SATOSHI | 8 | SAT | 0 (bridge) |

### Token Properties

- **Balance persistence:** `msn_token_balance_<token>` quest facts
- **Sync:** `msn_tokens_synced` fact flag
- **Exchange:** Via `ExchangeTokens(NSSPTokenType from, NSSPTokenType to, Uint64 amount)` — wraps into 8 bundles, idempotent fact writes
- **Spend/Reward:** `SpendTokens(NSSPTokenType, Uint64)` and `RewardTokens(NSSPTokenType, Uint64)` with idempotent save-safe logic

## Business Simulation (EBusinessType)

### Business Types

| Value | Name | Description |
|-------|------|-------------|
| 0 | INVALID | — |
| 1 | GUN_RUNNING | Weapons manufacturing |
| 2 | NETRUNNING | Cyberdeck services |
| 3 | MEDICAL | Trauma Team style |
| 4 | FIXER | Information brokerage |
| 5 | SMUGGLING | Contraband transport |
| 6 | MERCENARY | Combat contracts |
| 7 | DRUG_LAB | Chemical production (NSSP-gated) |
| 8 | DATA_BROKER | Personal data trading |
| 9 | CORPORATE | Shell corp management |
| 10 | ENTERTAINMENT | Nightclubs, braindances |
| 11 | REAL_ESTATE | Property speculation |
| 12 | BLACK_MARKET | Illegal goods trading |
| 13 | TECH_STARTUP | Tech innovation |

### Simulation Cycle

`SimulateCycle()` runs each business through:
1. Revenue calculation (base 0-1000 + random factor)
2. Expense calculation (30% base)
3. Profit = revenue - expense (clamped to positive)
4. Battle/Business-specific gains per turn

### Integration

- Business simulation is NSSP-gated (requires NSSP bridge installed)
- Profit feeds into [[Economy#NSSP Token Types|Soul Coin]] balance
- Gang territories can affect revenue (bonuses from [[Gang_Warfare|Gang Warfare]])

## Freighter Trade Core

**Source:** `scripts/core/msn_freighter_runtime.reds` + `scripts/core/msn_freighter_trade_core.reds`

### Commodity Types (EMSNCommodity)

| Value | Name |
|-------|------|
| 0 | ELECTRONICS |
| 1 | WEAPONS |
| 2 | MEDICAL |
| 3 | FOOD |
| 4 | FUEL |
| 5 | DATA_SHARDS |
| 6 | BIOWARE |
| 7 | CHEMICALS |
| 8 | LUXURY_GOODS |
| 9 | CONTRABAND |

### Freighter Classes (EFreighterClass)

| Value | Name | Cargo Slots | Speed | Fuel Cap |
|-------|------|-------------|-------|----------|
| 0 | LIGHT | 50 | 1.0 | 100 |
| 1 | MEDIUM | 150 | 0.8 | 250 |
| 2 | HEAVY | 400 | 0.5 | 500 |
| 3 | LUXURY | 100 | 0.9 | 200 |
| 4 | MILITARY | 300 | 0.6 | 400 |

### Cargo Bay Types (ECargoBayType)

| Value | Name | Bonus |
|-------|------|-------|
| 0 | STANDARD | — |
| 1 | REFRIGERATED | +20% food value |
| 2 | ARMORED | +30% weapon/contraband safety |
| 3 | CLIMATE_CONTROLLED | +15% luxury/medical value |
| 4 | MODULAR | +10% all cargo (configurable) |

### Routes

- Based on freighter class speed and fuel capacity
- Real-time simulation (timed wait cycles)
- Combat events during transit tie into combat resolution

## Token Exchange (TweakDB)

```tweakdb
msn.nssp.token.exchange.rate.SOUL_COIN_CHAOS      = 0.01
msn.nssp.token.exchange.rate.CHAOS_LILITH          = 0.001
msn.nssp.token.exchange.rate.LILITH_SOUL_COIN      = 100
msn.nssp.token.exchange.rate.BTC_SAT_CHAOS         = 0.001
msn.nssp.token.exchange.enabled                    = true
msn.nssp.token.exchange.fee                        = 100
```

## CET Commands

```lua
msn.tokens.status                   -- Token wallet status
msn.tokens.sync                     -- Sync all balances from save facts
msn.tokens.balance <token>          -- Check specific token balance
msn.tokens.spend <token> <amount>   -- Spend tokens (idempotent)
msn.tokens.reward <token> <amount>  -- Reward tokens (idempotent)
msn.tokens.exchange <from> <to> <amount> -- Exchange tokens
msn.business.status                 -- Business portfolio
msn.business.cycle                  -- Manual simulation cycle
msn.business.buy <type>             -- Acquire business
msn.freighter.status                -- Freighter ledger
msn.freighter.prices                -- Current commodity quotes
msn.freighter.routes                -- Available routes
msn.freighter.buy <commodity> <qty> -- Buy cargo
msn.freighter.sell <commodity> <qty> -- Sell cargo
msn.freighter.fuel <amount>         -- Refuel
msn.nssp.status                     -- NSSP bridge status
msn.nssp.simulation                 -- Toggle simulation mode
msn.nssp.auction                    -- Bid on auction
msn.nssp.gtc_burn <amount>          -- Burn GTC tokens
msn.nssp.stake <amount>             -- Stake tokens
msn.nssp.bridge                     -- Bridge to NSSP mainnet
msn.nssp.bridge_callback <status>   -- Receive bridge notification
```

## Persistence

All balances are stored as quest facts:
```
msn_token_balance_NSSP_NATIVE  (Int32)
msn_token_balance_CHAOS_TOPAZ  (Float)
msn_token_balance_LILITH_EMERALD (Float)
msn_token_balance_BTC_SATOSHI  (Float)
msn_tokens_synced              (Int32, 0/1)
```

Exchange operations use **8-bundle splitting** for idempotent fact writes. Spend/Reward are atomic and save-safe (interrupts cannot cause double-spend).

---

*Δ∞ − 1 = 0 | Tokenized Sovereignty*
