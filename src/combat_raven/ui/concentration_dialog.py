from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QSpinBox

from combat_raven.models.effect_template import EffectTemplate

class ConcentrationDialog(QDialog):
    """
    Dialog for starting a concentration effect.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("CONCENTRATE")

        layout = QFormLayout(self)

        self.name_input = QLineEdit()

        self.duration_input = QSpinBox()
        self.duration_input.setRange(0, 9999)
        self.duration_input.setSpecialValueText("∞")

        layout.addRow("Effect Name:", self.name_input)
        layout.addRow("Duration (rounds):", self.duration_input)

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