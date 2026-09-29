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

## 2026-09-28

### Fixed (branch fix/core-bugs)
- Combatants and effects compare by identity (duplicate goblins / Bless removed correctly).
- Combat storage now persists legendary action limit, legendary actions used, reaction and concentration target.
- Effects without duration no longer crash when advancing turns.
- Next turn with no combatants does nothing instead of crashing.
- Sorting by initiative keeps the turn on the same combatant.

### Tests
218 passing.

### Next
UI bugs: unsaved changes (ADD / END TURN / closeEvent), rename CANCEL, rename overwritten on save, default current HP 0.

## 2026-09-29

### Fixed (branch fix/ui-bugs)
- Unsaved changes flag is set by ADD COMBATANT, END TURN, reactions and legendary actions (CombatantWidget.changed signal).
- Closing the window asks what to do with unsaved changes (SAVE / DISCARD / CANCEL).
- Rename dialog CANCEL button works.
- Renaming the open encounter keeps MainWindow in sync (OpenCombatDialog.combat_renamed signal).
- Current HP follows max HP in the combatant dialog.

### Refactor
- Extracted open combat dialog setup into a single method.

### Tests
228 passing. Replaced a cancel test that could never fail.

### Next
- Phase 2: damage/healing from the UI, START button, apply/remove effects.
- Pending: new concentration should end the previous one, drag down off by one, label borders, compact cards, app starts with demo combat / unnamed save.