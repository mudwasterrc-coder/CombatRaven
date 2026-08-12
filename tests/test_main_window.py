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

def test_main_window_can_remove_a_combatant(qtbot):
    combat = Combat()

    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    combat.add_combatant(fighter)

    window = MainWindow(combat)
    qtbot.addWidget(window)

    widget = window.combatants_layout.itemAt(0).widget()

    widget.remove_button.click()

    assert combat.combatants == []

def test_main_window_has_scrollable_combatants_list(qtbot):
    combat = Combat()
    window = MainWindow(combat)
    qtbot.addWidget(window)

    assert window.combatants_scroll_area is not None

def test_main_window_displays_many_combatants(qtbot):
    combat = Combat()

    for index in range(15):
        combat.add_combatant(
            Combatant(
                name=f"Combatant {index}",
                max_hp=100,
                current_hp=100,
                initiative=20 - index,
            )
        )

    window = MainWindow(combat)
    qtbot.addWidget(window)

    assert window.combatants_layout.count() == 15

def test_main_window_scroll_area_resizes_content(qtbot):
    combat = Combat()
    window = MainWindow(combat)
    qtbot.addWidget(window)

    assert window.combatants_scroll_area.widget() is (
        window.combatants_container
    )

    assert window.combatants_scroll_area.widgetResizable() is True

def  test_main_window_moves_combatant_when_move_is_requested(qtbot):
    combat = Combat()

    fighter = Combatant(
        name="Fighter",
        initiative=20,
        max_hp=30,
        current_hp=30,
    )

    wizard = Combatant(
        name="Wizard",
        initiative=15,
        max_hp=20,
        current_hp=20,
    )

    combat.add_combatant(fighter)
    combat.add_combatant(wizard)

    window = MainWindow(combat)
    qtbot.addWidget(window)

    widget = window.combatants_layout.itemAt(0).widget()

    widget.request_move(1)

    assert combat.combatants == [
        wizard,
        fighter,
    ]