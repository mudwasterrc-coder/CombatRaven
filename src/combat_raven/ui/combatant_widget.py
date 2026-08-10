from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel

from combat_raven.models.combatant import Combatant


class CombatantWidget(QFrame):
    """
    Visual representation of a combatant.
    """

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

        layout.addWidget(self.name_label)
        layout.addWidget(self.hp_label)
        layout.addWidget(self.initiative_label)

        self.refresh()

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

        if self.is_current:
            self.setStyleSheet(
                "QFrame { border: 2px solid #d4af37; border-radius: 8px; }"
            )
        else:
            self.setStyleSheet(
                "QFrame { border: 1px solid #666; border-radius: 8px; }"
            )