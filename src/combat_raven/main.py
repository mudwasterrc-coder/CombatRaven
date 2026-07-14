from models.combat import Combat
from models.combatant import Combatant


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

    print(combat)


if __name__ == "__main__":
    main()