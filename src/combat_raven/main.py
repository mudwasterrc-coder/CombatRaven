import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from combat_raven.models.combat import Combat
from combat_raven.repositories.combat_repository import CombatRepository
from combat_raven.ui.main_window import MainWindow
from combat_raven.ui.theme import apply_theme


def main() -> None:
    app = QApplication(sys.argv)
    apply_theme(app)

    window = build_window(Path.home() / "CombatRaven" / "encounters")
    window.show()

    sys.exit(app.exec())

    if __name__ == "__main__":
        main()


def build_window(encounters_dir: Path) -> MainWindow:
    """
    Builds the main application window with an empty combat.
    """

    combat = Combat()
    repository = CombatRepository(encounters_dir)
    window = MainWindow(combat, repository)
    return window