from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from combat_raven.models.combat import Combat
from combat_raven.repositories.combat_repository import CombatRepository
from combat_raven.ui.open_combat_dialog import OpenCombatDialog


def test_open_combat_dialog_lists_saved_combats(qtbot, tmp_path):
    repository = CombatRepository(tmp_path)

    first = Combat(name="Assault on the Tower")
    second = Combat(name="Crypt of Ravenloft")

    repository.save(first)
    repository.save(second)

    dialog = OpenCombatDialog(repository)
    qtbot.addWidget(dialog)

    assert dialog.combat_list.count() == 2
    assert dialog.combat_list.item(0).text() == "Assault on the Tower"
    assert dialog.combat_list.item(1).text() == "Crypt of Ravenloft"

def test_open_combat_dialog_items_keep_combat_ids(qtbot, tmp_path):
    repository = CombatRepository(tmp_path)

    first = Combat(name="Assault on the Tower")
    second = Combat(name="Crypt of Ravenloft")

    repository.save(first)
    repository.save(second)

    dialog = OpenCombatDialog(repository)
    qtbot.addWidget(dialog)

    first_item = dialog.combat_list.item(0)
    second_item = dialog.combat_list.item(1)

    assert first_item.data(Qt.ItemDataRole.UserRole) == first.id
    assert second_item.data(Qt.ItemDataRole.UserRole) == second.id

def test_open_combat_dialog_returns_selected_combat_id(
    qtbot,
    tmp_path,
):
    repository = CombatRepository(tmp_path)

    combat = Combat(name="Assault on the Tower")
    repository.save(combat)

    dialog = OpenCombatDialog(repository)
    qtbot.addWidget(dialog)

    dialog.combat_list.setCurrentRow(0)

    assert dialog.selected_combat_id == combat.id

def test_open_combat_dialog_has_cancel_button(qtbot, tmp_path):
    repository = CombatRepository(tmp_path)

    dialog = OpenCombatDialog(repository)
    qtbot.addWidget(dialog)

    assert dialog.cancel_button is not None
    assert dialog.cancel_button.text() == "CANCEL"

def test_open_combat_dialog_cancel_rejects_dialog(qtbot, tmp_path):
    repository = CombatRepository(tmp_path)

    dialog = OpenCombatDialog(repository)
    qtbot.addWidget(dialog)

    dialog.show()

    qtbot.mouseClick(
        dialog.cancel_button,
        Qt.MouseButton.LeftButton,
    )

    assert dialog.result() == QDialog.DialogCode.Rejected

def test_open_combat_dialog_has_open_button(qtbot, tmp_path):
    repository = CombatRepository(tmp_path)

    dialog = OpenCombatDialog(repository)
    qtbot.addWidget(dialog)

    assert dialog.open_button is not None
    assert dialog.open_button.text() == "OPEN"

def test_open_combat_dialog_open_accepts_selected_combat(
    qtbot,
    tmp_path,
):
    repository = CombatRepository(tmp_path)

    combat = Combat(name="Assault on the Tower")
    repository.save(combat)

    dialog = OpenCombatDialog(repository)
    qtbot.addWidget(dialog)

    dialog.show()

    dialog.combat_list.setCurrentRow(0)

    qtbot.mouseClick(
        dialog.open_button,
        Qt.MouseButton.LeftButton,
    )

    assert dialog.result() == QDialog.DialogCode.Accepted

def test_open_combat_dialog_open_does_not_accept_without_selection(
    qtbot,
    tmp_path,
):
    repository = CombatRepository(tmp_path)

    combat = Combat(name="Assault on the Tower")
    repository.save(combat)

    dialog = OpenCombatDialog(repository)
    qtbot.addWidget(dialog)

    dialog.show()

    dialog.combat_list.clearSelection()

    qtbot.mouseClick(
        dialog.open_button,
        Qt.MouseButton.LeftButton,
    )

    assert dialog.result() == 0