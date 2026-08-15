from pathlib import Path

from combat_raven.models.combat import Combat
from combat_raven.storage.combat_storage import CombatStorage


class CombatRepository:
    """
    Manages saved combat encounters.
    """

    def __init__(self, directory: Path) -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def save(self, combat: Combat) -> None:
        """
        Saves a combat encounter using its ID as the filename.
        """
        storage = CombatStorage(
            self.directory / f"{combat.id}.json"
        )
        storage.save(combat)

    def get_by_id(self, combat_id: str) -> Combat | None:
        """
        Loads a combat encounter by ID.
        """
        path = self.directory / f"{combat_id}.json"

        if not path.exists():
            return None

        return CombatStorage(path).load()

    def list(self) -> list[Combat]:
        """
        Returns all saved combat encounters sorted by name
        """
        combats = []

        for path in self.directory.glob("*.json"):
            combat = CombatStorage(path).load()
            combats.append(combat)

        return sorted(
            combats,
            key=lambda combat: combat.name.lower(),
        )

    def delete(self, combat_id: str) -> None:
        """
        Deletes a saved combat encounter.
        """
        path = self.directory / f"{combat_id}.json"

        if path.exists():
            path.unlink()