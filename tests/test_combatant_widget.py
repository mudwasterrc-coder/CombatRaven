from combat_raven.models.combatant import Combatant
from combat_raven.ui.combatant_widget import CombatantWidget
from combat_raven.models.combat import Combat
from PySide6.QtCore import QPoint
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent


def test_combatant_widget_can_use_reaction(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    assert fighter.can_react() is True

    widget.use_reaction_button.click()

    assert fighter.can_react() is False

def test_combatant_widget_disables_reaction_button_after_use(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    widget.use_reaction_button.click()

    assert fighter.can_react() is False
    assert widget.use_reaction_button.isEnabled() is False

def test_combatant_widget_enables_reaction_button_after_reset(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    widget.use_reaction_button.click()

    assert fighter.can_react() is False
    assert widget.use_reaction_button.isEnabled() is False

    fighter.reset_reaction()
    widget.refresh()

    assert fighter.can_react() is True
    assert widget.use_reaction_button.isEnabled() is True

def test_combatant_widget_refreshes_reaction_after_next_turn(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    fighter.use_reaction()

    combat = Combat()
    combat.add_combatant(fighter)
    combat.start()

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    assert fighter.can_react() is False
    assert widget.use_reaction_button.isEnabled() is False

    combat.next_turn()
    widget.refresh()

    assert fighter.can_react() is True
    assert widget.use_reaction_button.isEnabled() is True

def test_combatant_widget_displays_legendary_action_usage(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
        legendary_action_limit=3,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    assert widget.legendary_action_label.text() == "Legendary Actions: 0 / 3"

def test_combatant_widget_updates_legendary_action_usage(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
        legendary_action_limit=3,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    fighter.use_legendary_action()
    widget.refresh()

    assert (
        widget.legendary_action_label.text()
        == "Legendary Actions: 1 / 3"
    )

def test_combatant_widget_can_use_legendary_action(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
        legendary_action_limit=3,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    widget.use_legendary_action_button.click()

    assert fighter.legendary_actions_used == 1
    assert (
        widget.legendary_action_label.text()
        == "Legendary Actions: 1 / 3"
    )

def test_combatant_widget_disables_legendary_action_button_at_limit(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
        legendary_action_limit=3,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    widget.use_legendary_action_button.click()
    widget.use_legendary_action_button.click()
    widget.use_legendary_action_button.click()

    assert fighter.legendary_actions_used == 3
    assert widget.use_legendary_action_button.isEnabled() is False

def test_combatant_widget_has_remove_button(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    assert widget.remove_button.text() == "REMOVE"

def test_combatant_widget_emits_remove_request(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    received = []

    widget.remove_requested.connect(received.append)

    widget.remove_button.click()

    assert received == [fighter]

def test_combatant_widget_can_request_move(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    received = []

    widget.move_requested.connect(
        lambda combatant, index: received.append(
            (combatant, index)
        )
    )

    widget.request_move(2)

    assert received == [(fighter, 2)]

def test_combatant_widget_stores_drag_start_position(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    assert widget.drag_start_position is None

def test_combatant_widget_stores_mouse_press_position(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    widget.show()

    position = QPoint(20, 30)

    qtbot.mousePress(
        widget,
        Qt.MouseButton.LeftButton,
        pos=position,
    )

    assert widget.drag_start_position == position

def test_combatant_widget_does_not_start_drag_for_small_mouse_move(
        qtbot,
):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    widget.drag_start_position = QPoint(20, 30)

    position = QPoint(21, 31)  # Small move, should not trigger drag

    assert not widget.should_start_drag(position)

def test_combatant_widget_starts_drag_for_large_mouse_move(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    widget.drag_start_position = QPoint(20, 30)

    position = QPoint(50, 60)

    assert widget.should_start_drag(position)

def test_combatant_widget_requests_drag_for_large_mouse_move(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    widget.drag_start_position = QPoint(20, 30)

    called = []

    def fake_start_drag():
        called.append(True)

    widget.start_drag = fake_start_drag

    widget.mouseMoveEvent(
        QMouseEvent(
            QMouseEvent.Type.MouseMove,
            QPoint(50, 60),
            Qt.MouseButton.NoButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier
        )
    )

    assert called == [True]

def test_combatant_widget_can_create_drag(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    drag = widget.create_drag()

    assert drag.source() is widget

def test_combatant_widget_starts_drag(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    executed = []

    class FakeDrag:
        def exec(self):
            executed.append(True)

    widget.create_drag = lambda: FakeDrag()

    widget.start_drag()

    assert executed == [True]

def test_combatant_widget_drag_has_mime_data(qtbot):
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    widget = CombatantWidget(fighter)
    qtbot.addWidget(widget)

    drag = widget.create_drag()

    assert drag.mimeData() is not None