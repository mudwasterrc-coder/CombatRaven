from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)

from combat_raven.models.combat import Combat
from combat_raven.models.combatant import Combatant
from combat_raven.ui.combatant_widget import CombatantWidget
from combat_raven.ui.combatant_dialog import CombatantDialog


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
        self.add_combatant_button = QPushButton("ADD COMBATANT")
        self.add_combatant_button.clicked.connect(
            self.open_combatant_dialog
        )

        self.end_turn_button.clicked.connect(self.end_turn)

        layout.addWidget(self.round_label)
        layout.addWidget(self.current_turn_label)
        layout.addLayout(self.combatants_layout)
        layout.addWidget(self.add_combatant_button)
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

        if self.combat.combatants:
            self.current_turn_label.setText(
                f"CURRENT TURN: {self.combat.current_combatant.name}"
            )
        else:
            self.current_turn_label.setText(
                "NO COMBATANTS"
            )

    def end_turn(self) -> None:
        """
        Advances the combat to the next turn and refreshes the UI.
        """
        self.combat.next_turn()
        self.refresh()

    def add_combatant(
        self,
        name: str,
        max_hp: int,
        current_hp: int,
        initiative: int,
        legendary_action_limit: int = 0,
    ) -> None:
        """
        Adds a combatant to the current combat and refreshes the UI.
        """
        combatant = Combatant(
            name=name,
            max_hp=max_hp,
            current_hp=current_hp,
            initiative=initiative,
            legendary_action_limit=legendary_action_limit,
        )

        self.combat.add_combatant(combatant)
        self.refresh()

    def open_combatant_dialog(self) -> None:
        """
        Opens the dialog for creating a new combatant.
        """
        dialog = CombatantDialog()

        if dialog.exec():
            combatant = dialog.create_combatant()
            self.combat.add_combatant(combatant)
            self.refresh()