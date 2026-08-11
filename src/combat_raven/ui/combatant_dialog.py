from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QPushButton,
)

from combat_raven.models.combatant import Combatant


class CombatantDialog(QDialog):
    """
    Dialog for creating a combatant.
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Add Combatant")

        layout = QFormLayout(self)

        self.name_input = QLineEdit()

        self.max_hp_input = QSpinBox()
        self.max_hp_input.setRange(1, 9999)

        self.current_hp_input = QSpinBox()
        self.current_hp_input.setRange(0, 9999)

        self.initiative_input = QSpinBox()
        self.initiative_input.setRange(-100, 100)

        self.legendary_action_limit_input = QSpinBox()
        self.legendary_action_limit_input.setRange(0, 10)

        self.create_button = QPushButton("CREATE")
        self.create_button.clicked.connect(self.accept)

        layout.addRow("Name:", self.name_input)
        layout.addRow("Max HP:", self.max_hp_input)
        layout.addRow("Current HP:", self.current_hp_input)
        layout.addRow("Initiative:", self.initiative_input)
        layout.addRow(
            "Legendary Actions:",
            self.legendary_action_limit_input,
        )
        layout.addRow(self.create_button)

    def create_combatant(self) -> Combatant:
        """
        Creates a Combatant from the values entered in the dialog.
        """
        return Combatant(
            name=self.name_input.text(),
            max_hp=self.max_hp_input.value(),
            current_hp=self.current_hp_input.value(),
            initiative=self.initiative_input.value(),
            legendary_action_limit=(
                self.legendary_action_limit_input.value()
            ),
        )