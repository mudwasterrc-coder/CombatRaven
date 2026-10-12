from combat_raven.models.combatant import Combatant, CombatantType
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

def test_combatant_defaults_to_ally():
    combatant = Combatant(
        name="Fighter",
        initiative=20,
        current_hp=30,
        max_hp=30,
    )

    assert combatant.combatant_type == CombatantType.ALLY

def test_combatant_can_be_an_enemy():
    goblin = Combatant(
        name="Goblin",
        initiative=10,
        current_hp=7,
        max_hp=7,
        combatant_type=CombatantType.ENEMY,
    )

    assert goblin.combatant_type == CombatantType.ENEMY

def test_effect_without_duration_survives_advancing_effects():
    barbarian = Combatant(
        name="Barbarian",
        initiative=14,
        current_hp=45,
        max_hp=45,
    )
    rage = Effect.from_template(
        EffectTemplate(name="Rage", default_duration=None)
    )
    barbarian.add_effect(rage)

    barbarian.advance_effects()

    assert barbarian.effects == [rage]
    assert rage.remaining_rounds is None

def test_combatant_at_zero_hp_is_down():
    goblin = Combatant(name="Goblin", initiative=12, current_hp=7, max_hp=7)

    assert goblin.is_down is False

    goblin.damage(7)

    assert goblin.is_down is True

def test_each_combatant_has_a_unique_id():
    first = Combatant(name="Goblin", initiative=12, current_hp=7, max_hp=7)
    second = Combatant(name="Goblin", initiative=12, current_hp=7, max_hp=7)

    assert first.id
    assert first.id != second.id