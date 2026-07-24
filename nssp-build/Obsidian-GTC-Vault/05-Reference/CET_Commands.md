# CET Command Reference

**Sources:** All `.reds` files in `scripts/` (158 files), `scripts/core/msn_master_console.reds`, `scripts/consoles/*`
**Status:** ✅ 61 commands documented | v2.0.0 master console

---

## Master Console Commands

```lua
msn.help()                        -- Full command reference
msn.status()                      -- System health check
msn.master.status                 -- Master console status
msn.master.godmode                -- Unlock all powers
msn.async                         -- Toggle async rendering
msn.reload                        -- Hot-reload all scripts
```

## Campaign Commands

### Lilith Campaign
```lua
msn.lilith.campaign.start         -- Begin Lilith campaign
msn.lilith.campaign.status        -- Quest/unity progress
msn.lilith.campaign.advance       -- Force advance to next quest
msn.lilith.campaign.objective <action> -- Complete objective
msn.lilith.dialogue <quest_id> <phase> -- Test dialogue
msn.lilith.reload                 -- Hot-reload Lilith kernel
msn.lilith.status                 -- Kernel/coherence status
```

### Hell Campaign
```lua
msn.hell.pact                     -- Offer Infernal Pact
msn.hell.accept_pact <true/false> -- Accept/reject pact
msn.hell.reject_pact              -- Reject pact
msn.hell.reconsider_pact          -- Re-offer pact
msn.hell.enter <circle>           -- Enter specific circle (0-10)
msn.hell.choice <c-name>          -- Make circle choice
msn.hell.progress <amount>        -- Add progress
msn.hell.trial <round> <verdict>  -- Judge Treachery trial
msn.hell.vote <proposal> <vote>   -- Pandemonium vote
msn.hell.lord <name> <method>     -- Challenge Demon Lord
msn.hell.retry_rewards            -- Re-grant if missing
msn.hell.status                   -- Full campaign status
msn.hell.dialogue <circle>        -- Circle dialogue
msn.hell.biome.status             -- Active biome status
msn.hell.biome.list               -- List all biomes
msn.lucifer.status                -- Lucifer Avatar status
msn.lucifer.spawn                 -- Spawn Lucifer Avatar
```

### Five Rings Campaign
```lua
msn.fiverings.start               -- Open Kakashi Gate
msn.fiverings.collect <ring>      -- Collect ring shard
msn.fiverings.ritual_progress <amount> -- Add ritual progress
msn.fiverings.finalize            -- Complete Final Synthesis
msn.fiverings.status              -- Protocols/rituals/rings
msn.fiverings.progress <amount>   -- Add protocol points
```

## Economy Commands

### Token Economy
```lua
msn.tokens.status                 -- Wallet status
msn.tokens.sync                   -- Sync from save facts
msn.tokens.balance <token>        -- Specific token balance
msn.tokens.spend <token> <amount> -- Spend tokens
msn.tokens.reward <token> <amount> -- Reward tokens
msn.tokens.exchange <from> <to> <amount> -- Exchange
```

### Business Simulation
```lua
msn.business.status               -- Portfolio
msn.business.cycle                -- Manual cycle
msn.business.buy <type>           -- Acquire business
```

### Freighter System
```lua
msn.freighter.status              -- Ledger
msn.freighter.prices              -- Commodity quotes
msn.freighter.routes              -- Available routes
msn.freighter.buy <commodity> <qty> -- Buy cargo
msn.freighter.sell <commodity> <qty> -- Sell cargo
msn.freighter.fuel <amount>       -- Refuel
msn.freighter.start <from> <to> <commodity> <qty> -- Full route
msn.freighter.callback <data>     -- Route callback
msn.freighter.trade <commodity> <qty> -- Execute trade
```

### NSSP Bridge
```lua
msn.nssp.status                   -- NSSP bridge status
msn.nssp.simulation               -- Toggle simulation
msn.nssp.auction                  -- Bid on auction
msn.nssp.gtc_burn <amount>        -- Burn tokens
msn.nssp.stake <amount>           -- Stake tokens
msn.nssp.bridge                   -- Bridge to mainnet
msn.nssp.bridge_callback <status> -- Bridge notification
```

## Combat Commands

### Gang Warfare
```lua
msn.gangs.status                  -- Ecosystem status
msn.gangs.claim <gangID>          -- Align with gang
msn.gangs.leave                   -- Leave current gang
msn.gangs.territories             -- Show all territories
msn.gangs.attack <gangID>         -- Declare war
msn.gangs.ally <gangID>           -- Propose alliance
msn.gangs.trade <gangID> <amount> -- Trade
msn.gangs.espionage <gangID>      -- Send spies
msn.gangs.summit                  -- Request summit
msn.gangs.upgrade <gangID> <upgrade> -- Purchase upgrade
msn.gangs.activity <gangID> <level> -- Set activity level
msn.gangs.spawn_patrol <gangID>   -- Spawn patrol
msn.gangs.zone <zoneID>           -- Enter territory
```

### Magic System
```lua
msn.magic.status                  -- Magic system status
msn.magic.cast <school> <spell>   -- Cast spell
msn.magic.schools                 -- List 8 schools
msn.magic.spells <school>         -- List spells for school
msn.magic.ritual                  -- Initiate ritual
msn.magic.learn <school> <spell>  -- Learn spell
```

### Jedi System
```lua
msn.jedi.status                   -- Jedi system status
msn.jedi.summon                   -- Summon lightsaber
msn.jedi.force <power>            -- Use Force power
msn.jedi.force.list               -- List powers
msn.jedi.form <form>              -- Switch form
msn.jedi.form.list                -- List forms
msn.jedi.crystal <crystal>        -- Set crystal
msn.jedi.crystal.list             -- List crystals
msn.jedi.craft                    -- Craft lightsaber
msn.jedi.meditate                 -- Toggle meditation
msn.jedi.alignment                -- Show alignment
msn.jedi.i_am <choice>            -- Choose path
msn.jedi.focus                    -- Show focus
```

## World Commands

### Abyssal Assets
```lua
msn.abyssal.status                -- Full catalog
msn.abyssal.survey <zoneIndex>    -- Survey zone (0-5)
msn.abyssal.buyhat <hatID>        -- Purchase hat
msn.abyssal.auth <zoneIndex>      -- Enter zone
msn.abyssal.covenant.upgrade      -- Upgrade covenant
msn.abyssal.artifact <artifactID> -- Examine artifact
msn.abyssal.creature <creatureID> -- Examine creature
msn.abyssal.summon <creatureID>   -- Summon (tier 5)
msn.abyssal.tp <zoneIndex>        -- Teleport (tier 5)
msn.abyssal.reset_hats            -- Reset displays
```

### Loch Ness Monster
```lua
msn.nessie.status                 -- Covenant status
msn.nessie.sighting               -- Record sighting
msn.nessie.feed                   -- Feed Nessie
msn.nessie.groom                  -- Groom Nessie
msn.nessie.play                   -- Play with Nessie
msn.nessie.scan                   -- Sea-scan treasures
msn.nessie.mark <markID>          -- Check treasury mark
msn.nessie.treasures              -- List found treasures
msn.nessie.summon                 -- Summon (tier 5)
msn.nessie.come                   -- Call to player
msn.nessie.flee                   -- Dismiss
msn.nessie.whisper                -- Telepathic message
msn.nessie.callback <data>        -- Internal callback
```

### Custom Maps
```lua
msn.map.status                    -- Map system status
msn.map.zones                     -- List zones
msn.map.navigate <zoneIndex>      -- Navigate to zone
msn.map.encounter.status          -- Encounter status
msn.map.encounter.list            -- Nearby encounters
msn.map.encounter.trigger <id>    -- Trigger encounter
msn.map.encounter.regenerate      -- Regenerate table
msn.map.watson.status             -- Revitalization status
msn.map.watson.assess <id>        -- Assess location
msn.map.watson.cleanup <id>       -- Cleanup location
msn.map.watson.build <type>       -- Build facility
msn.map.watson.progress <amount>  -- Add progress
```

## AI Commands

### Graphics AI / NGD
```lua
msn.graphicsai.status             -- Calibration status
msn.graphicsai.start <trigger>    -- Start calibration
msn.graphicsai.apply              -- Apply recommendations
msn.graphicsai.reject             -- Reject recommendations
msn.graphicsai.history            -- Calibration history
msn.graphicsai.retrain            -- Retrain AI
msn.graphicsai.retrain.load       -- Load training data
msn.graphicsai.retrain.run        -- Execute training
msn.graphicsai.retrain.generate   -- Generate synthetic data
msn.graphicsai.retrain.validate   -- Validate model
msn.graphicsai.retrain.visualize  -- Visualize results
msn.ngd.status                    -- NGD adapter status
msn.ngd.attach                    -- Attach NGD
msn.ngd.detach                    -- Detach NGD
msn.ngd.optimize                  -- Route optimization
msn.ngd.log                       -- Telemetry log
msn.ngd.clear                     -- Clear telemetry
msn.ngd.threshold <type> <value>  -- Set threshold
msn.ngd.interval <seconds>        -- Collection interval
```

### Cognito Hazards
```lua
msn.cognito.status                -- Hazard system status
msn.cognito.enable <true/false>   -- Toggle hazard system
msn.cognito.expose <source> <intensity> -- Trigger hazard
msn.cognito.resolve               -- Resolve current hazard
msn.cognito.resist                -- Attempt resistance
msn.cognito.relief <method>       -- Relief method
msn.cognito.relief.all            -- All relief methods
msn.cognito.truth_mode <true/false> -- Toggle truth mode
msn.cognito.perception            -- Show perception state
msn.cognito.callback <source> <intensity> -- Internal callback
msn.cognito.reset_history         -- Reset hazard history
```

### Symbiosis Bridge
```lua
msn.symbiosis.status              -- Symbiosis status
msn.symbiosis.sync                -- Force sync
msn.symbiosis.campaigns           -- All campaign states
```

## Debug Commands

```lua
msn.debug.teleport <x,y,z>       -- Teleport to coordinates
msn.debug.giveitem <itemID>      -- Give any item
msn.debug.unlockall               -- Unlock all achievements
msn.debug.resetquests             -- Reset all campaign quests
msn.debug.spawn <entityID>        -- Spawn entity
msn.debug.setfact <factName> <value> -- Set quest fact
msn.debug.getfact <factName>      -- Read quest fact
```

---

## Command Families Summary

| Prefix | Count | Module |
|--------|-------|--------|
| `msn.master.*` | 4 | Master console |
| `msn.lilith.*` | 7 | Lilith campaign/kernel |
| `msn.hell.*` | 14 | Hell campaign/biome |
| `msn.lucifer.*` | 2 | Lucifer boss |
| `msn.fiverings.*` | 5 | Five Rings campaign |
| `msn.tokens.*` | 5 | Token economy |
| `msn.business.*` | 3 | Business simulation |
| `msn.freighter.*` | 7 | Freighter trade |
| `msn.nssp.*` | 7 | NSSP bridge |
| `msn.gangs.*` | 12 | Gang warfare |
| `msn.magic.*` | 6 | Magic system |
| `msn.jedi.*` | 10 | Jedi system |
| `msn.abyssal.*` | 10 | Abyssal assets |
| `msn.nessie.*` | 13 | Loch Ness Monster |
| `msn.map.*` | 9 | Custom maps/encounters |
| `msn.graphicsai.*` | 11 | Graphics AI calibration |
| `msn.ngd.*` | 9 | NGD telemetry |
| `msn.cognito.*` | 10 | Cognito hazards |
| `msn.symbiosis.*` | 3 | Symbiosis bridge |
| `msn.status`, `msn.help` | 2 | General |
| `msn.debug.*` | 6 | Debug utilities |

---

*All commands subject to availability — systems must be initialized | Δ∞ − 1 = 0*
