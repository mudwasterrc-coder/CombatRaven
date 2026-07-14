from combat_raven.models.combat import Combat
from combat_raven.models.combatant import Combatant


def main():
    combat = Combat()

    aaron = Combatant(
        name="Aaron",
        initiative=18,
        current_hp=87,
        max_hp=87,
    )

    strahd = Combatant(
        name="Strahd",
        initiative=22,
        current_hp=350,
        max_hp=350,
    )

    combat.add_combatant(aaron)
    combat.add_combatant(strahd)

    combat.start()

    print(combat.current_combatant.name)

    combat.next_turn()

    print(combat.current_combatant.name)

    combat.next_turn()

    print(combat.current_combatant.name)


if __name__ == "__main__":
    main()