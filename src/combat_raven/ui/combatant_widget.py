from PySide6.QtWidgets import (QFrame, QVBoxLayout, QLabel, QPushButton, QSpinBox, QApplication)

from combat_raven.models.combatant import Combatant
from PySide6.QtCore import Qt, Signal, QMimeData
from PySide6.QtGui import QDrag


class CombatantWidget(QFrame):
    """
    Visual representation of a combatant.
    """
    remove_requested = Signal(Combatant)
    move_requested = Signal(Combatant, int)
    changed = Signal()
    drop_concentration_requested = Signal(Combatant)
    concentrate_requested = Signal(Combatant)
    went_down = Signal(Combatant)

    def __init__(
        self,
        combatant: Combatant,
        is_current: bool = False,
        concentrating_on: list[str] | None = None,
        source_names: dict[str, str] | None = None,
    ) -> None:
        super().__init__()

        self.combatant = combatant
        self.is_current = is_current
        self.concentrating_on = concentrating_on or []
        self.source_names = source_names or {}
        self.drag_start_position = None

        layout = QVBoxLayout(self)

        self.name_label = QLabel()
        self.hp_label = QLabel()
        self.effects_label = QLabel()
        self.initiative_label = QLabel()
        self.reaction_label = QLabel()
        self.concentration_label = QLabel()
        self.legendary_action_label = QLabel()

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

        self.concentrate_button = QPushButton("CONCENTRATE")
        self.concentrate_button.clicked.connect(
            lambda: self.concentrate_requested.emit(self.combatant)
        )

        self.drop_concentration_button = QPushButton("DROP CONCENTRATION")
        self.drop_concentration_button.clicked.connect(
            lambda: self.drop_concentration_requested.emit(self.combatant)
        )

        self.damage_button = QPushButton("DAMAGE")
        self.damage_button.clicked.connect(self.apply_damage)

        self.heal_button = QPushButton("HEAL")
        self.heal_button.clicked.connect(self.apply_healing)

        self.amount_input = QSpinBox()
        self.amount_input.setRange(0, 9999)
        self.amount_input.lineEdit().returnPressed.connect(self.apply_damage)

        

        layout.addWidget(self.name_label)
        layout.addWidget(self.hp_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.damage_button) 
        layout.addWidget(self.heal_button)       
        layout.addWidget(self.initiative_label)
        layout.addWidget(self.reaction_label)
        layout.addWidget(self.legendary_action_label)
        layout.addWidget(self.effects_label)
        layout.addWidget(self.concentration_label)
        layout.addWidget(self.concentrate_button)
        layout.addWidget(self.drop_concentration_button)
        layout.addWidget(self.use_reaction_button)
        layout.addWidget(self.use_legendary_action_button)
        self.refresh()
        layout.addWidget(self.remove_button)
        

    def refresh(self) -> None:
        """
        Refreshes the information displayed for the combatant.
        """
        self.name_label.setText(self.combatant.name)

        hp_text = f"HP: {self.combatant.current_hp} / {self.combatant.max_hp}"

        if self.combatant.is_down:
            hp_text += " (DOWN)"

        self.hp_label.setText(hp_text)

        effects_text = []
        for effect in self.combatant.effects:
            if effect.remaining_rounds is None:
                text = f"{effect.template.name} (∞)"
            else:
                text = f"{effect.template.name} ({effect.remaining_rounds})"

            if effect.source_id in self.source_names:
                text += f" from {self.source_names[effect.source_id]}"

            effects_text.append(text)

        self.effects_label.setText(", ".join(effects_text))

        if self.concentrating_on:
            self.concentration_label.setText(
                f"Concentrating: {', '.join(self.concentrating_on)}"
            )
            self.drop_concentration_button.setEnabled(True)
        else:
            self.concentration_label.setText("")
            self.drop_concentration_button.setEnabled(False)

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
        self.changed.emit()

    def use_legendary_action(self) -> None:
        """
        Uses one legendary action and refreshes the widget.
        """
        self.combatant.use_legendary_action()
        self.refresh()
        self.changed.emit()

    def request_move(self, index: int) -> None:
        """
        Requests that this combatant be moved to a new position.
        """
        self.move_requested.emit(self.combatant, index)

    def mousePressEvent(self, event) -> None:
        """
        Stores the starting position for a possible drag operation.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position().toPoint()

        super().mousePressEvent(event)

    def should_start_drag(self, position) -> bool:
        """
        Returns whether the mouse has moved far enough to start a drag.
        """
        if self.drag_start_position is None:
            return False

        distance = (position - self.drag_start_position)

        return (
            abs(distance.x()) >= QApplication.startDragDistance()
            or abs(distance.y()) >= QApplication.startDragDistance()
        )

    def mouseMoveEvent(self, event) -> None:
        """
        Starts a drag operation when the mouse moves far enough.
        """
        if (
            event.buttons() & Qt.MouseButton.LeftButton
            and self.should_start_drag(
                event.position().toPoint()
            )
        ):
            self.start_drag()

        super().mouseMoveEvent(event)

    def create_drag(self) -> QDrag:
        """
        Creates a drag operation for this combatant.
        """
        drag = QDrag(self)

        mime_data = QMimeData()
        drag.setMimeData(mime_data)

        return drag

    def start_drag(self) -> None:
        """
        Starts a drag operation for this combatant.
        """
        drag = self.create_drag()
        drag.exec()

    def apply_damage(self) -> None:
        """
        Applies the entered amount as damage to the combatant.
        """
        was_standing = not self.combatant.is_down

        self.combatant.damage(self.amount_input.value())

        if was_standing and self.combatant.is_down:
            self.went_down.emit(self.combatant)
        
        self._finish_hp_change()

    def apply_healing(self) -> None:
        """
        Applies the entered amount as healing to the combatant.
        """
        self.combatant.heal(self.amount_input.value())
        self._finish_hp_change()

    def _finish_hp_change(self) -> None:
        """
        Clears the amount and updates the widget after an HP change.
        """
        self.amount_input.setValue(0)
        self.refresh()
        self.changed.emit()