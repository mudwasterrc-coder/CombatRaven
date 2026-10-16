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

## 2026-10-02

### Added (branch feature/damage-healing)
- Damage and healing from each combatant card (amount input + DAMAGE / HEAL buttons).
- Enter in the amount input applies damage (lineEdit returnPressed, not editingFinished, to avoid accidental damage on focus loss).
- Amount resets to 0 after applying damage or healing.
- HP label shows "(DOWN)" at 0 HP.

### Changed
- Renamed Combatant.is_dead to is_down (0 HP means unconscious for PCs, not always dead).
- Fixed .gitignore rules.

### Refactor
- Shared HP change follow-up between damage and healing.

### Tests
235 passing.

### Next
- START button to begin combat from the UI.
- Apply / remove effects from the UI.

## 2026-10-07

### Added (branch feature/start-combat)
- START COMBAT button: sorts by initiative, sets round 1, marks unsaved changes.
- START is enabled only before the combat starts and when there are combatants.
- END TURN is enabled only after the combat starts.

### Fixed
- Combat.start() does nothing when there are no combatants (avoids a stuck "started" empty encounter).

### Tests
240 passing.

### Next
- Apply / remove effects from the UI.
- Pending: new concentration should end the previous one, drag down off by one, label borders, compact cards, app starts with demo combat / unnamed save.

## 2026-10-08 to 2026-10-13

### Added (branch feature/concentration)
- Each combatant has its own id.
- Effects know who sustains them (source_id) and which casting they belong to (concentration_id).
- Combat.apply_concentration: one effect copy per target; with limit 1 the new concentration ends the previous one.
- Combat.drop_concentration (all of a caster's) and drop_concentration_by_id (a single one).
- Combatant.concentration_limit (Dual-Focused = 2). At a higher limit the model refuses and the UI must ask what to drop.
- Concentration ids and links are saved and loaded.
- Combatant cards show effects with remaining rounds, "∞" for effects without duration.

### Removed
- Old Combatant-held concentration API (replaced by the Combat-level model, see ADR-004).

### Tests
247 passing.

### Next
- Card for the caster shows "Concentrating: ..." (needs combat context in the widget).
- CONCENTRATE dialog (name, duration, targets) and DROP CONCENTRATION button.
- Ask to drop concentration when a concentrating caster drops to 0 HP.

## 2026-10-16

### Added (branch feature/concentration)
- Combat.concentration_names_of(caster).
- Combatant cards show "Concentrating: ..." (caster) and "Bless (10) from Cleric" (targets).
  Design: cards stay dumb; MainWindow asks the Combat and passes plain data (ADR-004, option B).
- DROP CONCENTRATION button on cards: enabled only when concentrating, emits a request, MainWindow drops it.
- ConcentrationDialog (WIP): effect name and rounds; 0 rounds shows "∞" and means no limit.

### Tests
257 passing.

### Next
- - ConcentrationDialog: targets with checkboxes, APPLY / CANCEL. (Decided: opens at ∞ by default.)
- CONCENTRATE button on cards opening the dialog.
- Dual-Focused: ask what to drop when at the limit.
- Ask to drop concentration when a concentrating caster drops to 0 HP.