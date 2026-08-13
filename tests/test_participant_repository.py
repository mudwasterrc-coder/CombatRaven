from combat_raven.models.participant_template import ParticipantTemplate
from combat_raven.models.combatant import CombatantType
from combat_raven.repositories.participant_repository import (
    ParticipantRepository,
)


def test_repository_stores_participant():
    repository = ParticipantRepository()

    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    repository.add(goblin)

    assert repository.get("Goblin") is goblin


def test_repository_lists_participants():
    repository = ParticipantRepository()

    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    fighter = ParticipantTemplate(
        name="Fighter",
        combatant_type=CombatantType.ALLY,
        max_hp=30,
    )

    repository.add(goblin)
    repository.add(fighter)

    assert repository.list() == [goblin, fighter]


def test_repository_removes_participant():
    repository = ParticipantRepository()

    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    repository.add(goblin)
    repository.remove(goblin.id)

    assert repository.get_by_id(goblin.id) is None

    
def test_repository_gets_participant_by_id():
    repository = ParticipantRepository()

    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    repository.add(goblin)

    assert repository.get_by_id(goblin.id) is goblin

def test_repository_gets_participant_by_name():
    repository = ParticipantRepository()

    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    repository.add(goblin)

    assert repository.get_by_name("Goblin") is goblin

def test_repository_allows_duplicate_names():
    repository = ParticipantRepository()

    first = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    second = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=10,
    )

    repository.add(first)
    repository.add(second)

    assert repository.list() == [first, second]

def test_repository_removes_participant_by_id():
    repository = ParticipantRepository()

    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    repository.add(goblin)
    repository.remove(goblin.id)

    assert repository.get_by_id(goblin.id) is None