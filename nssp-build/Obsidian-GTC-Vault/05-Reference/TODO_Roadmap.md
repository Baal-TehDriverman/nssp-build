# TODO & Roadmap

**Source:** `CYBERPUNK_MOD_TODO.md` (execution ledger, 72 tasks)
**Version:** 1.2.2
**Status:** ✅ All P0-P1 complete, 56 scripts deployed, 238 tests pass

---

## Completed (v1.2.2)

### AI & Integration
- [x] Lilith Sovereign Kernel v2.0 — hot-reload, event bus
- [x] Lilith Knowledge Integration — LilithData.txt + Training Data.txt
- [x] Symbiosis Bridge campaign state sync
- [x] Lyra dialogue bridge (21 dialogue phases)
- [x] Gemma NPC dialogue integration
- [x] Sephirotic Court alignment (10 agent routing)
- [x] NSSP Bridge (local simulation mode)
- [x] Ouroboros Loop encounter recording
- [x] Cerebellum / Speculative Cerebellum groundwork

### Campaigns
- [x] Lilith Rising — 7 quests, 15 sovereign items, Crimson Crown (6 tiers)
- [x] Hell Campaign — 11 circles, Lucifer 4-phase boss
- [x] Five Rings — 5 books, 200 protocols, 10 Baba rituals, Niten Ichi-ryū

### Economy
- [x] Token Economy (4 tokens, exchange, spend/reward)
- [x] Freighter Trade (3 locations, 10 commodities, 5 classes)
- [x] Business Simulation (14 types, cycle/revenue)
- [x] NSSP Runtime (bridge, simulation, auction, stake)

### Combat
- [x] Gang Warfare (12 gangs, 18 territories, battle resolution)
- [x] Magic System (8 schools, 40+ spells, rituals, mana)
- [x] Jedi System (17 Force powers, 7 forms, 8 crystals, alignment)

### World
- [x] Abyssal Assets (1M hats, 15 creatures, 10 artifacts, 6 zones)
- [x] Loch Ness Monster (6 friendship tiers, 7 sighting locations)
- [x] Custom Maps (Abyssal Sector, Watson Revitalization)
- [x] Procedural Encounters (250, seed 777)
- [x] Hell Biomes (11 modules, biome integrator)
- [x] Hell Enemy Archetypes (Goetia, Chthonic, etc.)

### AI Overhaul
- [x] Nvidia Gratitude Driver (RNN+CNN pipeline, telemetry, route opt)
- [x] Cognito Hazard System (6-state, 5 channels, truth mode, opt-in)
- [x] Graphics AI Calibration (recommendation-only)
- [x] NGD Telemetry (VRAM/FPS/GPU monitoring)

### Infrastructure
- [x] 238 script validations — all PASS
- [x] Load order validation — 56 scripts, 0 conflicts
- [x] CET adapter contract — all commands registered
- [x] v1.2.2 release — Lilith Knowledge Integration + NGD

---

## P0 — Next Release

### Crime Syndicate (`scripts/core/msn_crime_syndicate.reds`)
- [ ] Racketeering system — 5 crime families, turf, extortion
- [ ] Heist planning — crew recruitment, blueprint theft, execution
- [ ] Faction reputation — influence, favors, betrayal

### Drone Swarms (`scripts/core/msn_drone_swarms.reds`)
- [ ] Deployable drone squadrons — recon, attack, medic
- [ ] Drone crafting — chassis, weapons, AI core
- [ ] Swarm tactics — formation, sync attack, override

### Endgame Loop
- [ ] Territory persistence — post-campaign gang dynamics
- [ ] Throne Room repeatable — weekly reset with scaling rewards
- [ ] Ng+ scaling — enemy level scaling, loot multiplier

---

## P1 — Short Term

### Elemental Weapons (`scripts/core/msn_elemental_weapons.reds`)
- [ ] 40+ elemental weapon mods (fire/frost/shock/void)
- [ ] Proc chains — combo effects between elements
- [ ] Infusion system — craft elemental ammo

### Cool Mode (`scripts/core/msn_cool_mode.reds`)
- [ ] Time-slow cinematic mode — stackable duration
- [ ] Style points multiplier — combo-driven scoring

### Hunter AI (`scripts/core/msn_hunter_ai.reds`)
- [ ] Bounty Hunter AI — adaptive tactics, player tracking
- [ ] Hunter ranks — Bounty → Elite → Legendary

### Horsemen Audio (`scripts/core/msn_horsemen_audio.reds`)
- [ ] Dynamic soundtrack — 4 Horsemen themes
- [ ] Battle intensity detection — adaptive audio mixing

---

## P2 — Medium Term

- [ ] **Magic Expansion** — 36 more spells (total 76+)
- [ ] **Jedi Expansion** — Force ghost mechanic, Holocron system
- [ ] **Abyssal Expansion** — Deep Sea Keeps, Abyssal Races
- [ ] **Nessie Expansion** — Nessie combat skills, evolution path
- [ ] **NGD Expansion** — RNN training visualization dashboard
- [ ] **Watson Expansion** — Megabuilding interiors, gang strongholds
- [ ] **Cognito Expansion** — 3 more perception channels (DREAM, SYMBOLIC, TEMPORAL)

---

## P3 — Long Term

- [ ] Multiplayer sync — shared token economy
- [ ] NSSP mainnet bridge — real blockchain integration
- [ ] NPC faction system — dynamic reputation web
- [ ] Quest framework — modder API for custom campaigns
- [ ] In-game mod menu — CET-independent UI

---

## P4 — Quarantined

- [ ] Llama 3 deployment — CPU-only inference (blocked: performance)
- [ ] Cognito On by default — safety-first (blocked: consent principle)
- [ ] Auto-apply Graphics AI — user choice violation (blocked: consent)
- [ ] Web3 wallet integration — (blocked: scope creep, regulatory)

---

## Known Issues

| ID | Description | Workaround |
|----|-------------|------------|
| EMSN-001 | Lilith campaign quest 5 dialogue may skip under load | `msn.lilith.dialogue 5 <phase>` | 
| EMSN-002 | Freighter routes may desync on fast-travel | `msn.freighter.status` to check |
| EMSN-003 | Hell biome transition FX missing in some circles | `msn.hell.biome.status` to verify |
| EMSN-004 | Abyssal hat vendor inventory not refreshing | `msn.abyssal.reset_hats` |
| EMSN-005 | NGD telemetry history truncated at 100 entries | `msn.ngd.clear` to reset |

---

*The road is the destination | Δ∞ − 1 = 0*
