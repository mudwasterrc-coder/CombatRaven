from PySide6.QtCore import Qt
from combat_raven.ui.new_combat_dialog import NewCombatDialog


def test_new_combat_dialog_has_name_input(qtbot):
    dialog = NewCombatDialog()
    qtbot.addWidget(dialog)

    assert dialog.name_input is not None

def test_new_combat_dialog_has_create_button(qtbot):
    dialog = NewCombatDialog()
    qtbot.addWidget(dialog)

    assert dialog.create_button is not None
    assert dialog.create_button.text() == "CREATE"

def test_new_combat_dialog_returns_entered_name(qtbot):
    dialog = NewCombatDialog()
    qtbot.addWidget(dialog)

    dialog.name_input.setText("Assault on the Tower")

    qtbot.mouseClick(
        dialog.create_button,
        Qt.MouseButton.LeftButton,
    )

    assert dialog.selected_name == "Assault on the Tower"

def test_new_combat_dialog_does_not_accept_empty_name(qtbot):
    dialog = NewCombatDialog()
    qtbot.addWidget(dialog)

    dialog.name_input.clear()

    qtbot.mouseClick(
        dialog.create_button,
        Qt.MouseButton.LeftButton,
    )

    assert dialog.result() == 0

def test_new_combat_dialog_has_cancel_button(qtbot):
    dialog = NewCombatDialog()
    qtbot.addWidget(dialog)

    assert dialog.cancel_button is not None
    assert dialog.cancel_button.text() == "CANCEL"

def test_new_combat_dialog_cancel_rejects(qtbot):
    dialog = NewCombatDialog()
    qtbot.addWidget(dialog)

    qtbot.mouseClick(
        dialog.cancel_button,
        Qt.MouseButton.LeftButton,
    )

    assert dialog.result() == 0