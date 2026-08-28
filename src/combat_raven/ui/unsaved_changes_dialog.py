from PySide6.QtWidgets import (
    QDialog,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)


class UnsavedChangesDialog(QDialog):
    """
    Dialog shown when an encounter has unsaved changes.
    """

    def __init__(self) -> None:
        super().__init__()
        self.selected_action = None
        self.setWindowTitle("UNSAVED CHANGES")

        self.save_button = QPushButton("SAVE")
        self.discard_button = QPushButton("DISCARD")
        self.cancel_button = QPushButton("CANCEL")

        self.cancel_button.clicked.connect(self.reject)
        self.discard_button.clicked.connect(self._discard)
        self.save_button.clicked.connect(
            self._save
        )

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.discard_button)
        self.button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addLayout(self.button_layout)

        self.setLayout(layout)

    def _save(self) -> None:
        """
        Marks the SAVE action and accepts the dialog.
        """
        self.selected_action = "save"
        self.accept()

    def _discard(self) -> None:
        """
        Marks the DISCARD action and accepts the dialog.
        """
        self.selected_action = "discard"
        self.accept()