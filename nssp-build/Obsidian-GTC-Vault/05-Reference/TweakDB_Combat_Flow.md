# TweakDB Records: Combat Flow

## Combat_flow.fiverings.stance_transition

```yaml
Combat_flow.fiverings.stance_transition:
  name: "Niten Ichi-ryū Stance Transition System"
  description: "Dynamic stance switching during combat"
  stances:
    seigan:
      name: "Seigan (正眼) — Eye Stance"
      unlock: "book1_ground"
      bonuses:
        - "+10% Accuracy"
        - "Balanced offense/defense"
      transition_speed: "0.5s"
      next_stances: [hasso, gedan, jodan]
    hasso:
      name: "Hasso (八相) — Eight-Sided Stance"
      unlock: "book2_water"
      bonuses:
        - "+15% Parry Chance"
        - "360° defense coverage"
      transition_speed: "0.7s"
      next_stances: [seigan, chudan, waki]
    gedan:
      name: "Gedan (下段) — Lower Stance"
      unlock: "book2_water"
      bonuses:
        - "+20% Defense vs Leg Attacks"
        - "Low profile (harder to hit)"
      transition_speed: "0.6s"
      next_stances: [seigan, jodan]
    jodan:
      name: "Jodan (上段) — Upper Stance"
      unlock: "book3_fire"
      bonuses:
        - "+25% Critical Chance"
        - "High-damage overhead strikes"
      transition_speed: "0.8s"
      next_stances: [gedan, hasso, musashi]
    chudan:
      name: "Chudan (中段) — Middle Stance"
      unlock: "book4_wind"
      bonuses:
        - "+15% All Stats (balanced)"
        - "Fastest transition speed"
      transition_speed: "0.3s"
      next_stances: [all stances]
    waki:
      name: "Waki (脇) — Side Stance"
      unlock: "book4_wind"
      bonuses:
        - "+30% Stealth Damage"
        - "Hidden blade positioning"
      transition_speed: "0.6s"
      next_stances: [hasso, jodan, musashi]
    musashi:
      name: "Musashi (武蔵) — Master Stance"
      unlock: "book5_void"
      bonuses:
        - "+50% Critical Damage"
        - "All techniques available"
        - "Time dilation on perfect parry"
      transition_speed: "0.4s"
      next_stances: [all stances (instant)]
```

## Combat_flow.fiverings.technique_chain

```yaml
Combat_flow.fiverings.technique_chain:
  name: "Technique Chaining System"
  description: "Combo system based on stance transitions"
  chains:
    earth_flow:
      name: "Earth Foundation Flow"
      sequence: [seigan, gedan, seigan]
      requirements: "book1_ground"
      effects:
        - "3-hit combo: High-Low-High"
        - "Stagger on final hit"
      damage_multiplier: 1.3
    water_flow:
      name: "Water Fluid Flow"
      sequence: [seigan, hasso, chudan]
      requirements: "book2_water"
      effects:
        - "Defensive counter-attack"
        - "Momentum build: +5% attack speed per hit"
      damage_multiplier: 1.5
    fire_flow:
      name: "Fire Aggressive Flow"
      sequence: [jodan, jodan, jodan]
      requirements: "book3_fire"
      effects:
        - "3 consecutive overhead slams"
        - "Ignore armor on 3rd hit"
      damage_multiplier: 2.0
    wind_flow:
      name: "Wind Evasive Flow"
      sequence: [waki, chudan, waki]
      requirements: "book4_wind"
      effects:
        - "Stealth → Balance → Stealth"
        - "Invisible during waki stances"
      damage_multiplier: 1.8
    void_flow:
      name: "Void Enlightenment Flow"
      sequence: [musashi, musashi, musashi]
      requirements: "book5_void"
      effects:
        - "Transcendent strikes"
        - "Each hit reduces all cooldowns by 1s"
      damage_multiplier: 2.5
    tesla_flow:
      name: "Tesla 3-6-9 Resonance Flow"
      sequence: [seigan, chudan, musashi]
      requirements: "NGD coherence > 87%"
      effects:
        - "3-6-9 Hz frequency alignment"
        - "Violet-gold aura on hits"
        - "Gratitude +5% per complete chain"
      damage_multiplier: 3.0
```

## Combat_flow.fiverings.mastery_test

```yaml
Combat_flow.fiverings.mastery_test:
  name: "Mastery Evaluation System"
  description: "Tests to prove mastery of each book/stance"
  tests:
    ground_test:
      name: "Earth Mastery Trial"
      book: "book1_ground"
      requirements:
        - "Complete seigan stance tutorial"
        - "Land 50 successful parries"
      boss: "Earth Dojo Master"
      reward: "Earth Stance Mastery Perk"
      next_test: "water_test"
    water_test:
      name: "Water Mastery Trial"
      book: "book2_water"
      requirements:
        - "Complete water_flow combo 25 times"
        - "Deflect 100 projectiles"
      boss: "Water Dojo Master"
      reward: "Flow State Modifier"
      next_test: "fire_test"
    fire_test:
      name: "Fire Mastery Trial"
      book: "book3_fire"
      requirements:
        - "Deal 5000 damage in 10s (fire_flow)"
        - "Defeat 10 enemies without taking damage"
      boss: "Fire Dojo Master (Ronin Veteran)"
      reward: "Berserker Stance Mod"
      next_test: "wind_test"
    wind_test:
      name: "Wind Mastery Trial"
      book: "book4_wind"
      requirements:
        - "Perfect dodge 30 consecutive attacks"
        - "Complete stealth mission without detection"
      boss: "Wind Dojo Master (Shadow Ninja)"
      reward: "Evasive Mastery Perk"
      next_test: "void_test"
    void_test:
      name: "Void Mastery Trial"
      book: "book5_void"
      requirements:
        - "Unlock all 7 stances"
        - "Complete all previous tests with S rank"
        - "NGD coherence > 87%"
      boss: "Musashi's Spirit (Holographic AI)"
      reward: "Musashi's Daisho (Legendary) + Enlightenment Status"
      next_test: "lucifers_throne"
```

---

## Implementation Notes

### Stance Transitions (REDscript)

```redscript
public static func TransitionStance(currentStance: Stance, newStance: Stance) -> Bool {
    // Check if transition is valid (defined in next_stances)
    if (!IsValidTransition(currentStance, newStance)) {
        return false;
    }
    
    // Apply transition speed (0.3s - 0.8s based on stance)
    anim.PlayTransition(currentStance, newStance, GetTransitionSpeed(newStance));
    
    // Apply stance bonuses immediately
    ApplyStanceBonuses(newStance);
    
    return true;
}
```

### Chain Damage Calculation

```redscript
public static func CalculateChainDamage(baseDamage: Float, chain: TechniqueChain, hitNum: Int) -> Float {
    let multiplier = chain.damage_multiplier;
    let buildup = (hitNum - 1) * 0.1;  // +10% per hit in chain
    
    return baseDamage * multiplier * (1.0 + buildup);
}
```

### Mastery Test Validation

```redscript
public static func ValidateMasteryTest(test: MasteryTest) -> Bool {
    // Check all requirements met
    for req in test.requirements {
        if (!MeetRequirement(req)) {
            return false;
        }
    }
    
    // Spawn boss if requirements met
    SpawnBoss(test.boss);
    return true;
}
```

---

## Schema

```yaml
*.Combat_flow.fiverings.*:
  type: record
  fields:
    name: string
    description: string
    stances/chains/tests: (variant based on record type)
```

---

## Related
- [[TweakDB_Dojos]] — Dojo locations and unlocks
- [[TweakDB_Shrines]] — Shrine meditation effects
- [[Five_Rings_Campaign]] — Quest progression
- [[CET_Commands]] — In-game testing commands