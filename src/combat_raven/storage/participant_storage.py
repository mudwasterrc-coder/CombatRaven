import json
from pathlib import Path

from combat_raven.models.combatant import CombatantType
from combat_raven.models.participant_template import ParticipantTemplate
from combat_raven.repositories.participant_repository import (
    ParticipantRepository,
)


class ParticipantStorage:
    """
    Persists participant templates as JSON.
    """

    def __init__(self, path: Path) -> None:
        self.path = path

    def save(self, repository: ParticipantRepository) -> None:
        """
        Saves all participant templates to disk.
        """
        data = []

        for participant in repository.list():
            data.append(
                {
                    "id": participant.id,
                    "name": participant.name,
                    "combatant_type": participant.combatant_type.value,
                    "max_hp": participant.max_hp,
                    "legendary_action_limit": (
                        participant.legendary_action_limit
                    ),
                }
            )

        self.path.write_text(
            json.dumps(data, indent=4),
            encoding="utf-8",
        )

    def load(self) -> ParticipantRepository:
        """
        Loads participant templates from disk.
        """
        if not self.path.exists():
            return ParticipantRepository()
        
        repository = ParticipantRepository()

        data = json.loads(
            self.path.read_text(encoding="utf-8")
        )

        for item in data:
            participant = ParticipantTemplate(
                id=item["id"],
                name=item["name"],
                combatant_type=CombatantType(
                    item["combatant_type"]
                ),
                max_hp=item["max_hp"],
                legendary_action_limit=item[
                    "legendary_action_limit"
                ],
            )

            repository.add(participant)

        return repository