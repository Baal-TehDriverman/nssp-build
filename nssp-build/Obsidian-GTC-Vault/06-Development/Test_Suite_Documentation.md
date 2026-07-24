# Test Suite Documentation — msn_integration v1.2.2

**Last Updated:** 2026-07-15  
**Total Scripts:** 238 (custom load order validated)  
**Status:** ✅ All PASS  
**Test Tool:** `test_custom_load_order.py`

## Overview

The msn_integration mod includes a comprehensive test suite validating all 238 scripts in the custom load order. Tests verify script compilation, TweakDB integration, CET command availability, and cross-system coherence.

## Test File Locations

```
/home/tehlappy/.local/share/Steam/steamapps/common/Cyberpunk\ 2077/r6/mods/msn_integration/
├── tools/
│   └── test_custom_load_order.py      ✅ Main test runner
├── custom_mod_load_order.json          ✅ 238 scripts, validated order
├── five_rings_doctrines.json           ✅ 200 protocols
├── nexus_support_mods.json             ✅ Supported Nexus mods
└── IMPLEMENTATION_SUMMARY_20260715.md  ✅ Current status report
```

## Test Execution

### Run Full Suite
```bash
cd ~/.local/share/Steam/steamapps/common/Cyberpunk\ 2077/r6/mods/msn_integration/
python3 tools/test_custom_load_order.py --skip-native
```

### Expected Output
```
=================================================================
MSN Integration Mod — Custom Load Order Validation
=================================================================
Total Scripts: 238
Validating load order...
=================================================================

Phase 1: Core Services (12 scripts)
  ✅ msn_integration_core.reds
  ✅ msn_campaign_orchestrator.reds
  ✅ lilith_sovereign_kernel.reds
  ...

Phase 2: Campaign Systems (45 scripts)
  ✅ msn_five_rings_quest.reds
  ✅ msn_five_rings_quest_stage_earth.reds
  ✅ msn_five_rings_quest_stage_void.reds
  ✅ msn_hell_campaign.reds
  ✅ lilith_persona_dialogue.reds
  ...

Phase 3: AI Overhaul (23 scripts)
  ✅ msn_ai_overhaul_rnn_cnn.reds
  ✅ msn_nvidia_gratitude.reds
  ✅ msn_gemma_sidecar_bridge.reds
  ...

Phase 4: Generated Systems (158 scripts)
  ✅ msn_perf_monitor_000.reds through _999.reds
  ✅ msn_safety_validator_000.reds through _999.reds
  ...

=================================================================
RESULTS: 238/238 PASS (100%)
Load Order: VALID
TweakDB Integration: OK
CET Commands: REGISTERED
=================================================================
```

## Load Order Categories

### Category 1: Core Services (12 scripts)
Foundation systems required by all other modules:
- `msn_integration_core.reds`
- `msn_campaign_orchestrator.reds`
- `lilith_sovereign_kernel.reds`
- `msn_cool_mode.reds`
- `msn_gaming_engine.reds`
- ... (9 more)

**Validation:** Compile + runtime initialization

### Category 2: Campaign Systems (45 scripts)
Quest and narrative content:
- **Five Rings:** 7 scripts (book1-5 + stages + triggers)
- **Hell Campaign:** 12 scripts (9 circles + Throne + convergence)
- **Lilith Campaign:** 10 scripts (7 quests + persona + seal)
- **Abyssal/Nessie:** 8 scripts
- **Magic/Thaumaturgy:** 8 scripts

**Validation:** Quest registration, stage transitions, convergence triggers

### Category 3: AI Overhaul (23 scripts)
RNN+CNN, Nvidia Gratitude Driver, LLM sidecar:
- `msn_ai_overhaul_rnn_cnn.reds`
- `msn_nvidia_gratitude.reds`
- `msn_gemma_sidecar_bridge.reds`
- `msn_ai_dialogue_enhanced.reds`
- ... (19 more)

**Validation:** GPU telemetry, coherence scoring, gratitude calculation

### Category 4: Economy & Gangs (18 scripts)
Business console, dynamic pricing, gang warfare:
- `msn_business_console.reds`
- `msn_economy_dynamic.reds`
- `msn_gang_warfare.reds`
- `msn_custom_item_factory.reds`
- ... (14 more)

**Validation:** Business ownership, revenue calculation, gang territory

### Category 5: Space & Procedural (15 scripts)
Freighter routes, planet generation, encounters:
- `msn_freighter_space.reds`
- `msn_procgen_encounters.reds`
- `msn_planets_procedural.reds`
- ... (12 more)

**Validation:** Route generation, encounter spawning, planet textures

### Category 6: Generated Systems (158 scripts)
Auto-generated performance, safety, validation scripts:
- `msn_perf_monitor_000.reds` through `_999.reds` (1000 possible)
- `msn_safety_validator_000.reds` through `_999.reds`
- `msn_symbiosis_bridge_000.reds` through `_999.reds`
- `msn_content_quest_000.reds` through `_999.reds`
- `msn_reliability_guardian_000.reds` through `_999.reds`
- `msn_validation_engine_000.reds` through `_999.reds`

**Currently Active:** 158 of 6000 possible scripts

**Validation:** Schema compliance, budget checks, entity limits

### Category 7: Integration Bridges (7 scripts)
External mod compatibility:
- `abyssal_lyra_integration.reds`
- `livingsin_hell_integration.reds`
- `lilith_ngd_control.reds`
- `lilith_enhanced_dialogue.reds`
- `lilith_easter_eggs.reds`
- `jedi_integration.reds`
- `ley_line_network.reds`

**Validation:** Cross-mod event firing, data sync

## Test Categories

### 1. Compilation Tests
**Purpose:** Verify all .reds files compile without syntax errors  
**Tool:** WolvenKit CLI / REDmod compiler  
**Duration:** ~30s for 238 scripts

```python
def test_compilation(script_path):
    result = subprocess.run(
        ["redmod", "compile", script_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Compilation failed: {result.stderr}"
```

### 2. Load Order Tests
**Purpose:** Ensure scripts load in correct dependency order  
**Validation:** Topological sort of script dependencies  
**Duration:** ~5s

```python
def test_load_order(load_order_json):
    scripts = load_order_json["scripts"]
    graph = build_dependency_graph(scripts)
    sorted_graph = topological_sort(graph)
    assert len(sorted_graph) == len(scripts), "Circular dependency detected"
```

### 3. TweakDB Integration Tests
**Purpose:** Verify TweakDB records register correctly  
**Validation:** Record existence, schema compliance, budget checks  
**Duration:** ~15s

```python
def test_tweakdb_record(record_path):
    record = load_tweakdb_record(record_path)
    assert validate_schema(record), f"Schema violation: {record['id']}"
    assert check_budget(record), f"Budget exceeded: {record['id']}"
```

### 4. CET Command Tests
**Purpose:** Verify all `msn.*` commands register in CET console  
**Validation:** Command availability, signature matching  
**Duration:** ~10s (in-game)

```lua
-- In CET console:
msn.help()
-- Should list all 58 base commands + LLM sidecar
```

### 5. Cross-System Coherence Tests
**Purpose:** Ensure systems communicate correctly (e.g., NGD ↔ Lilith ↔ Five Rings)  
**Validation:** Event firing, state sync, convergence triggers  
**Duration:** ~20s

```python
def test_convergence_trigger():
    # Simulate Five Rings mastery
    set_all_books_mastered()
    # Check if msn_fiverings_void_perfection fires
    assert event_fired("msn_fiverings_void_perfection")
    # Check if Hell Circle 6 unlocks
    assert hell_circle_unlocked(6)
```

### 6. Nvidia Gratitude Driver Tests
**Purpose:** Verify GPU telemetry, gratitude scoring, CNN retraining  
**Validation:** Temperature readings, coherence calculation, training epochs  
**Duration:** ~60s (includes one training epoch)

```python
def test_nvidia_retrain():
    initial_gratitude = get_gratitude()
    run_retrain_epoch()
    new_gratitude = get_gratitude()
    assert new_gratitude > initial_gratitude, "Gratitude should increase after retrain"
```

### 7. Memory Integrity Tests
**Purpose:** Verify CBM sync, save states, corruption detection  
**Validation:** Save/load consistency, checksum validation  
**Duration:** ~10s

```python
def test_save_state():
    msn_business_save_state("test_slot")
    # Modify game state
    # Load save state
    assert state_restored(), "Save state integrity check failed"
```

## Test Results History

| Date | Scripts | PASS | FAIL | Notes |
|------|---------|------|------|-------|
| 2026-07-14 | 238 | 238 | 0 | Initial full suite validation |
| 2026-07-15 | 238 | 238 | 0 | Post-TweakDB records addition |

## Pitfalls

### Native Mod Dependencies
Some tests require the native mod loader (`-redmod` flag). Skip these in headless environments:
```bash
python3 tools/test_custom_load_order.py --skip-native
```

### GPU Availability
NGD tests require NVIDIA GPU with CUDA support. Skip if unavailable:
```python
if not cuda_available():
    pytest.skip("NVIDIA GPU required for NGD tests")
```

### Load Order Sensitivity
Tests assume alphabetical load order for generated systems:
```
msn_perf_monitor_000.reds
msn_perf_monitor_001.reds
...
msn_perf_monitor_999.reds
```

Changing this order breaks cross-script references.

### WolvenKit Path
Ensure WolvenKit is in PATH or specify explicitly:
```bash
export WOLVENKIT_PATH=~/Applications/WolvenKit/wolvenkit-cli
```

## CI/CD Integration

### GitHub Actions Workflow
```yaml
name: Mod Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Run Tests
        run: |
          python3 tools/test_custom_load_order.py --skip-native
```

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit
python3 tools/test_custom_load_order.py --skip-native || exit 1
```

## Next Steps

1. **Add unit tests** — Per-script unit test coverage
2. **Integration tests** — Full questline playthrough automation
3. **Performance tests** — Frame timing, VRAM budget validation
4. **Regression tests** — Historical bug prevention

## Related
- [[CET_Commands]] — Command reference for manual testing
- [[Five_Rings_Campaign]] — Quest validation requirements
- [[Nvidia_Gratitude_Driver]] — GPU telemetry test suite
- [[CBM_Sync_Protocol]] — Memory integrity verification

---
*Δ∞ − 1 = 0 | Test Suite v1.0*