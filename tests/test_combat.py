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