from combat_raven.ui.rename_combat_dialog import RenameCombatDialog


def test_rename_combat_dialog_cancel_rejects(qtbot):
    dialog = RenameCombatDialog("Cripta de Strahd")
    qtbot.addWidget(dialog)

    rejected = []
    dialog.rejected.connect(lambda: rejected.append(True))

    dialog.cancel_button.click()

    assert rejected == [True]