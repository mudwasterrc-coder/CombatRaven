from combat_raven.models.combatant import Combatant
from combat_raven.models.effect import Effect
from combat_raven.models.effect_template import EffectTemplate


def test_damage_reduces_hp():
    strahd = Combatant(
        name="Strahd",
        initiative=22,
        current_hp=350,
        max_hp=350,
    )
    strahd.damage(50)
    assert strahd.current_hp == 300

def test_fighter_damage():
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=100,
        max_hp=100,
    )
    fighter.damage(30)
    assert fighter.current_hp == 70

def test_combatant_starts_with_no_effects():
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=100,
        max_hp=100,
    )
    assert len(fighter.effects) == 0
    

def test_add_effect_to_combatant():
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=100,
        max_hp=100,
    )
    bless = EffectTemplate(
        name="Bless",
        default_duration=10,
        concentration=True,
        notes="+1d4 to attack rolls and saving throws",
    )
    effect = Effect.from_template(bless)

    fighter.add_effect(effect)

    assert len(fighter.effects) == 1
    assert fighter.effects[0] == effect


def test_combatant_has_effect():
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=100,
        max_hp=100,
    )
    bless = EffectTemplate(
        name="Bless",
        default_duration=10,
        concentration=True,
        notes="+1d4 to attack rolls and saving throws",
    )
    effect = Effect.from_template(bless)

    fighter.add_effect(effect)

    assert fighter.has_effect("Bless") is True
    assert fighter.has_effect("Haste") is False

def test_advance_effect_reduces_duration():
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=100,
        max_hp=100,
    )
    bless = EffectTemplate(
        name="Bless",
        default_duration=10,
        concentration=True,
        notes="+1d4 to attack rolls and saving throws",
    )
    effect = Effect.from_template(bless)

    fighter.add_effect(effect)

    fighter.advance_effects()

    assert fighter.effects[0].remaining_rounds == 9

def test_expired_effects_are_removed():
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=100,
        max_hp=100,
    )
    bless = EffectTemplate(
        name="Bless",
        default_duration=1,
        concentration=True,
        notes="+1d4 to attack rolls and saving throws",
    )
    effect = Effect.from_template(bless)

    fighter.add_effect(effect)

    fighter.advance_effects()

    assert fighter.has_effect("Bless") is False
    assert len(fighter.effects) == 0

def test_combatant_can_use_reaction():
    fighter = Combatant(
        name="Fighter",
        max_hp=30,
        current_hp=30,
        initiative=15,
    )

    assert fighter.can_react() is True

    fighter.use_reaction()

    assert fighter.can_react() is False

def test_combatant_can_start_and_end_concentration():
    fighter = Combatant(
        name="Fighter",
        max_hp=30,
        current_hp=30,
        initiative=15,
    )

    bless = Effect.from_template(
        EffectTemplate(
            name="Bless",
            default_duration=10,
            concentration=True,
        )
    )

    fighter.start_concentration(bless)

    assert fighter.is_concentrating()

    fighter.end_concentration()

    assert not fighter.is_concentrating()
    assert fighter.concentration_effects == ()

def test_combatant_can_concentrate_on_an_effect():
    fighter = Combatant(
        name="Fighter",
        max_hp=30,
        current_hp=30,
        initiative=15,
    )

    bless_template = EffectTemplate(
            name="Bless",
            default_duration=10,
            concentration=True,
        )

    bless = Effect.from_template(bless_template)

    assert fighter.is_concentrating() is False

    fighter.start_concentration(bless)

    assert fighter.is_concentrating() is True
    assert fighter.concentration_effects == (bless,)

def test_starting_a_new_concentration_replaces_the_previous_one():
    fighter = Combatant(
        name="Fighter",
        max_hp=30,
        current_hp=30,
        initiative=15,
    )

    bless = Effect.from_template(
        EffectTemplate(
            name="Bless",
            default_duration=10,
            concentration=True,
        )
    )

    fly = Effect.from_template(
        EffectTemplate(
            name="Fly",
            default_duration=10,
            concentration=True,
        )
    )

    fighter.start_concentration(bless)
    fighter.start_concentration(fly)

    assert fighter.is_concentrating()
    assert fighter.concentration_effects == (fly,)

def test_ending_concentration_removes_the_concentrated_effect():
    fighter = Combatant(
        name="Fighter",
        max_hp=30,
        current_hp=30,
        initiative=15,
    )

    bless = Effect.from_template(
        EffectTemplate(
            name="Bless",
            default_duration=10,
            concentration=True,
        )
    )

    fighter.add_effect(bless)
    fighter.start_concentration(bless)

    fighter.end_concentration()

    assert fighter.is_concentrating() is False
    assert fighter.concentration_effects == ()
    assert fighter.effects == []

def test_combatant_starts_with_no_legendary_actions_used():
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
    )

    assert fighter.legendary_actions_used == 0  

def test_combatant_has_a_legendary_action_limit():
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
        legendary_action_limit=3,
    )   

    assert fighter.legendary_action_limit == 3

def test_combatant_can_use_a_legendary_action():
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
        legendary_action_limit=3,
    )   

    fighter.use_legendary_action()

    assert fighter.legendary_actions_used == 1

def test_combatant_cannot_use_more_legendary_actions_than_limit():
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
        legendary_action_limit=3,
    )

    assert fighter.can_use_legendary_action() is True

    fighter.use_legendary_action()
    fighter.use_legendary_action()
    fighter.use_legendary_action()

    assert fighter.can_use_legendary_action() is False

def test_using_a_legendary_action_when_none_are_available_fails():
    fighter = Combatant(
        name="Fighter",
        initiative=15,
        current_hp=30,
        max_hp=30,
        legendary_action_limit=1,
    )

    fighter.use_legendary_action()

    assert fighter.can_use_legendary_action() is False
    assert fighter.use_legendary_action() is False
    assert fighter.legendary_actions_used == 1