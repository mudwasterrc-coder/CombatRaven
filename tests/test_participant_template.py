from combat_raven.models.participant_template import ParticipantTemplate
from combat_raven.models.combatant import CombatantType


def test_participant_template_stores_reusable_data():
    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
        legendary_action_limit=0,
    )

    assert goblin.name == "Goblin"
    assert goblin.combatant_type == CombatantType.ENEMY
    assert goblin.max_hp == 7
    assert goblin.legendary_action_limit == 0

def test_participant_template_creates_combatant_instance():
    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
        legendary_action_limit=0,
    )

    combatant = goblin.create_combatant(initiative=15)

    assert combatant.name == "Goblin"
    assert combatant.combatant_type == CombatantType.ENEMY
    assert combatant.max_hp == 7
    assert combatant.current_hp == 7
    assert combatant.initiative == 15

def test_template_instances_have_independent_state():
    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    first = goblin.create_combatant(initiative=15)
    second = goblin.create_combatant(initiative=10)

    first.current_hp = 2

    assert first.current_hp == 2
    assert second.current_hp == 7

def test_participant_templates_have_unique_ids():
    first = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    second = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    assert first.id != second.id

def test_participant_template_can_have_specific_id():
    participant_id = "goblin-123"

    goblin = ParticipantTemplate(
        id=participant_id,
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
    )

    assert goblin.id == participant_id

def test_template_passes_concentration_limit_to_combatant():
    wizard = ParticipantTemplate(
        name="Wizard",
        combatant_type=CombatantType.ALLY,
        max_hp=18,
        concentration_limit=2,
    )

    combatant = wizard.create_combatant(initiative=14)

    assert combatant.concentration_limit == 2

def test_template_rolls_initiative_with_its_bonus():
    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
        initiative_bonus=2,
    )

    loaded_die = lambda: 12

    assert goblin.roll_initiative(d20=loaded_die) == 14

def test_template_rolls_a_real_d20_by_default():
    goblin = ParticipantTemplate(
        name="Goblin",
        combatant_type=CombatantType.ENEMY,
        max_hp=7,
        initiative_bonus=2,
    )

    rolls = [goblin.roll_initiative() for _ in range(200)]

    assert all(3 <= roll <= 22 for roll in rolls)