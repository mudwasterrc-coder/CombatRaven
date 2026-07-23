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