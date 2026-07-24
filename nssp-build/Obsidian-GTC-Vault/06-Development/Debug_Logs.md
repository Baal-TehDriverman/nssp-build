# Debug Logs

**Sources:** REDscript cache, CET console, NGD telemetry logs
**Status:** Reference — log types, locations, and interpretation

---

## Log Sources

### 1. REDscript Cache (`cyberpunk2077.dev.cache`)

**Location:** `Cyberpunk 2077/r6/cache/cyberpunk2077.dev.cache`

Commands to check:
```bash
# Check cache age
ls -la ~/.local/share/Steam/steamapps/common/Cyberpunk\ 2077/r6/cache/cyberpunk2077.dev.cache

# Check cache validity
python3 -c "
import os, struct
path = os.path.expanduser('~/.local/share/Steam/steamapps/common/Cyberpunk 2077/r6/cache/cyberpunk2077.dev.cache')
with open(path, 'rb') as f:
    magic = f.read(4)
    version = struct.unpack('<I', f.read(4))[0]
print(f'Magic: {magic} | Version: {version}')
"
```

### 2. CET Console

**In-game:** Open CET console (`~`) and type:
```lua
msn.status()           -- System health check
msn.master.status     -- Master console status
```

**Log file:** `Cyberpunk 2077/bin/x64/plugins/cyber_engine_tweaks/cyber_engine_tweaks.log`

```bash
# View recent CET errors
tail -50 ~/.local/share/Steam/steamapps/common/Cyberpunk\ 2077/bin/x64/plugins/cyber_engine_tweaks/cyber_engine_tweaks.log | grep -i "msn\|error\|fail\|exception"
```

### 3. NGD Telemetry Log

In-game via CET:
```lua
msn.ngd.log            -- View telemetry history
msn.ngd.clear          -- Clear telemetry log
```

Telemetry stored as quest facts:
```
msn_ngd_telemetry_0 through msn_ngd_telemetry_99
msn_ngd_telemetry_count
msn_ngd_telemetry_interval
```

### 4. Quest Fact Dump

To inspect any MSN system state:
```lua
msn.debug.getfact "msn_lilith_campaign_started"
msn.debug.getfact "msn_hell_current_circle"
msn.debug.getfact "msn_token_balance_NSSP_NATIVE"
msn.debug.getfact "msn_ngd_telemetry_count"
```

### 5. Game Log (`Cyberpunk2077.log`)

```bash
tail -200 ~/.local/share/Steam/steamapps/common/Cyberpunk\ 2077/Cyberpunk2077.log | grep -i "msn\|error\|mod\|script"
```

---

## Common Issues & Debug Steps

### Script Not Loading

**Symptoms:** `msn.*` commands not recognized in CET
**Checks:**
1. Verify scripts deployed: `ls ~/.local/share/Steam/steamapps/common/Cyberpunk\ 2077/r6/mods/msn_integration/scripts/`
2. Check REDscript cache was rebuilt (restart game)
3. Check CET console for parse errors: look in CET log for `msn` references
4. Verify `init.lua` exists and loads scripts in correct order

### Command Not Found

**Symptom:** `msn.something.help` works but `msn.something.action` returns nil
**Checks:**
1. Check if the specific system has been initialized (some require triggers)
2. `msn.master.status` — verify master console sees all commands
3. Some commands are only registered after their system is first used
4. Try `msn.status()` first to ensure core is loaded

### Token Balance Wrong

**Symptom:** Token balance doesn't match expected value
**Checks:**
1. `msn.tokens.sync` — force sync from save facts
2. `msn.tokens.status` — view all balances
3. Exchange operations are split into 8 bundles — wait for all to complete
4. Check fact values: `msn.debug.getfact "msn_token_balance_NSSP_NATIVE"`

### Campaign Progress Lost

**Symptom:** Campaign quests reset or stuck
**Checks:**
1. `msn.lilith.campaign.status` — view current quest state
2. `msn.hell.status` — view hell progress
3. `msn.fiverings.status` — view five rings progress
4. `msn.symbiosis.campaigns` — check all campaign state facts
5. `msn.debug.getfact "msn_lilith_campaign_current_quest"` — raw quest ID

### NGD Telemetry Not Recording

**Symptom:** `msn.ngd.log` returns empty
**Checks:**
1. `msn.ngd.attach` — ensure adapter is attached
2. `msn.ngd.status` — check adapter health
3. Telemetry interval defaults to 30s — wait for collection
4. Verify GPU drivers support telemetry queries

### Hell Biome Effects Missing

**Symptom:** No visual/environmental effects in Hell circles
**Checks:**
1. `msn.hell.biome.status` — verify biome is active
2. `msn.hell.biome.list` — confirm all 11 modules registered
3. Some effects require certain NGD route mode (HYBRID_OK, LOCAL_REQUIRED, etc.)
4. Check circle-specific hazards are supported by player hardware

---

## Diagnostic Command Sequence

When reporting a bug, run this and include output:

```lua
msn.status()
msn.master.status
msn.lilith.status
msn.symbiosis.status
msn.ngd.status
msn.cognito.status
msn.debug.getfact "msn_scripts_loaded"
```

---

## CET Profile Commands

```lua
-- Benchmark macros
msn.lilith.campaign.start           ; msn.lilith.campaign.status
msn.hell.pact                       ; msn.hell.accept_pact true
msn.fiverings.status                ; msn.map.encounter.list
msn.abyssal.status                  ; msn.nessie.status
msn.tokens.status                   ; msn.gangs.status
msn.magic.status                    ; msn.jedi.status

-- Full state dump (for bug reports)
msn.status()                        -- Core
msn.symbiosis.campaigns             -- All campaigns
msn.debug.getfact "msn_scripts_loaded"  -- Script load state
```

---

*First, diagnose. Then, resolve. | Δ∞ − 1 = 0*
