from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
)

from combat_raven.models.combat import Combat
from combat_raven.models.combatant import Combatant
from combat_raven.ui.combatant_widget import CombatantWidget
from combat_raven.ui.combatant_dialog import CombatantDialog
from combat_raven.ui.combatants_container import CombatantsContainer
from combat_raven.repositories.combat_repository import CombatRepository
from combat_raven.ui.open_combat_dialog import OpenCombatDialog


class MainWindow(QMainWindow):
    """
    Main application window for Combat Raven.
    """

    def __init__(
            self,
            combat: Combat,
            combat_repository: CombatRepository | None = None,
            ) -> None:
        super().__init__()

        self.combat = combat
        self.combat_repository = combat_repository

        self.setWindowTitle("Combat Raven")
        self.resize(1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.round_label = QLabel()
        self.current_turn_label = QLabel()
        self.combatants_scroll_area = QScrollArea()
        self.combatants_scroll_area.setWidgetResizable(True)
        self.combatants_container = CombatantsContainer()
        self.combatants_layout = QVBoxLayout(
            self.combatants_container
        )
        self.combatants_scroll_area.setWidget(
            self.combatants_container
        )

        self.combatants_container.drop_requested.connect(
            self.move_combatant
        )

        self.end_turn_button = QPushButton("END TURN")
        self.add_combatant_button = QPushButton("ADD COMBATANT")
        self.save_combat_button = QPushButton("SAVE COMBAT")
        self.save_combat_button.clicked.connect(
            self.save_combat
        )
        self.open_combat_button = QPushButton("OPEN ENCOUNTER")
        self.add_combatant_button.clicked.connect(
            self.open_combatant_dialog
        )

        self.end_turn_button.clicked.connect(self.end_turn)
        self.sort_by_initiative_button = QPushButton("SORT BY INITIATIVE")
        self.sort_by_initiative_button.clicked.connect(
            self.sort_by_initiative
        )

        layout.addWidget(self.round_label)
        layout.addWidget(self.current_turn_label)
        layout.addWidget(self.combatants_scroll_area)
        layout.addWidget(self.sort_by_initiative_button)
        layout.addWidget(self.add_combatant_button)
        layout.addWidget(self.save_combat_button)
        layout.addWidget(self.open_combat_button)
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

            widget.remove_requested.connect(
                self.remove_combatant
            )

            widget.move_requested.connect(
                self.move_combatant
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

    def remove_combatant(self, combatant: Combatant) -> None:
        """
        Removes a combatant from the current combat and refreshes the UI.
        """
        self.combat.remove_combatant(combatant)
        self.refresh()

    def move_combatant(
        self,
        combatant: Combatant,
        new_index: int,
    ) -> None:
        """
        Moves a combatant to a new position and resfreshes the UI.
        """
        self.combat.move_combatant(
            combatant,
            new_index,
        )
        self.refresh()

    def sort_by_initiative(self) -> None:
        """
        Sorts combatants by initiative and refreshes the UI.
        """
        self.combat.sort_by_initiative()
        self.refresh()

    def save_combat(self) -> None:
        """
        Saves the current combat through the combat repository.
        """
        if self.combat_repository is None:
            raise RuntimeError(
                "Cannot save combat without a combat repository."
            )

        self.combat_repository.save(self.combat)

    def open_combat(self) -> None:
        """
        Opens the dialog for selecting a saved combat encounter.
        """
        self.open_combat_dialog = OpenCombatDialog(
            self.combat_repository
        )

        self.open_combat_dialog.accepted.connect(
            self._load_selected_combat
        )

        self.open_combat_dialog.show()

    def _load_selected_combat(self) -> None:
        """
        Loads the combat selected in the open combat dialog.
        """
        combat_id = self.open_combat_dialog.selected_combat_id

        if combat_id is None:
            return

        combat = self.combat_repository.get_by_id(combat_id)

        if combat is None:
            return

        self.combat = combat
        self.refresh()