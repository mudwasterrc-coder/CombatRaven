# Combat Raven Architecture

## Core Domain

### Combat

Responsible for coordinating combat.

Responsibilities:

- Manage combatants
- Determine initiative order
- Track rounds
- Track current turn
- Advance turns
- Trigger start-of-turn events

Combat never manipulates HP or effects directly.

---

### Combatant

Represents a creature participating in combat.

Responsibilities:

- Hit points
- Effects
- Conditions (future)
- Reactions (future)
- Legendary actions (future)

---

### Effect

Represents a single active effect.

Responsibilities:

- Remaining duration
- Tick duration
- Expiration

---

### EffectTemplate

Reusable blueprint used to create Effects.

Stores:

- Name
- Default duration
- Concentration requirement
- Notes