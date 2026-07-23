# ADR-003

## Title

Effects advance at the beginning of a combatant's turn.

## Status

Accepted

## Context

Effects with durations need a deterministic moment to decrease their remaining duration.

Several options were considered:

- End of turn
- Beginning of turn
- End of round

## Decision

Effects advance when a combatant's turn begins.

Combat coordinates the turn transition and delegates effect management to Combatant.

Combat does not manipulate Effect objects directly.

## Consequences

Advantages

- Clear responsibility boundaries.
- Compatible with many D&D 5e effects.
- Easy to extend with reactions and other start-of-turn mechanics.

Trade-offs

Some game systems resolve durations differently and may require configurable timing in the future.