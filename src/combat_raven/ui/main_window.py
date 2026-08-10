from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)

from combat_raven.models.combat import Combat
from combat_raven.ui.combatant_widget import CombatantWidget


class MainWindow(QMainWindow):
    """
    Main application window for Combat Raven.
    """

    def __init__(self, combat: Combat) -> None:
        super().__init__()

        self.combat = combat

        self.setWindowTitle("Combat Raven")
        self.resize(1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.round_label = QLabel()
        self.current_turn_label = QLabel()
        self.combatants_layout = QHBoxLayout()
        self.end_turn_button = QPushButton("END TURN")

        self.end_turn_button.clicked.connect(self.end_turn)

        layout.addWidget(self.round_label)
        layout.addWidget(self.current_turn_label)
        layout.addLayout(self.combatants_layout)
        layout.addWidget(self.end_turn_button)

        self.refresh()

    def refresh(self) -> None:
        """
        Refreshes the combat information displayed by the UI.
        """
        self.round_label.setText(
            f"ROUND {self.combat.current_round}"
        )

        while self.combatants_layout.count():
            item = self.combatants_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        for combatant in self.combat.combatants:
            widget = CombatantWidget(
                combatant,
                is_current=(
                    combatant is self.combat.current_combatant
                ),
            )
            self.combatants_layout.addWidget(widget)

        self.current_turn_label.setText(
            f"CURRENT TURN: {self.combat.current_combatant.name}"
        )

    def end_turn(self) -> None:
        """
        Advances the combat to the next turn and refreshes the UI.
        """
        self.combat.next_turn()
        self.refresh()