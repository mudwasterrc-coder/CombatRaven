from PySide6.QtCore import Qt

from combat_raven.models.combat import Combat
from combat_raven.ui.main_window import MainWindow
from combat_raven.models.combatant import Combatant
from combat_raven.ui.combatants_container import CombatantsContainer
from combat_raven.repositories.combat_repository import CombatRepository
from combat_raven.models.effect import Effect
from combat_raven.models.effect_template import EffectTemplate


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

def test_main_window_has_sort_by_initiative_button(qtbot):
    combat = Combat()
    window = MainWindow(combat)
    qtbot.addWidget(window)

    assert (
        window.sort_by_initiative_button.text() == "SORT BY INITIATIVE"
    )

def test_main_window_sorts_combatants_by_initiative(qtbot):
    combat = Combat()

    goblin = Combatant(
        name="Goblin",
        max_hp=7,
        current_hp=7,
        initiative=10,
    )

    fighter = Combatant(
        name="Fighter",
        max_hp=30,
        current_hp=30,
        initiative=20,
    )

    wizard = Combatant(
        name="Wizard",
        max_hp=20,
        current_hp=20,
        initiative=15,
    )

    combat.add_combatant(goblin)
    combat.add_combatant(fighter)
    combat.add_combatant(wizard)

    window = MainWindow(combat)
    qtbot.addWidget(window)

    window.sort_by_initiative_button.click()

    assert combat.combatants == [
        fighter,
        wizard,
        goblin,
    ]

def test_main_window_uses_combatants_container(qtbot):
    combat = Combat()

    window = MainWindow(combat)
    qtbot.addWidget(window)

    assert isinstance(
        window.combatants_container,
        CombatantsContainer,
    )

def test_main_window_moves_combatant_when_drop_is_requested(qtbot):
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

    window.combatants_container.drop_requested.emit(
        wizard,
        0,
    )

    assert combat.combatants == [
        wizard,
        fighter,
    ]

def test_main_window_reorders_widgets_when_combatant_is_moved(qtbot):
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

    window.combatants_container.drop_requested.emit(
        wizard,
        0,
    )

    first_widget = (
        window.combatants_container.layout()
        .itemAt(0)
        .widget()
    )

    second_widget = (
        window.combatants_container.layout()
        .itemAt(1)
        .widget()
    )

    assert first_widget.combatant is wizard
    assert second_widget.combatant is fighter

def test_main_window_has_combat_repository(qtbot, tmp_path):
    combat = Combat()
    repository = CombatRepository(tmp_path)

    window = MainWindow(combat, repository)
    qtbot.addWidget(window)

    assert window.combat_repository is repository

def test_main_window_can_save_current_combat(
    qtbot,
    tmp_path,
):
    combat = Combat(
        name="Assault on the Tower",
    )

    repository = CombatRepository(tmp_path)

    window = MainWindow(
        combat,
        repository,
    )
    qtbot.addWidget(window)

    window.save_combat()

    loaded = repository.get_by_id(combat.id)

    assert loaded is not None
    assert loaded.id == combat.id
    assert loaded.name == "Assault on the Tower"

def test_main_window_can_update_saved_combat(qtbot, tmp_path):
    combat = Combat(
        name="Assault on the Tower",
    )

    repository = CombatRepository(tmp_path)

    window = MainWindow(
        combat,
        repository,
    )
    qtbot.addWidget(window)

    window.save_combat()

    combat.name = "Assault on the Tower - Final Battle"

    window.save_combat()

    loaded = repository.get_by_id(combat.id)

    assert loaded is not None
    assert loaded.name == "Assault on the Tower - Final Battle"

def test_main_window_has_save_combat_button(qtbot, tmp_path):
    combat = Combat()
    repository = CombatRepository(tmp_path)

    window = MainWindow(combat, repository)
    qtbot.addWidget(window)

    assert window.save_combat_button is not None
    assert window.save_combat_button.text() == "SAVE COMBAT"

def test_main_window_save_combat_button_saves_combat(
    qtbot,
    tmp_path,
):
    combat = Combat(name="Assault on the Tower")
    repository = CombatRepository(tmp_path)

    window = MainWindow(combat, repository)
    qtbot.addWidget(window)

    qtbot.mouseClick(
        window.save_combat_button,
        Qt.MouseButton.LeftButton,
    )

    loaded = repository.get_by_id(combat.id)

    assert loaded is not None
    assert loaded.name == "Assault on the Tower"

def test_main_window_has_open_combat_button(qtbot, tmp_path):
    combat = Combat()
    repository = CombatRepository(tmp_path)

    window = MainWindow(combat, repository)
    qtbot.addWidget(window)

    assert window.open_combat_button is not None
    assert window.open_combat_button.text() == "OPEN ENCOUNTER"

def test_main_window_can_open_combat_dialog(qtbot, tmp_path):
    combat = Combat()
    repository = CombatRepository(tmp_path)

    window = MainWindow(combat, repository)
    qtbot.addWidget(window)

    window.open_combat()

    assert window.open_combat_dialog is not None

def test_main_window_can_load_selected_combat(
    qtbot,
    tmp_path,
):
    repository = CombatRepository(tmp_path)

    saved_combat = Combat(
        name="Assault on the Tower",
    )
    repository.save(saved_combat)

    current_combat = Combat(
        name="Current Encounter",
    )

    window = MainWindow(
        current_combat,
        repository,
    )
    qtbot.addWidget(window)

    window.open_combat()

    window.open_combat_dialog.combat_list.setCurrentRow(0)
    window.open_combat_dialog.open_button.click()

    assert window.combat.id == saved_combat.id
    assert window.combat.name == "Assault on the Tower"

def test_main_window_refreshes_after_loading_combat(
    qtbot,
    tmp_path,
):
    repository = CombatRepository(tmp_path)

    saved_combat = Combat(name="Saved Encounter")

    fighter = Combatant(
        name="Fighter",
        initiative=20,
        max_hp=30,
        current_hp=17,
    )

    saved_combat.add_combatant(fighter)
    repository.save(saved_combat)

    current_combat = Combat(name="Current Encounter")

    window = MainWindow(
        current_combat,
        repository,
    )
    qtbot.addWidget(window)

    window.open_combat()

    window.open_combat_dialog.combat_list.setCurrentRow(0)
    window.open_combat_dialog.open_button.click()

    assert window.round_label.text() == "ROUND 0"
    assert window.current_turn_label.text() == "CURRENT TURN: Fighter"
    assert (
        window.combatants_layout.itemAt(0).widget().combatant
        is window.combat.combatants[0]
    )

def test_main_window_restores_saved_combat_state(
        qtbot,
        tmp_path,
):
    repository = CombatRepository(tmp_path)

    saved_combat = Combat(name="Boss Fight")

    fighter = Combatant(
        name="Fighter",
        initiative=20,
        max_hp=30,
        current_hp=17,
    )

    wizard = Combatant(
        name="Wizard",
        initiative=15,
        max_hp=20,
        current_hp=8,
    )

    saved_combat.add_combatant(fighter)
    saved_combat.add_combatant(wizard)

    saved_combat.start()
    saved_combat.next_turn()

    repository.save(saved_combat)

    current_combat = Combat(name="Empty Encounter")

    window = MainWindow(
        current_combat,
        repository,
    )
    qtbot.addWidget(window)

    window.open_combat()

    window.open_combat_dialog.combat_list.setCurrentRow(0)
    window.open_combat_dialog.open_button.click()

    assert window.combat.id == saved_combat.id
    assert window.combat.name == "Boss Fight"
    assert window.combat.current_round == 1
    assert window.combat.current_turn_index == 1
    assert window.combat.current_combatant.name == "Wizard"
    assert window.combat.combatants[0].current_hp == 17
    assert window.combat.combatants[1].current_hp == 8

def test_main_window_restores_saved_combat_effects(
    qtbot,
    tmp_path,
):
    repository = CombatRepository(tmp_path)

    saved_combat = Combat(name="Blessed Battle")

    fighter = Combatant(
        name="Fighter",
        initiative=20,
        max_hp=30,
        current_hp=17,
    )

    bless = EffectTemplate(
        name="Bless",
        default_duration=10,
        concentration=True,
        notes="+1d4 to attack rolls and saving throws",
    )

    effect = Effect.from_template(bless)
    effect.tick()
    effect.tick()

    fighter.effects.append(effect)
    saved_combat.add_combatant(fighter)

    repository.save(saved_combat)

    current_combat = Combat(name="Empty Encounter")

    window = MainWindow(
        current_combat,
        repository,
    )
    qtbot.addWidget(window)

    window.open_combat()

    window.open_combat_dialog.combat_list.setCurrentRow(0)
    window.open_combat_dialog.open_button.click()

    loaded_effect = window.combat.combatants[0].effects[0]

    assert loaded_effect.template.name == "Bless"
    assert loaded_effect.remaining_rounds == 8
    assert loaded_effect.concentration is True
    assert loaded_effect.enabled is True
    assert loaded_effect.notes == "+1d4 to attack rolls and saving throws"

def test_main_window_can_create_new_combat(qtbot, tmp_path):
    current_combat = Combat(
        name="Current Encounter",
    )

    repository = CombatRepository(tmp_path)

    window = MainWindow(
        current_combat,
        repository,
    )
    qtbot.addWidget(window)

    window.new_combat()

    window.new_combat_dialog.name_input.setText(
        "New Encounter"
    )

    window.new_combat_dialog.create_button.click()

    assert window.combat is not current_combat
    assert window.combat.name == "New Encounter"
    assert window.combat.combatants == []

def test_main_window_can_create_named_combat(
    qtbot,
    tmp_path,
):
    repository = CombatRepository(tmp_path)

    current_combat = Combat(
        name="Current Encounter",
    )

    window = MainWindow(
        current_combat,
        repository,
    )
    qtbot.addWidget(window)

    window.new_combat()

    window.new_combat_dialog.name_input.setText(
        "Assault on the Tower"
    )

    window.new_combat_dialog.create_button.click()

    assert window.combat.name == "Assault on the Tower"
    assert window.combat.combatants == []

def test_main_window_cancel_new_combat_keeps_current_combat(
    qtbot,
    tmp_path,
):
    repository = CombatRepository(tmp_path)

    current_combat = Combat(
        name="Current Encounter",
    )

    window = MainWindow(
        current_combat,
        repository,
    )
    qtbot.addWidget(window)

    window.new_combat()

    window.new_combat_dialog.name_input.setText(
        "Assault on the Tower"
    )

    window.new_combat_dialog.cancel_button.click()

    assert window.combat is current_combat
    assert window.combat.name == "Current Encounter"

def test_main_window_has_new_combat_button(qtbot, tmp_path):
    combat = Combat()
    repository = CombatRepository(tmp_path)

    window = MainWindow(combat, repository)
    qtbot.addWidget(window)

    assert window.new_combat_button is not None
    assert window.new_combat_button.text() == "NEW ENCOUNTER"

def test_main_window_new_combat_button_opens_dialog(
    qtbot,
    tmp_path,
):
    combat = Combat()
    repository = CombatRepository(tmp_path)

    window = MainWindow(combat, repository)
    qtbot.addWidget(window)

    qtbot.mouseClick(
        window.new_combat_button,
        Qt.MouseButton.LeftButton,
    )

    assert window.new_combat_dialog is not None
    assert window.new_combat_dialog.isVisible()

def test_main_window_can_create_named_combat_from_button(
    qtbot,
    tmp_path,
):
    repository = CombatRepository(tmp_path)

    current_combat = Combat(
        name="Current Encounter",
    )

    window = MainWindow(
        current_combat,
        repository,
    )
    qtbot.addWidget(window)

    qtbot.mouseClick(
        window.new_combat_button,
        Qt.MouseButton.LeftButton,
    )

    window.new_combat_dialog.name_input.setText(
        "Assault on the Tower"
    )

    qtbot.mouseClick(
        window.new_combat_dialog.create_button,
        Qt.MouseButton.LeftButton,
    )

    assert window.combat is not current_combat
    assert window.combat.name == "Assault on the Tower"
    assert window.combat.combatants == []

def test_main_window_has_status_label(qtbot, tmp_path):
    combat = Combat(name="Assault on the Tower")
    repository = CombatRepository(tmp_path)

    window = MainWindow(combat, repository)
    qtbot.addWidget(window)

    assert window.status_label is not None

def test_main_window_save_combat_shows_status(
    qtbot,
    tmp_path,
):
    combat = Combat(name="Assault on the Tower")
    repository = CombatRepository(tmp_path)

    window = MainWindow(combat, repository)
    qtbot.addWidget(window)

    window.save_combat()

    assert window.status_label.text() == (
        "COMBAT SAVED: Assault on the Tower"
    )

def test_main_window_open_combat_shows_status(
    qtbot,
    tmp_path,
):
    repository = CombatRepository(tmp_path)

    saved_combat = Combat(name="Assault on the Tower")
    repository.save(saved_combat)

    current_combat = Combat(name="Current Encounter")

    window = MainWindow(current_combat, repository)
    qtbot.addWidget(window)

    window.open_combat()

    window.open_combat_dialog.combat_list.setCurrentRow(0)
    window.open_combat_dialog.open_button.click()

    assert window.status_label.text() == (
        "COMBAT LOADED: Assault on the Tower"
    )

def test_main_window_save_button_saves_combat(
    qtbot,
    tmp_path,
):
    combat = Combat(name="Assault on the Tower")
    repository = CombatRepository(tmp_path)

    window = MainWindow(combat, repository)
    qtbot.addWidget(window)

    qtbot.mouseClick(
        window.save_combat_button,
        Qt.MouseButton.LeftButton,
    )

    loaded = repository.get_by_id(combat.id)

    assert loaded is not None
    assert loaded.name == "Assault on the Tower"
    assert window.status_label.text() == (
        "COMBAT SAVED: Assault on the Tower"
    )

def test_main_window_open_button_opens_dialog(
    qtbot,
    tmp_path,
):
    repository = CombatRepository(tmp_path)

    combat = Combat(name="Assault on the Tower")
    repository.save(combat)

    current_combat = Combat(name="Current Encounter")

    window = MainWindow(current_combat, repository)
    qtbot.addWidget(window)

    qtbot.mouseClick(
        window.open_combat_button,
        Qt.MouseButton.LeftButton,
    )

    assert window.open_combat_dialog is not None
    assert window.open_combat_dialog.isVisible()

def test_main_window_open_button_loads_selected_combat(
    qtbot,
    tmp_path,
):
    repository = CombatRepository(tmp_path)

    saved_combat = Combat(
        name="Assault on the Tower",
    )
    repository.save(saved_combat)

    current_combat = Combat(
        name="Current Encounter",
    )

    window = MainWindow(
        current_combat,
        repository,
    )
    qtbot.addWidget(window)

    qtbot.mouseClick(
        window.open_combat_button,
        Qt.MouseButton.LeftButton,
    )

    window.open_combat_dialog.combat_list.setCurrentRow(0)

    qtbot.mouseClick(
        window.open_combat_dialog.open_button,
        Qt.MouseButton.LeftButton,
    )

    assert window.combat.id == saved_combat.id
    assert window.combat.name == "Assault on the Tower"
    assert window.status_label.text() == (
        "COMBAT LOADED: Assault on the Tower"
    )

def test_main_window_open_button_opens_dialog_after_delete(
    qtbot,
    tmp_path,
):
    repository = CombatRepository(tmp_path)

    combat = Combat(name="Assault on the Tower")
    repository.save(combat)

    window = MainWindow(
        Combat(name="Current Encounter"),
        repository,
    )
    qtbot.addWidget(window)

    qtbot.mouseClick(
        window.open_combat_button,
        Qt.MouseButton.LeftButton,
    )

    assert hasattr(window, "open_combat_dialog")
    assert window.open_combat_dialog.isVisible()

