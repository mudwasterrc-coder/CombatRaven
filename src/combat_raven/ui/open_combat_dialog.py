from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)

from combat_raven.repositories.combat_repository import CombatRepository


class OpenCombatDialog(QDialog):
    """
    Dialog for selecting a saved combat encounter.
    """

    def __init__(
        self,
        repository: CombatRepository,
    ) -> None:
        super().__init__()

        self.repository = repository

        self.combat_list = QListWidget()

        self.cancel_button = QPushButton("CANCEL")
        self.cancel_button.clicked.connect(self.reject)

        self.open_button = QPushButton("OPEN")
        self.open_button.clicked.connect(self._open_selected_combat)

        self.delete_button = QPushButton("DELETE", self)
        self.delete_button.clicked.connect(
            self._delete_selected_combat
        )

        self._load_combats()

        layout = QVBoxLayout()
        layout.addWidget(self.combat_list)
        layout.addWidget(self.open_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def _load_combats(self) -> None:
        """
        Loads saved combats into the list.
        """
        self.combat_list.clear()
        
        for combat in self.repository.list():
            item = QListWidgetItem(combat.name)
            item.setData(Qt.ItemDataRole.UserRole, combat.id)
            self.combat_list.addItem(item)

    def _open_selected_combat(self) -> None:
        """
        Accepts the dialog only when a combat is selected
        """
        if self.selected_combat_id is None:
            return

        self.accept()

    @property
    def selected_combat_id(self) -> str | None:
        """
        Returns the ID of the currently selected combat, if any.
        """
        item = self.combat_list.currentItem()

        if item is None:
            return None

        return item.data(Qt.ItemDataRole.UserRole)

    def _delete_selected_combat(self) -> None:
        """
        Deletes the selected combat from the repository
        after confirmation.
        """
        combat_id = self.selected_combat_id

        if combat_id is None:
            return

        answer = QMessageBox.question(
            self,
            "DELETE ENCOUNTER",
            "Are you sure you want to delete this encounter?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        self.repository.delete(combat_id)
        self._load_combats()