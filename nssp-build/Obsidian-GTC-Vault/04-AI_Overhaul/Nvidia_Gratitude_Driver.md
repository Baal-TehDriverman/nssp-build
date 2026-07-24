# Nvidia Gratitude Driver

**Sources:** `scripts/core/msn_graphics_ai_runtime.reds` (783 lines), `scripts/core/msn_graphics_ai_retraining.reds` (409 lines), `scripts/*/*ngd*`
**Status:** ✅ FULLY IMPLEMENTED
**Systems:** `GraphicsAICalibration`, `NGDTelemetryAdapter`, `NGDRouteOptimizer`, `NGDRuntimeTelemetry`

---

## Overview

The Nvidia Gratitude Driver (NGD) is a **recommendation-only** telemetry and calibration system. It does NOT modify game settings — it observes, computes, and suggests. Players choose whether to apply recommendations.

## Graphics AI Calibration

`GraphicsAICalibration` (ScriptableSystem) runs in the background, collecting GPU/rendering data and computing optimal settings.

### Calibration Pipeline
1. **Data Collection** — VRAM usage, FPS, resolution, texture detail, shadow quality, ambient occlusion, ray tracing state, DLSS state
2. **Analysis** — Compare current vs optimal for scene complexity
3. **Recommendation** — Determine if improvement is needed
4. **Apply/Reject** — Player chooses via CET console

### Calibration Triggers
- `start` — Critical performance issue (FPS < 30)
- `auto` — Minor fluctuation (FPS 30-50)
- `manual` — Player requested
- `event` — Scene change (combat, driving, crowded area)

### Calibration Rules (TweakDB)

```tweakdb
msn.graphics.ai.calibration.fps.target.lower  = 30.0
msn.graphics.ai.calibration.fps.target.upper  = 60.0
msn.graphics.ai.calibration.vram.target.free  = 1024.0
msn.graphics.ai.calibration.cooldown          = 300.0
msn.graphics.ai.calibration.auto.apply        = false
msn.graphics.ai.calibration.show.notifications = true
```

## NGD Telemetry

`NGDTelemetryAdapter` collects and logs performance metrics:

### Telemetry Data Points

| Metric | Source | Unit | Frequency |
|--------|--------|------|-----------|
| VRAM Used | GPU | MB | 30s |
| VRAM Free | GPU | MB | 30s |
| FPS | Game | fps | Every frame (buffered) |
| 1% Low FPS | Computed | fps | 30s |
| 0.1% Low FPS | Computed | fps | 60s |
| GPU Temp | GPU | °C | 60s |
| GPU Utilization | GPU | % | 30s |
| VRAM Temp | GPU | °C | 60s |
| Power Draw | GPU | W | 60s |
| Scene Complexity | Computed | score (0-100) | On scene change |
| Texture Pool Usage | Game | MB | 60s |
| Shadow Map Usage | Game | MB | 60s |

### Telemetry Log

- Stored as quest facts: `msn_ngd_telemetry_<n>` (Array of String, up to 100 entries)
- `msn_ngd_telemetry_count` tracks total entries
- `msn_ngd_telemetry_interval` — configurable collection interval (default 30s)

### Alert Thresholds
- VRAM < 512MB free → WARNING
- FPS < 20 → CRITICAL
- GPU Temp > 85°C → WARNING

## NGD Route Optimizer

`NGDRouteOptimizer` provides pathfinding efficiency suggestions:

### Path Data Collected
- Start/end coordinates
- Total route distance
- Estimated time
- Optimization percentage (vs direct path)
- Hazard avoidance (fewer enemies = higher score)

### Optimization Factors
1. Distance reduction %
2. Time reduction %
3. Hazard avoidance score (fewer gang territories = higher)
4. Overall efficiency (weighted average)

### Route Feedback
- Returned as string via `GetOptimizedRouteDataAsString()`
- Player can manually use or ignore

## NGD Runtime Telemetry

`NGDRuntimeTelemetry` extends the runtime telemetry bus:
- Timestamped payloads via `NGDPayload`
- Route data container via `NGDRouteData`
- `AttachNGD()` / `DetachNGD()` adapter lifecycle
- Error state handling

## CET Commands

```lua
msn.graphicsai.status              -- Calibration status
msn.graphicsai.start <trigger>     -- Start calibration
msn.graphicsai.apply               -- Apply recommended settings
msn.graphicsai.reject              -- Reject recommendation
msn.graphicsai.history             -- View calibration history
msn.graphicsai.retrain             -- Trigger AI retraining
msn.graphicsai.retrain.load        -- Load training data
msn.graphicsai.retrain.run         -- Execute training
msn.graphicsai.retrain.generate    -- Generate synthetic data
msn.graphicsai.retrain.validate    -- Validate model
msn.graphicsai.retrain.visualize   -- Visualize training results
msn.ngd.status                     -- NGD adapter status
msn.ngd.attach                     -- Attach NGD adapter
msn.ngd.detach                     -- Detach NGD adapter
msn.ngd.optimize                   -- Request route optimization
msn.ngd.log                        -- View telemetry log
msn.ngd.clear                      -- Clear telemetry log
msn.ngd.threshold <type> <value>   -- Set alert threshold
msn.ngd.interval <seconds>         -- Set collection interval
```

## Integration

- NGD telemetry feeds [[../04-AI_Overhaul/Cognito_Hazards|Cognito Hazard]] exposure sources (GPU/VRAM anomalies)
- Calibration events route through [[Lilith_AI_Integration|Lilith Sovereign Kernel]] event bus
- Route optimization data is logged in `NGDRuntimeTelemetry` for session telemetry
- Route recommendations can be cross-referenced with [[../02-Systems/Gang_Warfare|Gang Warfare]] danger zones
- `GenerateSyntheticTrainingData()` produces AI model retraining input

---

*Gratitude = optimization | Δ∞ − 1 = 0*
