from dataclasses import dataclass
import random
from uuid import uuid4

from combat_raven.models.combatant import Combatant, CombatantType


@dataclass
class ParticipantTemplate:
    """
    Reusable participant definition.
    """

    name: str
    combatant_type: CombatantType
    max_hp: int
    initiative_bonus: int = 0
    legendary_action_limit: int = 0
    concentration_limit: int = 1
    id: str = None

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = str(uuid4())

    def create_combatant(self, initiative: int) -> Combatant:
        """
        Creates a new combatant instance from this template.
        """
        return Combatant(
            name=self.name,
            initiative=initiative,
            current_hp=self.max_hp,
            max_hp=self.max_hp,
            legendary_action_limit=self.legendary_action_limit,
            concentration_limit=self.concentration_limit,
            combatant_type=self.combatant_type,
        )

    def roll_initiative(self, d20=lambda: random.randint(1, 20)) -> int:
        """
        Rolls initiative: a d20 plus this template's initiative bonus.
        """
        return d20() + self.initiative_bonus