import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from combat_raven.models.combat import Combat
from combat_raven.models.combatant import Combatant
from combat_raven.repositories.combat_repository import CombatRepository
from combat_raven.ui.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)

    combat = Combat()

    aaron = Combatant(
        name="Aaron",
        initiative=18,
        current_hp=87,
        max_hp=87,
    )

    strahd = Combatant(
        name="Strahd",
        initiative=22,
        current_hp=350,
        max_hp=350,
    )

    combat.add_combatant(aaron)
    combat.add_combatant(strahd)

    combat.start()

    repository = CombatRepository(
        Path.home() / "CombatRaven" / "encounters"
    )

    window = MainWindow(
        combat,
        repository,
    )
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()