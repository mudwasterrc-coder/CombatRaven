from combat_raven.models.combatant import Combatant
from combat_raven.ui.combatant_widget import CombatantWidget
from combat_raven.ui.combatants_container import CombatantsContainer

from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import QPoint


class FakeDragEvent:
    def __init__(self, source=None):
        self._source = source
        self.accepted = False

    def source(self):
        return self._source

    def acceptProposedAction(self):
        self.accepted = True

    def ignore(self):
        self.accepted = False

    def isAccepted(self):
        return self.accepted

class FakeDropEvent:
    def __init__(self, source=None):
        self._source = source
        self.accepted = False

    def source(self):
        return self._source

    def acceptProposedAction(self):
        self.accepted = True

    def ignore(self):
        self.accepted = False

    def position(self):
        return QPoint(0, 0)

def test_combatants_container_accepts_drops(qtbot):
    container = CombatantsContainer()
    qtbot.addWidget(container)

    assert container.acceptDrops() is True

def test_combatants_container_accepts_combatant_drag(qtbot):
    container = CombatantsContainer()
    qtbot.addWidget(container)

    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    event = FakeDragEvent(widget)

    container.dragEnterEvent(event)

    assert event.isAccepted()

def test_combatants_container_rejects_non_combatant_drag(qtbot):
    container = CombatantsContainer()
    qtbot.addWidget(container)

    event = FakeDragEvent()

    container.dragEnterEvent(event)

    assert not event.isAccepted()

def test_combatants_container_can_receive_combatant_drop(qtbot):
    container = CombatantsContainer()
    qtbot.addWidget(container)

    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    event = FakeDropEvent(widget)

    container.dropEvent(event)

    assert event.accepted

def test_combatants_container_calculates_drop_index(qtbot):
    container = CombatantsContainer()
    qtbot.addWidget(container)

    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    wizard = Combatant(
        name="Wizard",
        initiative=10,
        current_hp=20,
        max_hp=20,
    )

    fighter_widget = CombatantWidget(fighter)
    wizard_widget = CombatantWidget(wizard)

    qtbot.addWidget(fighter_widget)
    qtbot.addWidget(wizard_widget)

    layout = QVBoxLayout(container)
    layout.addWidget(fighter_widget)
    layout.addWidget(wizard_widget)

    fighter_widget.show()
    wizard_widget.show()
    container.show()

    qtbot.waitExposed(container)

    index = container.drop_index_at(
        wizard_widget.geometry().center()
    )

    assert index == 1

def test_combatants_container_returns_zero_for_drop_above_first(
    qtbot,
):
    container = CombatantsContainer()
    qtbot.addWidget(container)

    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    fighter_widget = CombatantWidget(fighter)
    qtbot.addWidget(fighter_widget)

    layout = QVBoxLayout(container)
    layout.addWidget(fighter_widget)

    fighter_widget.show()
    container.show()

    qtbot.waitExposed(container)

    position = fighter_widget.geometry().topLeft()

    assert container.drop_index_at(position) == 0

def test_combatants_container_returns_count_for_drop_below_last(
    qtbot,
):
    container = CombatantsContainer()
    qtbot.addWidget(container)

    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    fighter_widget = CombatantWidget(fighter)
    qtbot.addWidget(fighter_widget)

    layout = QVBoxLayout(container)
    layout.addWidget(fighter_widget)

    fighter_widget.show()
    container.show()

    qtbot.waitExposed(container)

    position = fighter_widget.geometry().bottomLeft()

    assert container.drop_index_at(position) == 1

def test_combatants_container_emits_drop_request(qtbot):
    container = CombatantsContainer()
    qtbot.addWidget(container)

    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    received = []

    container.drop_requested.connect(
        lambda combatant, index: received.append(
            (combatant, index)
        )
    )

    event = FakeDropEvent(widget)

    container.drop_index_at = lambda position: 1

    container.dropEvent(event)

    assert received == [(fighter, 1)]