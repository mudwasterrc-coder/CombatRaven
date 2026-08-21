from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QMessageBox

from combat_raven.models.combat import Combat
from combat_raven.repositories.combat_repository import CombatRepository
from combat_raven.ui.open_combat_dialog import OpenCombatDialog
from combat_raven.ui.rename_combat_dialog import RenameCombatDialog


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

def test_open_combat_dialog_has_delete_button(qtbot, tmp_path):
    repository = CombatRepository(tmp_path)

    dialog = OpenCombatDialog(repository)
    qtbot.addWidget(dialog)

    assert dialog.delete_button is not None
    assert dialog.delete_button.text() == "DELETE"

def test_open_combat_dialog_delete_removes_selected_combat(
    qtbot,
    tmp_path,
    monkeypatch,
):
    repository = CombatRepository(tmp_path)

    first = Combat(name="Assault on the Tower")
    second = Combat(name="Crypt of Ravenloft")

    repository.save(first)
    repository.save(second)

    dialog = OpenCombatDialog(repository)
    qtbot.addWidget(dialog)

    dialog.combat_list.setCurrentRow(0)

    monkeypatch.setattr(
        "combat_raven.ui.open_combat_dialog.QMessageBox.question",
        lambda *args, **kwargs: QMessageBox.StandardButton.Yes,
)
    qtbot.mouseClick(
        dialog.delete_button,
        Qt.MouseButton.LeftButton,
    )

    assert repository.get_by_id(first.id) is None
    assert repository.get_by_id(second.id) is not None

def test_open_combat_dialog_delete_does_nothing_without_selection(qtbot, tmp_path,):
    repository = CombatRepository(tmp_path)

    combat = Combat(name="Assault on the Tower")
    repository.save(combat)

    dialog = OpenCombatDialog(repository)
    qtbot.addWidget(dialog)

    dialog.combat_list.clearSelection()

    qtbot.mouseClick(
        dialog.delete_button,
        Qt.MouseButton.LeftButton,
    )

    assert repository.get_by_id(combat.id) is not None

def test_open_combat_dialog_delete_can_be_cancelled(
    qtbot,
    tmp_path,
    monkeypatch,
):
    repository = CombatRepository(tmp_path)

    combat = Combat(name="Assault on the Tower")
    repository.save(combat)

    dialog = OpenCombatDialog(repository)
    qtbot.addWidget(dialog)

    dialog.combat_list.setCurrentRow(0)

    monkeypatch.setattr(
        "combat_raven.ui.open_combat_dialog.QMessageBox.question",
        lambda *args, **kwargs: QMessageBox.StandardButton.No,
    )

    qtbot.mouseClick(
        dialog.delete_button,
        Qt.MouseButton.LeftButton,
    )

    assert repository.get_by_id(combat.id) is not None

def test_open_combat_dialog_has_rename_button(qtbot, tmp_path):
    repository = CombatRepository(tmp_path)

    dialog = OpenCombatDialog(repository)
    qtbot.addWidget(dialog)

    assert dialog.rename_button is not None
    assert dialog.rename_button.text() == "RENAME"

def test_open_combat_dialog_rename_opens_dialog(
    qtbot,
    tmp_path,
):
    repository = CombatRepository(tmp_path)

    combat = Combat(name="Assault on the Tower")
    repository.save(combat)

    dialog = OpenCombatDialog(repository)
    qtbot.addWidget(dialog)

    dialog.combat_list.setCurrentRow(0)

    qtbot.mouseClick(
        dialog.rename_button,
        Qt.MouseButton.LeftButton,
    )

    assert dialog.rename_combat_dialog is not None

def test_rename_combat_dialog_has_name_input(qtbot):
    dialog = RenameCombatDialog("Assault on the Tower")
    qtbot.addWidget(dialog)

    assert dialog.name_input is not None

def test_rename_combat_dialog_prefills_current_name(qtbot):
    dialog = RenameCombatDialog("Assault on the Tower")
    qtbot.addWidget(dialog)

    assert dialog.name_input.text() == "Assault on the Tower"

def test_rename_combat_dialog_has_rename_button(qtbot):
    dialog = RenameCombatDialog("Assault on the Tower")
    qtbot.addWidget(dialog)

    assert dialog.rename_button is not None
    assert dialog.rename_button.text() == "RENAME"

def test_rename_combat_dialog_has_cancel_button(qtbot):
    dialog = RenameCombatDialog("Assault on the Tower")
    qtbot.addWidget(dialog)

    assert dialog.cancel_button is not None
    assert dialog.cancel_button.text() == "CANCEL"

def test_rename_combat_dialog_has_title(qtbot):
    dialog = RenameCombatDialog("Assault on the Tower")
    qtbot.addWidget(dialog)

    assert dialog.windowTitle() == "RENAME ENCOUNTER"

def test_rename_combat_dialog_has_main_layout(qtbot):
    dialog = RenameCombatDialog("Assault on the Tower")
    qtbot.addWidget(dialog)

    assert dialog.layout() is not None

def test_rename_combat_dialog_has_button_layout(qtbot):
    dialog = RenameCombatDialog("Assault on the Tower")
    qtbot.addWidget(dialog)

    assert dialog.button_layout is not None

def test_rename_combat_dialog_cancel_rejects(
    qtbot,
):
    dialog = RenameCombatDialog("Assault on the Tower")
    qtbot.addWidget(dialog)

    dialog.cancel_button.click()

    assert dialog.result() == 0

def test_rename_combat_dialog_returns_entered_name(
    qtbot,
):
    dialog = RenameCombatDialog("Assault on the Tower")
    qtbot.addWidget(dialog)

    dialog.name_input.setText("Assault on Castle Ravenloft")

    dialog.rename_button.click()

    assert dialog.selected_name == "Assault on Castle Ravenloft"

def test_open_combat_dialog_renames_selected_combat(
    qtbot,
    tmp_path,
):
    repository = CombatRepository(tmp_path)

    combat = Combat(name="Assault on the Tower")
    repository.save(combat)

    dialog = OpenCombatDialog(repository)
    qtbot.addWidget(dialog)

    dialog.combat_list.setCurrentRow(0)

    qtbot.mouseClick(
        dialog.rename_button,
        Qt.MouseButton.LeftButton,
    )

    dialog.rename_combat_dialog.name_input.setText(
        "Assault on Castle Ravenloft"
    )

    qtbot.mouseClick(
        dialog.rename_combat_dialog.rename_button,
        Qt.MouseButton.LeftButton,
    )

    renamed = repository.get_by_id(combat.id)

    assert renamed is not None
    assert renamed.name == "Assault on Castle Ravenloft"

def test_open_combat_dialog_rename_updates_list(
    qtbot,
    tmp_path,
):
    repository = CombatRepository(tmp_path)

    combat = Combat(name="Assault on the Tower")
    repository.save(combat)

    dialog = OpenCombatDialog(repository)
    qtbot.addWidget(dialog)

    dialog.combat_list.setCurrentRow(0)

    qtbot.mouseClick(
        dialog.rename_button,
        Qt.MouseButton.LeftButton,
    )

    dialog.rename_combat_dialog.name_input.setText(
        "Assault on Castle Ravenloft"
    )

    qtbot.mouseClick(
        dialog.rename_combat_dialog.rename_button,
        Qt.MouseButton.LeftButton,
    )

    assert dialog.combat_list.count() == 1
    assert (
        dialog.combat_list.item(0).text()
        == "Assault on Castle Ravenloft"
    )