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