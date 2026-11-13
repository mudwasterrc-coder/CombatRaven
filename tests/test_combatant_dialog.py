from combat_raven.models.combatant import Combatant
from combat_raven.ui.combatant_dialog import CombatantDialog


def test_combatant_dialog_creates_a_combatant(qtbot):
    dialog = CombatantDialog()
    qtbot.addWidget(dialog)

    dialog.name_input.setText("Strahd")
    dialog.max_hp_input.setValue(350)
    dialog.current_hp_input.setValue(350)
    dialog.initiative_input.setValue(22)
    dialog.legendary_action_limit_input.setValue(3)

    combatant = dialog.create_combatant()

    assert combatant.name == "Strahd"
    assert combatant.max_hp == 350
    assert combatant.current_hp == 350
    assert combatant.initiative == 22
    assert combatant.legendary_action_limit == 3

def test_combatant_dialog_current_hp_follows_max_hp(qtbot):
    dialog = CombatantDialog()
    qtbot.addWidget(dialog)

    assert dialog.current_hp_input.value() == dialog.max_hp_input.value()

    dialog.max_hp_input.setValue(45)

    assert dialog.current_hp_input.value() == 45

def test_combatant_dialog_sets_concentration_limit(qtbot):
    dialog = CombatantDialog()
    qtbot.addWidget(dialog)

    assert dialog.concentration_limit_input.value() == 1

    dialog.name_input.setText("Wizard")
    dialog.max_hp_input.setValue(18)
    dialog.concentration_limit_input.setValue(2)

    wizard = dialog.create_combatant()

    assert wizard.concentration_limit == 2

def test_combatant_dialog_prefills_from_existing_combatant(qtbot):
    wizard = Combatant(
        name="Wizard",
        initiative=15,
        current_hp=10,
        max_hp=18,
        legendary_action_limit=0,
        concentration_limit=2
    )

    dialog = CombatantDialog(combatant=wizard)
    qtbot.addWidget(dialog)

    assert dialog.name_input.text() == "Wizard"
    assert dialog.max_hp_input.value() == 18
    assert dialog.current_hp_input.value() == 10
    assert dialog.initiative_input.value() == 15
    assert dialog.legendary_action_limit_input.value() == 0
    assert dialog.concentration_limit_input.value() == 2

def test_combatant_dialog_applies_changes_to_existing_combatant(qtbot):
    wizard = Combatant(
        name="Wizard",
        initiative=15,
        current_hp=10,
        max_hp=18,
    )
    original_id = wizard.id

    dialog = CombatantDialog(combatant=wizard)
    qtbot.addWidget(dialog)

    dialog.name_input.setText("Elminster")
    dialog.initiative_input.setValue(20)
    dialog.max_hp_input.setValue(30)
    dialog.current_hp_input.setValue(12)
    dialog.legendary_action_limit_input.setValue(1)
    dialog.concentration_limit_input.setValue(2)

    dialog.apply_changes()

    assert wizard.name == "Elminster"
    assert wizard.initiative == 20
    assert wizard.max_hp == 30
    assert wizard.current_hp == 12
    assert wizard.legendary_action_limit == 1
    assert wizard.concentration_limit == 2
    assert wizard.id == original_id  # Ensure the ID remains unchanged