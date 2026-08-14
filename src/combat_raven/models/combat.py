from dataclasses import dataclass, field
from operator import index

from combat_raven.models.combatant import Combatant 

@dataclass
class Combat:
    """
    Represents an ongoing combat encounter.
    """
    combatants: list[Combatant] = field(default_factory=list)

    current_round: int = 0

    current_turn_index: int = 0

    started: bool = False

    def add_combatant(self, combatant: Combatant) -> None:
        """
        Adds a combatant to the encounter.
        """
        self.combatants.append(combatant)

    def remove_combatant(self, combatant: Combatant) -> None:
        """
        Removes a combatant from the encounter.
        """
        index = self.combatants.index(combatant)

        self.combatants.remove(combatant)

        if index < self.current_turn_index:
            self.current_turn_index -= 1

        if self.current_turn_index >= len(self.combatants):
            self.current_turn_index = 0

    def move_combatant(
            self,
            combatant: Combatant,
            new_index: int,
    ) -> None:
        """
        Moves a combatant to a new position in the encounter order.
        """
        old_index = self.combatants.index(combatant)
        moving_current = old_index == self.current_turn_index

        self.combatants.remove(combatant)
        self.combatants.insert(new_index, combatant)

        if moving_current:
            self.current_turn_index = new_index

        elif old_index < self.current_turn_index <= new_index:
            self.current_turn_index -= 1

        elif new_index <= self.current_turn_index < old_index:
            self.current_turn_index += 1

    def start(self) -> None:
        """
        Starts the combat encounter.
        """
        self.combatants.sort(
            key=lambda combatant: combatant.initiative,
            reverse=True,
        )

        self.current_round = 1
        self.current_turn_index = 0
        self.started = True

    @property
    def current_combatant(self) -> Combatant:
        """
        Returns the combatant whose turn it currently is.
        """

        return self.combatants[self.current_turn_index]
    
    def next_turn(self) -> None:
        """
        Advances to the next combatant's turn.
        """
        self.current_turn_index += 1

        if self.current_turn_index >= len(self.combatants):
            self.current_turn_index = 0
            self.current_round += 1

            for combatant in self.combatants:
                combatant.reset_legendary_actions()

        self.current_combatant.advance_effects()
        self.current_combatant.reset_reaction()

    def sort_by_initiative(self) -> None:
        """
        Sorts combatants by initiative, in descending order.
        """
        self.combatants.sort(
            key=lambda combatant: combatant.initiative,
            reverse=True,
        )

    def restore_state(
        self,
        current_round: int,
        current_turn_index: int,
    ) -> None:
        """
        Restores an existing combat to a previously saved state.
        """
        if not self.combatants:
            raise ValueError("Cannot restore a combat with no combatants.")

        if not 0 <= current_turn_index < len(self.combatants):
            raise ValueError(
                "Current turn index is out of range."
            )

        if current_round < 1:
            raise ValueError(
                "Current round must be at least 1."
            )

        self.current_round = current_round
        self.current_turn_index = current_turn_index
        self.started = True