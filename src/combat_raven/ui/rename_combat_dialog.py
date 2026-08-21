from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout


class RenameCombatDialog(QDialog):
    """
    Dialog for renaming a saved combat encounter.
    """

    def __init__(
        self,
        current_name: str,
    ) -> None:
        super().__init__()

        self.setWindowTitle("RENAME ENCOUNTER")

        self.current_name = current_name

        self.name_input = QLineEdit()
        self.name_input.setText(current_name)

        self.rename_button = QPushButton("RENAME")
        self.cancel_button = QPushButton("CANCEL")

        self.rename_button.clicked.connect(
            self._rename
        )

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.rename_button)
        self.button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addWidget(self.name_input)
        layout.addLayout(self.button_layout)

        self.setLayout(layout)

    def _rename(self) -> None:
        """
        Stores the entered name and accepts the dialog.
        """
        name = self.name_input.text().strip()

        if not name:
            return

        self.selected_name = name
        self.accept()
