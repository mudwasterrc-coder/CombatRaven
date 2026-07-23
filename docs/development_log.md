# Development Log

## 2026-07-23

### Feature

Effects now advance automatically when a combatant's turn begins.

### Tests

Added:

- test_next_turn_advances_new_current_combatants_effects()

### Result

12 tests passing.

### Notes

Combat now coordinates turn flow while Combatant remains responsible for managing its own active effects.

## 2026-07-23

### Added
- Reaction management for Combatant.
- Reaction reset at turn start.
- Concentration state management.

### Tests
- Added unit tests for reactions.
- Added integration test for turn-start reaction reset.
- Added unit tests for concentration state.

Status:
15 tests passing.