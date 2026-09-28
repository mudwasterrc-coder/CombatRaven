from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QListWidget, QListWidgetItem, QPushButton

from combat_raven.repositories.participant_repository import ParticipantRepository


class AddParticipantDialog(QDialog):
    """
    Dialog for selecting a participant template to add to combat.
    """

    def __init__(
        self,
        repository: ParticipantRepository,
    ) -> None:
        super().__init__(None)

        self.repository = repository
        self.participant_list = QListWidget()

        self.add_button = QPushButton("ADD")
        self.cancel_button = QPushButton("CANCEL")

        self.add_button.clicked.connect(self._add_selected_participant)
        self.cancel_button.clicked.connect(self.reject)

        self._load_participants()

    def _load_participants(self) -> None:
        """
        Loads participant templates into the list.
        """
        for participant in self.repository.list():
            item = QListWidgetItem(participant.name)
            item.setData(Qt.ItemDataRole.UserRole, participant.id,)
            self.participant_list.addItem(item)

    @property
    def selected_participant_id(self) -> str | None:
        """
        Returns the ID of the selected participant template.
        """
        item = self.participant_list.currentItem()

        if item is None:
            return None

        return item.data(Qt.ItemDataRole.UserRole)

    def _add_selected_participant(self) -> None:
        """
        Accepts the dialog only when a participant is selected.
        """
        if self.selected_participant_id is None:
            return

        self.accept()