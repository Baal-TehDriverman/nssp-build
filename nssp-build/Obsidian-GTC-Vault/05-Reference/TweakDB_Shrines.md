# TweakDB Records: Five Rings Shrines

## Shrine.fiverings.earth (Stone Shrine)
```yaml
Shrine.fiverings.earth:
  name: "Stone Shrine — Earth Meditation"
  description: "Meditate on the solidity and foundation of earth"
  location: "Badlands, Rocky Mesa"
  book_requirement: "book1_ground"
  meditation_type: "grounding"
  effects:
    - "+10% Stability"
    - "Unlock Earth Stance"
    - "Reduce Stamina Cost 15%"
  wisdom_teachings:
    - "The earth does not move, yet it supports all things"
    - "Foundation before technique"
  convergence:
    - hell_circle_limbo
```

## Shrine.fiverings.water (Wave Shrine)
```yaml
Shrine.fiverings.water:
  name: "Wave Shrine — Water Meditation"
  description: "Flow like water, adapt to all obstacles"
  location: "Pacifica, Abandoned Resort"
  book_requirement: "book2_water"
  meditation_type: "flowing"
  effects:
    - "+15% Attack Speed"
    - "Unlock Water Flow Combo"
    - "Chance to deflect projectiles 20%"
  wisdom_teachings:
    - "Water takes the shape of its container"
    - "Yield to overcome"
  convergence:
    - hell_circle_lust
```

## Shrine.fiverings.fire (Flame Shrine)
```yaml
Shrine.fiverings.fire:
  name: "Flame Shrine — Fire Meditation"
  description: "Burn with the intensity of a thousand suns"
  location: "Heywood, Industrial Incinerator"
  book_requirement: "book3_fire"
  meditation_type: "aggressive"
  effects:
    - "+25% Damage (5s after meditation)"
    - "Unlock Flame Strike"
    - "Fire resistance +30%"
  wisdom_teachings:
    - "Fire destroys to create anew"
    - "Aggression channeled is power"
  convergence:
    - hell_circle_gluttony
```

## Shrine.fiverings.wind (Gale Shrine)
```yaml
Shrine.fiverings.wind:
  name: "Gale Shrine — Wind Meditation"
  description: "Become as the wind—untouchable, unseen"
  location: "Santo Domingo, Wind Farm"
  book_requirement: "book4_wind"
  meditation_type: "evasive"
  effects:
    - "+20% Movement Speed"
    - "Unlock Wind Step"
    - "Enemy accuracy -25% against you"
  wisdom_teachings:
    - "The wind cannot be grasped"
    - " invisibility is the ultimate defense"
  convergence:
    - hell_circle_greed
```

## Shrine.fiverings.void (Void Shrine)
```yaml
Shrine.fiverings.void:
  name: "Void Shrine — Mu Meditation"
  description: "Transcend form, achieve nothingness"
  location: "Spaceport, Orbital Platform"
  book_requirement: "book5_void"
  meditation_type: "enlightenment"
  effects:
    - "Unlock All 7 Niten Stances"
    - "+50% Critical Damage"
    - "Time Dilation (10s combat slow-mo)"
    - "Void Walker: Phase through attacks"
  wisdom_teachings:
    - "The void contains all things"
    - "No-mind is the mind of the master"
  convergence:
    - hell_circle_wrath
    - lucifers_throne_trigger
```

---

## Schema
```yaml
*.Shrine.fiverings.*:
  type: record
  fields:
    name: string
    description: string
    location: string
    book_requirement: string (book1_ground | book2_water | book3_fire | book4_wind | book5_void)
    meditation_type: string (grounding | flowing | aggressive | evasive | enlightenment)
    effects: array[string]
    wisdom_teachings: array[string]
    convergence: array[string] (hell_circle_* | lucifers_throne_trigger)
```

---

## Meditation Mechanics

### Activation
```lua
// Approach shrine in world
// Press 'E' when prompt appears
// Minigame: Breathing rhythm (3-6-9 Hz Tesla pattern)
```

### Breathing Minigame
```
Inhale:  3 seconds (Tesla base)
Hold:    6 seconds (First harmonic)
Exhale:  9 seconds (Second harmonic)
Repeat:  3 cycles for full effect
```

### Wisdom Acquisition
Each shrine grants 1-2 "Wisdom Teachings" — collectible lore items that:
- Appear in journal
- Unlock dialogue options
- Provide permanent passive buffs
- Required for campaign convergence

---

## Convergence Mappings

| Shrine | Hell Circle | Trigger Condition |
|--------|-------------|-------------------|
| Earth | Limbo (1) | First meditation complete |
| Water | Lust (2) | Flow state achieved (3 cycles) |
| Fire | Gluttony (3) | Aggression channeled (damage dealt > 1000 in 10s) |
| Wind | Greed (4) | Untouchable perfect dodge (10+ consecutive) |
| Void | Wrath (5) | All previous shrines + Void stance unlocked |

**Circles 6-9** require Void Shrine completion + Lucifer's Throne events.