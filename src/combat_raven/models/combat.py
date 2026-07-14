from dataclasses import dataclass, field

from models.combatant import Combatant 

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

    def start(self) -> None:
        """
        Starts the combat encounter.
        """
        self.combatants.sort(
            key=lambda combatant: combatant.initiative,
            reverse=True,
        )

        self.current_round = 1
        self.current_turn = 0
        self.started = True