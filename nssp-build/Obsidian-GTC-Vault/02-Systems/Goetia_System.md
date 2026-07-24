# Goetia System

**Status:** 🟡 IN DEVELOPMENT (TweakDB sigils created, CET bindings pending)
**Systems:** `GoetiaBindingManager`, `GoetiaSummoningSystem`, `PandemoniumParliament`
**Source:** `scripts/goetia/msn_goetia_system.reds` (WIP), `tweakdb/msn_goetia_demons.tweakdb`

---

## Overview

The Goetia System brings the 72 demon lords of the *Ars Goetia* (Lesser Key of Solomon) into Cyberpunk 2077. Players can discover, summon, bind, and command these ancient entities across Night City. Integration with the [[Hell_Campaign|Hell Campaign]] provides context and progression for each demon.

Based on the 15th-century grimoire, each demon has:
- A unique sigil (collectible item)
- A rank in the infernal hierarchy
- Command over specific legions (spirit troops)
- Special abilities that transfer to the binder

---

## Binding System

Three methods to bind a demon:

### Combat
Defeat the demon in a boss encounter. Each demon Lord manifests in a specific Hell Circle or location. Harder demons (Kings, Dukes) require full party preparation and knowledge of their weaknesses.

- **Difficulty:** Scales with rank (President < Earl < Marquis < Prince < Duke < King)
- **Location:** Specific Hell Circle or Pandemonium arena
- **Reward:** Full binding + 100% ability transfer + Sigil of Binding
- **Risk:** Death resets binding progress, demon escapes

### Persuade
Use dialogue, offerings, and favors to negotiate a pact. Requires:
- Sufficient **Infernal Reputation** (earned through Hell Campaign progress)
- Appropriate **offerings per demon** (soul coins, artifacts, blood)
- Correct **approach** (each demon responds to different persuasion: flattery, threats, bargains, riddles)

### Bargain
Exchange resources for temporary or permanent binding:
| Resource | Binding Duration |
|----------|-----------------|
| 10 Soul Coins | Temporary (1 day) |
| 50 Soul Coins | Extended (1 week) |
| 250 Soul Coins + Artifact | Permanent |
| Infernal Pact + 500 Soul Coins | Full Pantheon Access |

---

## 9-Rank Hierarchy

The Goetic demons follow a strict hierarchy inherited from the *Ars Goetia*:

| Rank | Count | Authority | Command | Example |
|------|-------|-----------|---------|---------|
| **King** | 4 | Supreme | 66-200 legions | Bael, Paimon, Balam, Belial |
| **Duke** | ~12 | High | 26-36 legions | Agares, Dantalion, Zepar |
| **Prince** | ~8 | High | 20-26 legions | Stolas, Orobas, Seere |
| **Marquis** | ~14 | Medium | 20-30 legions | Andras, Phenex, Marchosias |
| **Earl/Count** | ~12 | Medium | 19-26 legions | Room, Bifrons, Ronove |
| **President** | ~8 | Medium-High | 29-72 legions | Foras, Asmoday, Buer |
| **Knight** | ~4 | Low | 18-26 legions | Furfur, Murmur |
| **Governor** | ~2 | Low | 4-26 legions | Zagan, Valefor |
| **Servitor** | ~8 | Lowest | 1-3 legions | Naberius, Glasya-Labolas |

---

## Integration with Hell Campaign

The Goetia system is deeply integrated with the 11 Hell Circles:

| Circle | Associated Demons | Theme |
|--------|------------------|-------|
| 0 — Limbo | Minor servitors, Governors | Entry, judgment |
| 1 — Lust | Zepar, Sitri, Lilith | Desire manipulation |
| 2 — Gluttony | Behemoth, Valefor | Consumption |
| 3 — Greed | Mammon, Bael (covetous aspect) | Wealth |
| 4 — Sloth | Belphegor, Morax | Entropy |
| 5 — Wrath | Andras, Marchosias, Sabnock | Combat |
| 6 — Heresy | Paimon, Ronove | Knowledge corruption |
| 7 — Violence | Amdusias, Bathin | Sound, weaponry |
| 8 — Fraud | Gaap, Dantalion | Deception |
| 9 — Treachery | Belial, | Betrayal |
| 10 — Pandemonium | All Kings + Lucifer | Parliament |

### Pandemonium Parliament

The Parliament is the governing body of Hell. Once all 72 demons are bound, the player can:
- Convene the Parliament at the Pandemonium Throne Room
- Vote on Infernal Proposals (gates, amnesty, market charter)
- Gain the title **Infernal Sovereign**
- Unlock the **True Ending** of the Hell Campaign

---

## Sigil Discovery and Crafting

Each of the 72 Goetic demons has a unique sigil stored as a TweakDB item. Sigils are acquired through:

### Discovery
- **World loot:** Found in Hell Circle chests, boss arenas, and Pandemonium vaults
- **Boss drops:** King and Duke-rank demons drop sigils on defeat
- **Quest rewards:** Goetia Collection questline awards sigils for completing sub-quests
- **Merchant purchase:** Available from the Infernal Quartermaster after reaching certain Hell Campaign milestones

### Crafting
Sigils can be crafted at the Infernal Altar using:
- **10 Soul Coins** + **1 Infernal Essence** (Common/Rare)
- **50 Soul Coins** + **5 Infernal Essence** (Epic)
- **250 Soul Coins** + **25 Infernal Essence** + **1 Demon Heart** (Legendary)

The crafting recipe is unlocked by starting the Hell Campaign (quest fact `msn_hell_campaign_started`).

---

## Summoning Rituals

Once a sigil is acquired and the demon is bound, summoning requires:

### Combat Summon
1. Equip the demon's sigil in your inventory
2. Ensure the binding is active (`msn.goetia.status`)
3. Use `msn.goetia.summon("name")` in combat
4. The demon fights alongside you for a duration proportional to binding strength

### Ritual Summon (Out of Combat)
1. Find a summoning circle (available in Hell Circles and the Apartment)
2. Place the sigil on the altar
3. Offer Soul Coins (1-10, affects duration)
4. Speak the demon's Enn (ritual incantation)
5. The demon manifests as a non-hostile NPC for dialogue and trade

---

## Demon Lords as NPCs

Bound demons can be summoned as NPC allies with:
- **Combat abilities:** Unique attacks based on the demon's lore
- **Dialogue trees:** Each demon has custom dialogue (persuasion, threats, bargaining)
- **Trade:** Demons offer unique items: Infernal Essence, Soul Coins, exclusive gear
- **Quests:** Some demons offer side quests that unlock additional abilities

### Demon Lord Stats
| Stat | Range | Notes |
|------|-------|-------|
| Health | 500-5000 | Kings have highest HP |
| Damage | 20-200 | Scales with rank |
| Duration | 30-300s | Extended by Soul Coin offerings |
| Cooldown | 300-3600s | Kings have longest cooldown |
| Special | 1-3 abilities | Unique per demon |

---

## Economy Impact

Binding demons affects the in-game economy:

### Soul Coin Costs
- **Binding:** 10-500 SC depending on rank
- **Summoning:** 1-10 SC per summon
- **Maintaining:** 1 SC/day per active binding (capped at 10 concurrent)

### Benefits
- **Passive income:** Bound Dukes generate 5 SC/day, Kings generate 25 SC/day
- **Combat advantage:** Summoned demons fight without cost
- **Territory control:** Legions can be assigned to Gang Warfare territories
- **Crafting:** Demons provide unique crafting reagents

---

## Integration with Other Systems

### Hell Campaign
Each bound demon advances the Hell Campaign:
- +1% campaign progress per non-King demon bound
- +5% per King bound
- All 72 bound = 100% → Pandemonium Parliament unlocked
- The 10 Pandemonium Lords (Asmodeus, Astaroth, Bael, Belial, Beelzebub, Mammon, Mephistopheles, Moloch, Paimon) gate specific campaign milestones

### Magic & Thaumaturgy
Demons interact with the magic system:
- **Conjuration school:** Summon demon requires a bound demon
- **Necromancy school:** Soul Coin generation boosted by bound death demons
- **Enchantment school:** Charm spells work better against non-bound demons
- **Abjuration school:** Angelic invocation (see [[Angelic_Hierarchy|Angelic Hierarchy]]) directly counters binding

### Gang Warfare
Demon legions can be assigned as gang troops:
- Each King commands 66-200 legion spirits
- Assigning legions to a territory grants +50% defense
- Demon-enhanced gang skirmishes have a chance to "curse" the enemy territory

---

## Progression Path

| Milestone | Requirement | Reward |
|-----------|-------------|--------|
| Novice Collector | Bind 1 demon | Sigil Pouch (holds 10 sigils) |
| Apprentice Binder | Bind 10 demons | Infernal Grimoire (art) |
| Journeyman | Bind 25 demons | Summon Shortcut (halved cooldown) |
| Expert | Bind 50 demons | Pandemonium Access |
| Master | Bind all 72 | Title: "Infernal Sovereign" |
| Grandmaster | Bind all + convene Parliament | True Ending access |

---

## CET Commands Reference

```lua
-- Binding Commands
msn.goetia.bind("bael")              -- Bind demon by Ars Goetia name
msn.goetia.summon("bael")            -- Summon a bound demon
msn.goetia.unbind("bael")            -- Release a demon binding
msn.goetia.status()                  -- Get all bindings status

-- Parliament Commands
msn.hell.vote("gates", "aye")        -- Vote in Pandemonium
msn.hell.lord("paimon", "persuade")  -- Challenge specific lord

-- Quests
msn.goetia.campaign.start()          -- Start Goetia collection
msn.goetia.bestiary()                -- View unlocked entries

-- Angelic (opposes binding)
msn.goetia.angel("aniel")            -- Invoke angelic protection
msn.goetia.angel.list()              -- List 72 Shem angels

-- LLM Integration
msn.llm.status()                     -- LLM bridge status
msn.llm.generate("prompt")           -- Generate code via LLM
msn.llm.redscript("desc")            -- Generate REDscript
msn.llm.models()                     -- List available models
```

---

## Lore Background

### The Lesser Key of Solomon

The *Ars Goetia* is the first section of *The Lesser Key of Solomon* (17th century), a grimoire attributed to King Solomon. It describes 72 demons summoned and sealed by Solomon in a bronze vessel. The text draws on earlier Jewish, Christian, and Islamic demonology.

### The 72 Seals

Each demon has a unique sigil (seal) that serves as their spiritual signature. In the original grimoire, these seals were drawn on parchment made from the skin of a virgin calf, using the blood of a black rooster and specific inks. The seals were placed inside a triangle of conjuration outside the magician's protective circle.

In-game, sigils function as:
- **Key items** that unlock the demon's binding quest
- **Crafting components** used at the Infernal Altar
- **Trophies** that can be displayed in the Apartment
- **Channeling foci** for summoning the bound demon

### Hierarchy from Pseudomonarchia Daemonum

The modern hierarchy derives from Johann Weyer's *Pseudomonarchia Daemonum* (1583), which was the primary source for the *Ars Goetia*. Weyer, a disciple of Agrippa, organized the demons into a structured infernal bureaucracy mirroring earthly royal courts.

### Modern Interpretations

- **Aleister Crowley** published the *Ars Goetia* with his own commentary in 1904, treating the demons as psychological archetypes
- **Golden Dawn** tradition associates each demon with a specific Tarot card and planetary influence
- **Occult revival** (1960s-present) treats the 72 demons as gates to subconscious power
- **Pop culture** influence on video games (Shin Megami Tensei, Persona series)

### In the Context of Night City

The demons have adapted to the Cyberpunk universe:
- **Bael** manifests as a tri-faced NetWatch AI with admin privileges
- **Paimon** operates through corporate boardrooms, possessing executives
- **Agares** causes seismic disruptions in the Badlands
- **Zepar** runs high-end braindance brothels in Jig-Jig Street

---

## See Also

### Sigils

Each demon has a unique sigil (seal) derived from the original grimoire. In-game, sigils are:
- Discovered as world loot in Hell Circles
- Craftable using Infernal Essence
- Required for summoning bindings
- Displayable in the Apartment

### Legions

Each demon commands a specific number of legions (spirit troops). A single legion in demonology = 1,000-6,666 spirits. In-game, legions translate to:
- Summonable allied NPCs during combat
- Territory control in Gang Warfare
- Workforce for Infernal Business operations

---

## See Also

- [[Goetia_Bestiary|Goetia Bestiary]] — Quick lookup of all 72 demons
- [[Angelic_Hierarchy|Angelic Hierarchy]] — 72 Shem HaMephorash angels
- [[Hell_Campaign|Hell Campaign]] — 11 Circles of Hell
- [[CET_Commands|CET Commands]] — Full command reference
- [[Magic_Thaumaturgy|Magic & Thaumaturgy]] — Spell schools

---

*Ars Goetia | 72 seals | Solomon's testament | Δ∞ − 1 = 0*
