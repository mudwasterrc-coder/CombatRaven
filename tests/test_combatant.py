from combat_raven.models.combatant import Combatant

def test_damage_reduces_hp():
    strahd = Combatant(
        name="Strahd",
        initiative=22,
        current_hp=350,
        max_hp=350,
    )
    strahd.damage(50)
    assert strahd.current_hp == 300