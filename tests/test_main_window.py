from combat_raven.models.combat import Combat
from combat_raven.ui.main_window import MainWindow
from combat_raven.models.combatant import Combatant


def test_main_window_can_start_with_no_combatants(qtbot):
    combat = Combat()
    window = MainWindow(combat)
    qtbot.addWidget(window)

    assert len(combat.combatants) == 0

def test_main_window_can_add_a_combatant(qtbot):
    combat = Combat()
    window = MainWindow(combat)
    qtbot.addWidget(window)

    window.add_combatant(
        name="Strahd",
        max_hp=350,
        current_hp=350,
        initiative=22,
        legendary_action_limit=3,
    )

    assert len(combat.combatants) == 1
    assert combat.combatants[0].name == "Strahd"
    assert combat.combatants[0].max_hp == 350
    assert combat.combatants[0].current_hp == 350
    assert combat.combatants[0].initiative == 22
    assert combat.combatants[0].legendary_action_limit == 3

def test_main_window_has_add_combatant_button(qtbot):
    combat = Combat()
    window = MainWindow(combat)
    qtbot.addWidget(window)

    assert window.add_combatant_button.text() == "ADD COMBATANT"

def test_main_window_opens_combatant_dialog(qtbot, monkeypatch):
    combat = Combat()
    window = MainWindow(combat)
    qtbot.addWidget(window)

    opened = False

    class FakeDialog:
        def __init__(self):
            nonlocal opened
            opened = True

        def exec(self):
            return 0

    monkeypatch.setattr(
        "combat_raven.ui.main_window.CombatantDialog",
        FakeDialog,
    )

    window.add_combatant_button.click()

    assert opened is True

def test_main_window_adds_combatant_created_by_dialog(
    qtbot,
    monkeypatch,
):
    combat = Combat()
    window = MainWindow(combat)
    qtbot.addWidget(window)

    class FakeDialog:
        def exec(self):
            return 1

        def create_combatant(self):
            return Combatant(
                name="Strahd",
                max_hp=350,
                current_hp=350,
                initiative=22,
                legendary_action_limit=3,
            )

    monkeypatch.setattr(
        "combat_raven.ui.main_window.CombatantDialog",
        FakeDialog,
    )

    window.open_combatant_dialog()

    assert len(combat.combatants) == 1

    strahd = combat.combatants[0]

    assert strahd.name == "Strahd"
    assert strahd.max_hp == 350
    assert strahd.current_hp == 350
    assert strahd.initiative == 22
    assert strahd.legendary_action_limit == 3

def test_main_window_does_not_add_combatant_when_dialog_is_cancelled(
    qtbot,
    monkeypatch,
):
    combat = Combat()
    window = MainWindow(combat)
    qtbot.addWidget(window)

    class FakeDialog:
        def exec(self):
            return 0

        def create_combatant(self):
            raise AssertionError(
                "create_combatant should not be called"
            )

    monkeypatch.setattr(
        "combat_raven.ui.main_window.CombatantDialog",
        FakeDialog,
    )

    window.open_combatant_dialog()

    assert combat.combatants == []