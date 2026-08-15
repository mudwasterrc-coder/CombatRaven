from combat_raven.models.combat import Combat
from combat_raven.repositories.combat_repository import CombatRepository


def test_combat_repository_saves_and_gets_combat(tmp_path):
    repository = CombatRepository(tmp_path)

    combat = Combat(
        name="Assault on the Tower",
    )

    repository.save(combat)

    loaded = repository.get_by_id(combat.id)

    assert loaded is not None
    assert loaded.id == combat.id
    assert loaded.name == "Assault on the Tower"

def test_combat_repository_lists_combats(tmp_path):
    repository = CombatRepository(tmp_path)

    first = Combat(name="Assault on the Tower")
    second = Combat(name="Crypt of Ravenloft")

    repository.save(first)
    repository.save(second)

    combats = repository.list()

    assert {combat.id for combat in combats} == {
        first.id,
        second.id,
    }

    assert {combat.name for combat in combats} == {
        "Assault on the Tower",
        "Crypt of Ravenloft",
    }

def test_combat_repository_deletes_combat(tmp_path):
    repository = CombatRepository(tmp_path)

    combat = Combat(name="Assault on the Tower")

    repository.save(combat)
    repository.delete(combat.id)

    assert repository.get_by_id(combat.id) is None

def test_combat_repository_updates_existing_combat(tmp_path):
    repository = CombatRepository(tmp_path)

    combat = Combat(name="Assault on the Tower")

    repository.save(combat)

    combat.name = "Assault on the Tower - Final Battle"

    repository.save(combat)

    loaded = repository.get_by_id(combat.id)

    assert loaded.name == "Assault on the Tower - Final Battle"

def test_combat_repository_allows_duplicate_names(tmp_path):
    repository = CombatRepository(tmp_path)

    first = Combat(name="Goblin Ambush")
    second = Combat(name="Goblin Ambush")

    repository.save(first)
    repository.save(second)

    combats = repository.list()

    assert {combat.id for combat in combats} == {
        first.id,
        second.id,
    }

def test_combat_repository_lists_combats_by_name(tmp_path):
    repository = CombatRepository(tmp_path)

    first = Combat(name="Zariel's Throne")
    second = Combat(name="Assault on the Tower")

    repository.save(first)
    repository.save(second)

    combats = repository.list()

    assert [combat.name for combat in combats] == [
        "Assault on the Tower",
        "Zariel's Throne",
    ]