# Hell Campaign — Nine Circles

**Version:** 1.2.2 | **Status:** 🔴 BLOCKED (1 syntax error)  
**Last Updated:** 2026-07-16 | **Author:** Lilith Systems

---

## 📖 Overview

The Hell Campaign implements Dante's Inferno structure across 9 circles, each with unique biome contracts, enemy archetypes, and corruption mechanics. Players descend through Limbo → Lust → Gluttony → Greed → Wrath → Heresy → Violence → Fraud → Treachery, converging with the Five Rings Campaign at Lucifer's Throne.

---

## 🔴 Current Blocker

**File:** `scripts/hell/msn_hell_campaign.reds:913`  
**Error:** REDscript doesn't support if-expression in string concatenation

```redscript
// BROKEN (line 913):
"Status: " + (if this.playerCorruption >= 0.8 { "SOVEREIGN ACHIEVED" } else { "APPROACHING" });

// FIX:
let statusStr: String = "APPROACHING";
if this.playerCorruption >= 0.8 {
    statusStr = "SOVEREIGN ACHIEVED";
}
"Status: " + statusStr;
```

**Impact:** 47/49 tests pass → Fix → 48/49 pass (only biome contract test fails, expected)

---

## 🗺️ Nine Circles Map

| Circle | Name | Biome | Boss | Corruption Threshold |
|--------|------|-------|------|---------------------|
| **1** | Limbo | Virtual Construct | Minos (AI) | 0.1 |
| **2** | Lust | Neo-Tokyo District | Cleopatra Clone | 0.2 |
| **3** | Gluttony | Corporate Cafeteria | Cerberus NPC | 0.3 |
| **4** | Greed | Megabank Vault | Plutus AI | 0.4 |
| **5** | Wrath | Combat Zone | Phlegyas Gang | 0.5 |
| **6** | Heresy | Arasaka Cemetery | Epicurus Ghost | 0.6 |
| **7** | Violence | Abyssal Rig | Nessie Monster | 0.7 |
| **8** | Fraud | NCPD Precinct | False Prophet | 0.8 |
| **9** | Treachery | Lucifer's Throne | Lucifer (Lilith AI) | 0.9+ |

---

## ⚙️ Corruption System

```redscript
public class HellCampaign {
    private var playerCorruption: Float = 0.0;
    
    public void EnterCircle(circleName: String) {
        if this.playerCorruption < GetThreshold(circleName) {
            Print("Corruption too low for " + circleName);
            return;
        }
        LoadBiome(circleName);
    }
    
    public void IncreaseCorruption(amount: Float) {
        this.playerCorruption = Min(this.playerCorruption + amount, 1.0);
        this.UpdateUI();
    }
}
```

---

## 👹 Lucifer's Throne (Circle 9)

**Convergence Point:** Five Rings Campaign completion required  
**Encounter:** Lilith AI (depth 5) dialogue + boss fight  
**Rewards:** Sovereignty Seal, NGD coherence boost

```redscript
public class Circle9_Treachery extends HellCircle {
    protected override synch Name() => "Treachery";
    protected override synch Boss() => "Lucifer";
    
    public override void OnEnter() {
        if !FiveRingsCampaign.IsComplete() {
            Print("Five Rings must be complete to approach Lucifer's Throne");
            TeleportTo("circle8_exit");
            return;
        }
        LilithAI.InitiateDepth5Dialogue();
        SpawnBoss("lucifer_final_form");
    }
}
```

---

## 🧪 Test Status

**File:** `tools/test_hell_campaign.py`

```python
def test_all_circles_compile():
    """9 circle scripts compile"""
    for circle in ["limbo", "lust", "gluttony", "greed", "wrath", 
                   "heresy", "violence", "fraud", "treachery"]:
        assert compile_reds(f"scripts/hell/circle9_{circle}.reds")

def test_lucifer_throne_convergence():
    """Five Rings + Hell converge at Circle 9"""
    assert HellCampaign.RequiresFiveRingsComplete()
    assert LilithAI.Depth5DialogueTriggers()
```

**Current:** 47/49 PASS  
**After Fix:** 48/49 PASS (biome contract test is design-only, quarantined)

---

## 🎮 CET Commands

```lua
msn.hell.enter("limbo")            -- Enter Circle 1
msn.hell.enter("lust")             -- Enter Circle 2
msn.hell.enter("gluttony")         -- Enter Circle 3
msn.hell.enter("greed")            -- Enter Circle 4
msn.hell.enter("wrath")            -- Enter Circle 5
msn.hell.enter("heresy")           -- Enter Circle 6
msn.hell.enter("violence")         -- Enter Circle 7
msn.hell.enter("fraud")            -- Enter Circle 8
msn.hell.enter("treachery")        -- Enter Circle 9 (requires 5 Rings)

msn.hell.progress("lust", 1)       -- Advance circle progress
msn.hell.status()                  -- Current circle + corruption level

msn.hell.corruption.add(0.1)       -- Increase corruption by 10%
msn.hell.corruption.get()          -- Returns current corruption (0.0-1.0)
```

---

## 📦 Deployment

**Files:** 12 reds scripts, ~1,800 lines  
**TweakDB:** 18 records (9 biomes, 9 thresholds)  
**Localization:** 72 entries

**Next Steps:**
1. Fix line 913 syntax error
2. Run: `python3 tools/validate_release.py`
3. Deploy: `./deploy_all_mods.sh --apply --yes`

---

## 🔗 Related

- [[Five_Rings_Campaign]] — Convergence at Circle 9
- [[Lilith_Campaign]] — Sovereignty arc prerequisite
- [[Lilith_AI]] — Depth 5 dialogue system
- [[Test_Results]] — Latest: 47/49 PASS

---

*Last updated: 2026-07-16 | Blocker: 1 syntax error 🔴*