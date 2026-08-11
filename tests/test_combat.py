from combat_raven.models.combat import Combat
from combat_raven.models.combatant import Combatant
from combat_raven.models.effect import Effect
from combat_raven.models.effect_template import EffectTemplate

def test_can_add_combatants():
    combat = Combat()

    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=100,
        max_hp=100,
    )

    goblin = Combatant(
        name="Goblin",
        initiative=12,
        current_hp=7,
        max_hp=7,
    )

    combat.add_combatant(fighter)
    combat.add_combatant(goblin)

    assert len(combat.combatants) == 2

def test_next_turn_advances_new_current_combatants_effects():
    fighter = Combatant(
        name="Fighter",
        max_hp=30,
        current_hp=30,
        initiative=20,
    )

    goblin = Combatant(
        name="Goblin",
        max_hp=7,
        current_hp=7,
        initiative=10,
    )

    bless = EffectTemplate(
        name="Bless",
        default_duration=2,
    )

    goblin.add_effect(Effect.from_template(bless))

    combat = Combat()

    combat.add_combatant(fighter)
    combat.add_combatant(goblin)

    combat.start()

    assert combat.current_combatant is fighter

    combat.next_turn()

    assert combat.current_combatant is goblin
    assert goblin.effects[0].remaining_rounds == 1

def test_next_turn_restores_current_combatants_reaction():
    fighter = Combatant(
        name="Fighter",
        max_hp=30,
        current_hp=30,
        initiative=20,
    )

    goblin = Combatant(
        name="Goblin",
        max_hp=7,
        current_hp=7,
        initiative=10,
    )

    goblin.use_reaction()

    combat = Combat()

    combat.add_combatant(fighter)
    combat.add_combatant(goblin)

    combat.start()

    combat.next_turn()

    assert combat.current_combatant is goblin
    assert goblin.can_react() is True

def test_next_round_restores_legendary_actions():
    fighter = Combatant(
        name="Fighter",
        max_hp=30,
        current_hp=30,
        initiative=20,
        legendary_action_limit=3,
    )

    goblin = Combatant(
        name="Goblin",
        max_hp=7,
        current_hp=7,
        initiative=10,
    )

    combat = Combat()

    combat.add_combatant(fighter)
    combat.add_combatant(goblin)

    combat.start()

    fighter.use_legendary_action()
    fighter.use_legendary_action()
    fighter.use_legendary_action()

    assert fighter.legendary_actions_used == 3

    combat.next_turn()
    assert combat.current_round == 1

    combat.next_turn()

    assert combat.current_round == 2
    assert fighter.legendary_actions_used == 0

def test_combat_can_remove_a_combatant():
    fighter = Combatant(
        name="Fighter",
        max_hp=30,
        current_hp=30,
        initiative=15,
    )

    goblin = Combatant(
        name="Goblin",
        max_hp=7,
        current_hp=7,
        initiative=10,
    )

    combat = Combat()

    combat.add_combatant(fighter)
    combat.add_combatant(goblin)

    combat.remove_combatant(fighter)

    assert combat.combatants == [goblin]

def test_removing_combatant_after_current_turn_keeps_current_turn():
    fighter = Combatant(
        name="Fighter",
        max_hp=30,
        current_hp=30,
        initiative=20,
    )

    goblin = Combatant(
        name="Goblin",
        max_hp=7,
        current_hp=7,
        initiative=15,
    )

    orc = Combatant(
        name="Orc",
        max_hp=15,
        current_hp=15,
        initiative=10,
    )

    combat = Combat()

    combat.add_combatant(fighter)
    combat.add_combatant(goblin)
    combat.add_combatant(orc)

    combat.start()

    assert combat.current_combatant is fighter

    combat.remove_combatant(orc)

    assert combat.current_combatant is fighter

def test_removing_combatant_before_current_turn_keeps_current_turn():
    fighter = Combatant(
        name="Fighter",
        max_hp=30,
        current_hp=30,
        initiative=20,
    )

    wizard = Combatant(
        name="Wizard",
        max_hp=20,
        current_hp=20,
        initiative=15,
    )

    goblin = Combatant(
        name="Goblin",
        max_hp=7,
        current_hp=7,
        initiative=10,
    )

    combat = Combat()

    combat.add_combatant(fighter)
    combat.add_combatant(wizard)
    combat.add_combatant(goblin)

    combat.start()

    combat.next_turn()

    assert combat.current_combatant is wizard

    combat.remove_combatant(fighter)

    assert combat.current_combatant is wizard

def test_removing_current_combatant_advances_to_next_turn():
    fighter = Combatant(
        name="Fighter",
        max_hp=30,
        current_hp=30,
        initiative=20,
    )

    wizard = Combatant(
        name="Wizard",
        max_hp=20,
        current_hp=20,
        initiative=15,
    )

    goblin = Combatant(
        name="Goblin",
        max_hp=7,
        current_hp=7,
        initiative=10,
    )

    combat = Combat()

    combat.add_combatant(fighter)
    combat.add_combatant(wizard)
    combat.add_combatant(goblin)

    combat.start()

    assert combat.current_combatant is fighter

    combat.remove_combatant(fighter)

    assert combat.current_combatant is wizard

def test_removing_last_combatant_keeps_a_valid_current_turn():
    fighter = Combatant(
        name="Fighter",
        max_hp=30,
        current_hp=30,
        initiative=20,
    )

    wizard = Combatant(
        name="Wizard",
        max_hp=20,
        current_hp=20,
        initiative=15,
    )

    goblin = Combatant(
        name="Goblin",
        max_hp=7,
        current_hp=7,
        initiative=10,
    )

    combat = Combat()

    combat.add_combatant(fighter)
    combat.add_combatant(wizard)
    combat.add_combatant(goblin)

    combat.start()

    combat.next_turn()
    combat.next_turn()

    assert combat.current_combatant is goblin

    combat.remove_combatant(goblin)

    assert combat.current_combatant is fighter

def test_removing_only_combatant_leaves_combat_empty():
    fighter = Combatant(
        name="Fighter",
        max_hp=30,
        current_hp=30,
        initiative=15,
    )

    combat = Combat()
    combat.add_combatant(fighter)
    combat.start()

    combat.remove_combatant(fighter)

    assert combat.combatants == []
    assert combat.current_turn_index == 0