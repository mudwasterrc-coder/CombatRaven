from PySide6.QtCore import Qt


from combat_raven.ui.concentration_dialog import ConcentrationDialog
from combat_raven.models.combatant import Combatant


def test_concentration_dialog_builds_template_from_inputs(qtbot):
    dialog = ConcentrationDialog()
    qtbot.addWidget(dialog)

    dialog.name_input.setText("Bless")
    dialog.duration_input.setValue(10)

    template = dialog.create_template()

    assert template.name == "Bless"
    assert template.default_duration == 10
    assert template.concentration is True

def test_concentration_dialog_zero_rounds_means_no_limit(qtbot):
    dialog = ConcentrationDialog()
    qtbot.addWidget(dialog)

    dialog.name_input.setText("Hex")
    dialog.duration_input.setValue(0)

    assert dialog.duration_input.specialValueText() == "∞"
    assert dialog.create_template().default_duration is None

def test_concentration_dialog_lists_candidates_unchecked(qtbot):
    fighter = Combatant(name="Fighter", initiative=20, current_hp=30, max_hp=30)
    rogue = Combatant(name="Rogue", initiative=15, current_hp=22, max_hp=22)

    dialog = ConcentrationDialog([fighter, rogue])
    qtbot.addWidget(dialog)

    assert dialog.target_list.count() == 2
    assert dialog.target_list.item(0).text() == "Fighter"
    assert dialog.target_list.item(1).text() == "Rogue"
    assert dialog.target_list.item(0).checkState() == Qt.CheckState.Unchecked

def test_concentration_dialog_returns_checked_targets(qtbot):
    fighter = Combatant(name="Fighter", initiative=20, current_hp=30, max_hp=30)
    rogue = Combatant(name="Rogue", initiative=15, current_hp=22, max_hp=22)
    wizard = Combatant(name="Wizard", initiative=14, current_hp=18, max_hp=18)

    dialog = ConcentrationDialog([fighter, rogue, wizard])
    qtbot.addWidget(dialog)

    dialog.target_list.item(0).setCheckState(Qt.CheckState.Checked)
    dialog.target_list.item(2).setCheckState(Qt.CheckState.Checked)

    assert dialog.selected_targets() == [fighter, wizard]

def test_concentration_dialog_cancel_rejects(qtbot):
    dialog = ConcentrationDialog()
    qtbot.addWidget(dialog)

    rejected = []
    dialog.rejected.connect(lambda: rejected.append(True))

    dialog.cancel_button.click()

    assert rejected == [True]


def test_concentration_dialog_apply_accepts_with_name_and_target(qtbot):
    fighter = Combatant(name="Fighter", initiative=20, current_hp=30, max_hp=30)
    dialog = ConcentrationDialog([fighter])
    qtbot.addWidget(dialog)

    accepted = []
    dialog.accepted.connect(lambda: accepted.append(True))

    dialog.name_input.setText("Bless")
    dialog.target_list.item(0).setCheckState(Qt.CheckState.Checked)
    dialog.apply_button.click()

    assert accepted == [True]

def test_concentration_dialog_apply_requires_a_name(qtbot):
    fighter = Combatant(name="Fighter", initiative=20, current_hp=30, max_hp=30)
    dialog = ConcentrationDialog([fighter])
    qtbot.addWidget(dialog)

    accepted = []
    dialog.accepted.connect(lambda: accepted.append(True))

    dialog.name_input.setText("   ")
    dialog.target_list.item(0).setCheckState(Qt.CheckState.Checked)
    dialog.apply_button.click()

    assert accepted == []


def test_concentration_dialog_apply_requires_a_target(qtbot):
    fighter = Combatant(name="Fighter", initiative=20, current_hp=30, max_hp=30)
    dialog = ConcentrationDialog([fighter])
    qtbot.addWidget(dialog)

    accepted = []
    dialog.accepted.connect(lambda: accepted.append(True))

    dialog.name_input.setText("Bless")
    dialog.apply_button.click()

    assert accepted == []