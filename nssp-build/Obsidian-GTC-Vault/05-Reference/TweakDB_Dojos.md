# TweakDB Records: Five Rings Dojos

## Dojo.fiverings.ground (Earth Dojo)
```yaml
Dojo.fiverings.ground:
  name: "Earth Dojo — Foundation Training"
  description: "Learn the foundation techniques and stance basics of Niten Ichi-ryū"
  location: "Japantown, Westbrook"
  book_requirement: "book1_ground"
  techniques:
    - seigan_stance_basic
    - footwork_fundamentals
    - dual_wield_introduction
  rewards:
    - "Wooden Training Swords (2x)"
    - "Earth Stance Manual"
  quests_unlocked:
    - q_fiverings_ground_01
    - q_fiverings_ground_02
```

## Dojo.fiverings.water (Water Dojo)
```yaml
Dojo.fiverings.water:
  name: "Water Dojo — Fluid Adaptation"
  description: "Master fluid combat techniques and adaptation"
  location: "Kabuki, Wakako's Backroom"
  book_requirement: "book2_water"
  techniques:
    - water_flow_combo
    - adaptive_parries
    - fluid_footwork
  rewards:
    - "Water-Element Katana"
    - "Flow State Modifier"
  quests_unlocked:
    - q_fiverings_water_01
    - q_fiverings_water_02
```

## Dojo.fiverings.fire (Fire Dojo)
```yaml
Dojo.fiverings.fire:
  name: "Fire Dojo — Aggressive Offense"
  description: "Unleash aggressive offensive techniques"
  location: "Arasaka Waterfront, Hidden Compound"
  book_requirement: "book3_fire"
  techniques:
    - flame_strike_combo
    - aggressive_rush
    - fire_element_infusion
  rewards:
    - "Flame-Infused Daisho"
    - "Berserker Stance Mod"
  quests_unlocked:
    - q_fiverings_fire_01
    - q_fiverings_fire_02
    - q_fiverings_fire_boss (Dojo Master)
```

## Dojo.fiverings.wind (Wind Dojo)
```yaml
Dojo.fiverings.wind:
  name: "Wind Dojo — Defensive Mastery"
  description: "Perfect defensive and evasive techniques"
  location: "Charter Hill, Rooftop Training Ground"
  book_requirement: "book4_wind"
  techniques:
    - wind_step_evasion
    - defensive_perimeter
    - counter_attack_mastery
  rewards:
    - "Wind-Walker Cloak"
    - "Evasive Mastery Perk"
  quests_unlocked:
    - q_fiverings_wind_01
    - q_fiverings_wind_02
```

## Dojo.fiverings.void (Void Dojo)
```yaml
Dojo.fiverings.void:
  name: "Void Dojo — Mastery Temple"
  description: "Achieve enlightenment through musashi's void"
  location: "Orbital Air Spaceport, Secret Dojo"
  book_requirement: "book5_void"
  techniques:
    - void_state_meditation
    - musashi_final_stance
    - enlightenment_strike
  rewards:
    - "Musashi's Daisho (Legendary)"
    - "Void Walker Augment"
    - "Enlightenment Status"
  quests_unlocked:
    - q_fiverings_void_final
    - ms Lucifer's Throne convergence
```

---

## Schema
```yaml
*.Dojo.fiverings.*:
  type: record
  fields:
    name: string
    description: string
    location: string
    book_requirement: string (book1_ground | book2_water | book3_fire | book4_wind | book5_void)
    techniques: array[string]
    rewards: array[string]
    quests_unlocked: array[string]
```