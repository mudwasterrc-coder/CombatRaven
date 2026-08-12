from combat_raven.models.combatant import Combatant
from combat_raven.ui.combatant_widget import CombatantWidget
from combat_raven.models.combat import Combat


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