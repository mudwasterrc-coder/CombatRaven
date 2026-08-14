import json

from combat_raven.models.combat import Combat
from combat_raven.models.combatant import Combatant, CombatantType
from combat_raven.storage.combat_storage import CombatStorage
from combat_raven.models.effect import Effect
from combat_raven.models.effect_template import EffectTemplate


def test_storage_saves_combat(tmp_path):
    combat = Combat()

    fighter = Combatant(
        name = "Fighter",
        initiative=20,
        current_hp=30,
        max_hp=30,
    )

    combat.add_combatant(fighter)

    storage = CombatStorage(
        tmp_path / "combat.json"
    )

    storage.save(combat)

    assert (tmp_path / "combat.json").exists()

def test_storage_loads_combat(tmp_path):
    path = tmp_path / "combat.json"

    combat = Combat()

    fighter = Combatant(
        name="Fighter",
        initiative=20,
        current_hp=17,
        max_hp=30,
    )

    combat.add_combatant(fighter)
    combat.start()

    storage = CombatStorage(path)
    storage.save(combat)

    loaded = storage.load()

    assert loaded.current_round == 1
    assert loaded.current_turn_index == 0
    assert loaded.started is True
    assert len(loaded.combatants) == 1

    loaded_fighter = loaded.combatants[0]

    assert loaded_fighter.name == "Fighter"
    assert loaded_fighter.initiative == 20
    assert loaded_fighter.current_hp == 17
    assert loaded_fighter.max_hp == 30

def test_storage_preserves_current_turn(tmp_path):
    path = tmp_path / "combat.json"

    combat = Combat()

    fighter = Combatant(
        name="Fighter",
        initiative=20,
        current_hp=30,
        max_hp=30,
    )

    wizard = Combatant(
        name="Wizard",
        initiative=15,
        current_hp=20,
        max_hp=20,
    )

    goblin = Combatant(
        name="Goblin",
        initiative=10,
        current_hp=7,
        max_hp=7,
    )

    combat.add_combatant(fighter)
    combat.add_combatant(wizard)
    combat.add_combatant(goblin)

    combat.start()

    combat.next_turn()

    storage = CombatStorage(path)
    storage.save(combat)

    loaded = storage.load()

    assert loaded.current_round == combat.current_round
    assert loaded.current_turn_index == combat.current_turn_index
    assert (
        loaded.current_combatant.name
        == combat.current_combatant.name
    )

def test_storage_preserves_turn_after_multiple_rounds(tmp_path):
    path = tmp_path / "combat.json"

    combat = Combat()

    fighter = Combatant(
        name="Fighter",
        initiative=20,
        current_hp=30,
        max_hp=30,
    )

    wizard = Combatant(
        name="Wizard",
        initiative=15,
        current_hp=20,
        max_hp=20,
    )

    combat.add_combatant(fighter)
    combat.add_combatant(wizard)

    combat.start()

    combat.next_turn()
    combat.next_turn()

    storage = CombatStorage(path)
    storage.save(combat)

    loaded = storage.load()

    assert loaded.current_round == combat.current_round
    assert loaded.current_turn_index == combat.current_turn_index
    assert (
        loaded.current_combatant.name
        == combat.current_combatant.name
    )

def test_storage_saves_current_turn_state(tmp_path):
    path = tmp_path / "combat.json"

    combat = Combat()

    fighter = Combatant(
        name="Fighter",
        initiative=20,
        current_hp=30,
        max_hp=30,
    )

    wizard = Combatant(
        name="Wizard",
        initiative=15,
        current_hp=20,
        max_hp=20,
    )

    combat.add_combatant(fighter)
    combat.add_combatant(wizard)

    combat.start()
    combat.next_turn()
    combat.next_turn()

    storage = CombatStorage(path)
    storage.save(combat)

    data = json.loads(
        path.read_text(encoding="utf-8")
    )

    assert data["current_round"] == combat.current_round
    assert data["current_turn_index"] == combat.current_turn_index
    assert data["started"] is True

def test_storage_preserves_combatant_type(tmp_path):
    path = tmp_path / "combat.json"

    combat = Combat()

    fighter = Combatant(
        name="Fighter",
        initiative=20,
        current_hp=30,
        max_hp=30,
        combatant_type=CombatantType.ALLY,
    )

    goblin = Combatant(
        name="Goblin",
        initiative=10,
        current_hp=7,
        max_hp=7,
        combatant_type=CombatantType.ENEMY,
    )

    combat.add_combatant(fighter)
    combat.add_combatant(goblin)

    storage = CombatStorage(path)
    storage.save(combat)

    loaded = storage.load()

    assert loaded.combatants[0].combatant_type == CombatantType.ALLY
    assert loaded.combatants[1].combatant_type == CombatantType.ENEMY

def test_storage_preserves_combatant_effect(tmp_path):
    path = tmp_path / "combat.json"

    combat = Combat()

    fighter = Combatant(
        name="Fighter",
        initiative=20,
        current_hp=30,
        max_hp=30,
    )

    bless = EffectTemplate(
        name="Bless",
        default_duration=10,
        concentration=True,
        notes="+1d4 to attack rolls and saving throws",
    )

    effect = Effect.from_template(bless)
    effect.tick()
    effect.tick()

    fighter.effects.append(effect)
    combat.add_combatant(fighter)

    storage = CombatStorage(path)
    storage.save(combat)

    loaded = storage.load()

    loaded_effect = loaded.combatants[0].effects[0]

    assert loaded_effect.template.name == "Bless"
    assert loaded_effect.remaining_rounds == 8
    assert loaded_effect.concentration is True
    assert loaded_effect.enabled is True
    assert loaded_effect.notes == "+1d4 to attack rolls and saving throws"

def test_storage_preserves_combat_identity(tmp_path):
    path = tmp_path / "combat.json"

    combat = Combat(
        id="encounter-123",
        name="Assault on the Tower",
    )

    fighter = Combatant(
        name="Fighter",
        initiative=20,
        current_hp=30,
        max_hp=30,
    )

    combat.add_combatant(fighter)

    storage = CombatStorage(path)
    storage.save(combat)

    loaded = storage.load()

    assert loaded.id == "encounter-123"
    assert loaded.name == "Assault on the Tower"

def test_storage_loads_legacy_combat_without_identity(tmp_path):
    path = tmp_path / "legacy_combat.json"

    path.write_text(
        """
        {
            "current_round": 0,
            "current_turn_index": 0,
            "started": false,
            "combatants": []
        }
        """,
        encoding="utf-8",
    )

    storage = CombatStorage(path)

    loaded = storage.load()

    assert loaded.id
    assert loaded.name == "Unnamed Encounter"