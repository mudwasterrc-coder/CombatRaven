from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QListWidget, QListWidgetItem, QSpinBox
from PySide6.QtCore import Qt

from combat_raven.models.combatant import Combatant
from combat_raven.models.effect_template import EffectTemplate

class ConcentrationDialog(QDialog):
    """
    Dialog for starting a concentration effect.
    """

    def __init__(self, candidates: list[Combatant] | None = None, parent=None) -> None:
        super().__init__(parent)

        self.candidates = candidates or []
        

        self.setWindowTitle("CONCENTRATE")

        layout = QFormLayout(self)

        self.name_input = QLineEdit()

        self.duration_input = QSpinBox()
        self.duration_input.setRange(0, 9999)
        self.duration_input.setSpecialValueText("∞")

        self.target_list = QListWidget()
        for candidate in self.candidates:
            item = QListWidgetItem(candidate.name)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.target_list.addItem(item)

        layout.addRow("Effect Name:", self.name_input)
        layout.addRow("Duration (rounds):", self.duration_input)
        layout.addRow("Targets:", self.target_list)

    def create_template(self) -> EffectTemplate:
        """
        Creates a concentration effect template from the dialog inputs.
        """
        name = self.name_input.text().strip()
        duration = self.duration_input.value()

        return EffectTemplate(
            name=name,
            default_duration=None if duration == 0 else duration,
            concentration=True
        )

    def selected_targets(self) -> list[Combatant]:
        """
        Returns the candidates whose checkbox is checked.
        """

        targets = []

        for row in range(self.target_list.count()):
            item = self.target_list.item(row)

            if item.checkState() == Qt.CheckState.Checked:
                targets.append(self.candidates[row])

        return targets