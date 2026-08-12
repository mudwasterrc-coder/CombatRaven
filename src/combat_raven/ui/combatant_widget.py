from PySide6.QtWidgets import (QFrame, QVBoxLayout, QLabel, QPushButton)

from combat_raven.models.combatant import Combatant
from PySide6.QtCore import Signal


class CombatantWidget(QFrame):
    """
    Visual representation of a combatant.
    """
    remove_requested = Signal(Combatant)
    move_requested = Signal(Combatant, int)

    def __init__(
        self,
        combatant: Combatant,
        is_current: bool = False,
    ) -> None:
        super().__init__()

        self.combatant = combatant
        self.is_current = is_current

        layout = QVBoxLayout(self)

        self.name_label = QLabel()
        self.hp_label = QLabel()
        self.initiative_label = QLabel()
        self.reaction_label = QLabel()
        self.use_reaction_button = QPushButton("USE REACTION")
        self.use_reaction_button.clicked.connect(self.use_reaction)
        self.use_legendary_action_button = QPushButton(
            "USE LEGENDARY ACTION"
        )
        self.remove_button = QPushButton("REMOVE")
        self.remove_button.clicked.connect(
            lambda: self.remove_requested.emit(self.combatant)
        )
        self.use_legendary_action_button.clicked.connect(
            self.use_legendary_action
        )
        self.legendary_action_label = QLabel()

        layout.addWidget(self.name_label)
        layout.addWidget(self.hp_label)
        layout.addWidget(self.initiative_label)
        layout.addWidget(self.reaction_label)
        layout.addWidget(self.legendary_action_label)
        layout.addWidget(self.use_reaction_button)
        layout.addWidget(self.use_legendary_action_button)
        self.refresh()
        layout.addWidget(self.remove_button)

    def refresh(self) -> None:
        """
        Refreshes the information displayed for the combatant.
        """
        self.name_label.setText(self.combatant.name)

        self.hp_label.setText(
            f"HP: {self.combatant.current_hp} / {self.combatant.max_hp}"
        )

        self.initiative_label.setText(
            f"Initiative: {self.combatant.initiative}"
        )

        reaction_status = (
            "AVAILABLE"
            if self.combatant.can_react()
            else "USED"
        )

        self.reaction_label.setText(
            f"Reaction: {reaction_status}"
        )

        self.legendary_action_label.setText(
            f"Legendary Actions: "
            f"{self.combatant.legendary_actions_used} / "
            f"{self.combatant.legendary_action_limit}"
        )

        self.use_legendary_action_button.setEnabled(
            self.combatant.can_use_legendary_action()
        )

        self.use_reaction_button.setEnabled(
                    self.combatant.can_react()
                )

        if self.is_current:
            self.setStyleSheet(
                "QFrame { border: 2px solid #d4af37; border-radius: 8px; }"
            )
        else:
            self.setStyleSheet(
                "QFrame { border: 1px solid #666; border-radius: 8px; }"
            )

    def use_reaction(self) -> None:
        """
        Uses the combatant's reaction and refreshes the widget.
        """
        self.combatant.use_reaction()
        self.refresh()

    def use_legendary_action(self) -> None:
        """
        Uses one legenday action and refreshes the widget.
        """
        self.combatant.use_legendary_action()
        self.refresh()

    def request_move(self, index: int) -> None:
        """
        Requests that this combatant be moved to a new position.
        """
        self.move_requested.emit(self.combatant, index)
