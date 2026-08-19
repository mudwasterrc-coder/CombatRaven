from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton


class NewCombatDialog(QDialog):
    """
    Dialog for creating a new combat encounter.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.name_input = QLineEdit(self)
        self.create_button = QPushButton("CREATE", self)
        self.create_button.clicked.connect(self._create_combat)

        self.cancel_button = QPushButton("CANCEL", self)

    def _create_combat(self) -> None:
        """
        Stores the entered encounter name and accepts the dialog.
        """
        name = self.name_input.text().strip()

        if not name:
            return

        self.selected_name = name
        self.accept()