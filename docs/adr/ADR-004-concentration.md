# ADR-004: Concentration held by the caster

## Status
Accepted (2026-10-07), not implemented yet.

## Context
In D&D, concentration is held by the caster, but the effect can be on other
combatants (e.g. Bless on three allies). When the caster loses concentration,
the effect ends on every target. The current model stores concentration on the
combatant that has the effect, so it cannot represent this.

## Decision
- Principle: the app keeps track, the DM decides. Only automate what is
  mechanical and easy to forget: round countdown and the concentration cascade.
- Every Combatant gets its own id.
- An Effect may have a source_id: the id of the combatant concentrating on it.
- Combat (not Combatant) applies and ends concentration, because it spans
  several combatants:
  - apply: creates one Effect per target with source_id = caster id; ends the
    caster's previous concentration first.
  - end: removes every effect whose source_id is the caster, on all combatants.
- Free-text effect name, optional duration, notes. No closed spell list.
- Persist combatant ids and effect source_id.
- The old Combatant concentration API is replaced step by step, then removed.

## Open questions
- Should durations tick on the caster's turn (RAW) or on the target's turn (current)?

## Update (2026-10-08): Dual-Focused and concentration limits
- Each Effect also has a concentration_id: one id per casting, shared by all
  its targets. A caster's concentrations are counted by distinct
  concentration_id, not by number of effects.
- Combatant.concentration_limit (default 1; 2 for Dual-Focused).
- At the limit: with limit 1 the previous concentration is dropped
  automatically; with a higher limit, apply_concentration raises ValueError
  and the UI must ask which concentration to drop (drop_concentration_by_id).
  The model never guesses.
- Implemented in the model: apply_concentration, drop_concentration,
  drop_concentration_by_id, concentration_ids_of.
- Pending: persistence, removing the old Combatant concentration API, UI,
  Dual-Focused round counter and DC display.