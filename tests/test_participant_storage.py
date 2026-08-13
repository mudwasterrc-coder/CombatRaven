import pytest

from combat_raven.models.combatant import CombatantType
from combat_raven.models.participant_template import ParticipantTemplate
from combat_raven.repositories.participant_repository import (
    ParticipantRepository,
)
from combat_raven.storage.participant_storage import ParticipantStorage


def test_storage_saves_participant_templates(tmp_path):
    repository = ParticipantRepository()

    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
        legendary_action_limit=0,
    )

    repository.add(goblin)

    storage = ParticipantStorage(tmp_path / "participants.json")

    storage.save(repository)

    assert (tmp_path / "participants.json").exists()


def test_storage_loads_participant_templates(tmp_path):
    path = tmp_path / "participants.json"

    original_repository = ParticipantRepository()

    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
        legendary_action_limit=0,
    )

    original_repository.add(goblin)

    storage = ParticipantStorage(path)
    storage.save(original_repository)

    loaded_repository = storage.load()

    loaded = loaded_repository.get_by_id(goblin.id)

    assert loaded is not None
    assert loaded.id == goblin.id
    assert loaded.name == "Goblin"
    assert loaded.combatant_type == CombatantType.ENEMY
    assert loaded.max_hp == 7
    assert loaded.legendary_action_limit == 0


def test_storage_preserves_multiple_participants_with_same_name(tmp_path):
    repository = ParticipantRepository()

    first = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    second = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=12,
    )

    repository.add(first)
    repository.add(second)

    storage = ParticipantStorage(
        tmp_path / "participants.json"
    )

    storage.save(repository)

    loaded_repository = storage.load()

    assert loaded_repository.get_by_id(first.id).max_hp == 7
    assert loaded_repository.get_by_id(second.id).max_hp == 12

def test_storage_preserves_participant_ids(tmp_path):
    repository = ParticipantRepository()

    goblin = ParticipantTemplate(
        id="goblin-fixed-id",
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    repository.add(goblin)

    storage = ParticipantStorage(
        tmp_path / "participants.json"
    )

    storage.save(repository)

    loaded_repository = storage.load()

    assert loaded_repository.get_by_id("goblin-fixed-id") is not None

def test_storage_load_missing_file(tmp_path):
    storage = ParticipantStorage(
        tmp_path / "does_not_exist.json"
    )

    repository = storage.load()

    assert repository.list() == []

def test_storage_rejects_invalid_json(tmp_path):
    path = tmp_path / "participants.json"
    path.write_text("this is not json", encoding="utf-8")

    storage = ParticipantStorage(path)

    with pytest.raises(ValueError):
        storage.load()