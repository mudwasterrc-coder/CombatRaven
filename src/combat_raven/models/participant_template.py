from dataclasses import dataclass
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
    legendary_action_limit: int = 0
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
            combatant_type=self.combatant_type,
        )