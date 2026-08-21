from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout


class NewCombatDialog(QDialog):
    """
    Dialog for creating a new combat encounter.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("NEW ENCOUNTER")

        self.name_label = QLabel("ENCOUNTER NAME", self)
        self.name_input = QLineEdit(self)
        self.create_button = QPushButton("CREATE", self)
        self.cancel_button = QPushButton("CANCEL", self)

        self.create_button.clicked.connect(self._create_combat)
        self.cancel_button.clicked.connect(self.reject)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.create_button)
        self.button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addLayout(self.button_layout)

        self.setLayout(layout)
        

    def _create_combat(self) -> None:
        """
        Stores the entered encounter name and accepts the dialog.
        """
        name = self.name_input.text().strip()

        if not name:
            return

        self.selected_name = name
        self.accept()