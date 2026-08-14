import json

from combat_raven.models.combat import Combat
from combat_raven.models.combatant import Combatant, CombatantType
from combat_raven.models.effect import Effect
from combat_raven.models.effect_template import EffectTemplate

class CombatStorage:
    """
    Persists combat encounters as JSON
    """

    def __init__(self, path):
        self.path = path

    def save(self, combat) -> None:
        """
        Saves a combat encounter to disk
        """
        data = {
            "current_round": combat.current_round,
            "current_turn_index": combat.current_turn_index,
            "started": combat.started,
            "combatants": [
                {
                    "name": combatant.name,
                    "initiative": combatant.initiative,
                    "current_hp": combatant.current_hp,
                    "max_hp": combatant.max_hp,
                    "combatant_type": combatant.combatant_type.value,
                    "effects": [
                        {
                            "template": {
                                "name": effect.template.name,
                                "default_duration": effect.template.default_duration,
                                "concentration": effect.template.concentration,
                                "notes": effect.template.notes,
                            },
                            "remaining_rounds": effect.remaining_rounds,
                            "concentration": effect.concentration,
                            "enabled": effect.enabled,
                            "notes": effect.notes,
                        }
                        for effect in combatant.effects
                    ],
                }
                for combatant in combat.combatants
            ],
        }

        self.path.write_text(
            json.dumps(data, indent=4),
            encoding="utf-8",
        )

    def load(self) -> Combat:
        """
        Loads a combat encounter from disk.
        """
        data = json.loads(
            self.path.read_text(encoding="utf-8")
        )

        combat = Combat()

        for item in data["combatants"]:
            combatant = Combatant(
                name=item["name"],
                initiative=item["initiative"],
                current_hp=item["current_hp"],
                max_hp=item["max_hp"],
                combatant_type=CombatantType(item["combatant_type"]),
            )

            for effect_data in item.get("effects", []):
                template_data = effect_data["template"]

                template = EffectTemplate(
                    name=template_data["name"],
                    default_duration=template_data["default_duration"],
                    concentration=template_data["concentration"],
                    notes=template_data["notes"],
                )

                effect = Effect(
                    template=template,
                    remaining_rounds=effect_data["remaining_rounds"],
                    concentration=effect_data["concentration"],
                    enabled=effect_data["enabled"],
                    notes=effect_data["notes"],
                )

                combatant.effects.append(effect)

            combat.add_combatant(combatant)

        if data["started"]:
            combat.restore_state(
                current_round=data["current_round"],
                current_turn_index=data["current_turn_index"],
            )

        return combat