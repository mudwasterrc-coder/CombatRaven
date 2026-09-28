from PySide6.QtWidgets import QApplication

from combat_raven.repositories.participant_repository import ParticipantRepository
from combat_raven.ui.add_participant_dialog import AddParticipantDialog
from combat_raven.models.combatant import CombatantType
from combat_raven.models.participant_template import ParticipantTemplate

def test_add_participant_dialog_has_participant_list(qtbot):
    repository = ParticipantRepository()

    dialog = AddParticipantDialog(repository)
    qtbot.addWidget(dialog)

    assert dialog.participant_list is not None

def test_add_participant_dialog_loads_participants(
    qtbot,
):
    repository = ParticipantRepository()

    fighter = ParticipantTemplate(
        name="Fighter",
        combatant_type=CombatantType.ALLY,
        max_hp=50,
    )

    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    repository.add(fighter)
    repository.add(goblin)

    dialog = AddParticipantDialog(repository)
    qtbot.addWidget(dialog)

    assert dialog.participant_list.count() == 2
    assert dialog.participant_list.item(0).text() == "Fighter"
    assert dialog.participant_list.item(1).text() == "Goblin"

def test_add_participant_dialog_returns_selected_participant(
    qtbot,
):
    repository = ParticipantRepository()

    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    repository.add(goblin)

    dialog = AddParticipantDialog(repository)
    qtbot.addWidget(dialog)

    dialog.participant_list.setCurrentRow(0)

    assert dialog.selected_participant_id == goblin.id

def test_add_participant_dialog_returns_none_without_selection(
    qtbot,
):
    repository = ParticipantRepository()

    dialog = AddParticipantDialog(repository)
    qtbot.addWidget(dialog)

    assert dialog.selected_participant_id is None

def test_add_participant_dialog_has_add_button(
    qtbot,
):
    repository = ParticipantRepository()

    dialog = AddParticipantDialog(repository)
    qtbot.addWidget(dialog)

    assert dialog.add_button is not None

def test_add_participant_dialog_has_cancel_button(
    qtbot,
):
    repository = ParticipantRepository()

    dialog = AddParticipantDialog(repository)
    qtbot.addWidget(dialog)

    assert dialog.cancel_button is not None

def test_add_participant_dialog_cancel_rejects(
    qtbot,
):
    repository = ParticipantRepository()

    dialog = AddParticipantDialog(repository)
    qtbot.addWidget(dialog)

    dialog.cancel_button.click()

    assert dialog.result() == 0

def test_add_participant_dialog_add_accepts_selected_participant(
    qtbot,
):
    repository = ParticipantRepository()

    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    repository.add(goblin)

    dialog = AddParticipantDialog(repository)
    qtbot.addWidget(dialog)

    dialog.participant_list.setCurrentRow(0)

    dialog.add_button.click()

    assert dialog.result() == 1
    assert dialog.selected_participant_id == goblin.id

def test_add_participant_dialog_add_without_selection_does_not_accept(
    qtbot,
):
    repository = ParticipantRepository()

    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    repository.add(goblin)

    dialog = AddParticipantDialog(repository)
    qtbot.addWidget(dialog)

    dialog.add_button.click()

    assert dialog.result() == 0

def test_add_participant_dialog_returns_selected_participant_after_add(
    qtbot,
):
    repository = ParticipantRepository()

    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    repository.add(goblin)

    dialog = AddParticipantDialog(repository)
    qtbot.addWidget(dialog)

    dialog.participant_list.setCurrentRow(0)
    dialog.add_button.click()

    assert dialog.result() == 1
    assert dialog.selected_participant_id == goblin.id