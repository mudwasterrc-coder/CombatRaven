from dataclasses import dataclass

from combat_raven.models.effect_template import EffectTemplate




@dataclass
class Effect:
    """
    Represents an effect applied to a combatant.
    """

    template: EffectTemplate
    remaining_rounds: int | None
    concentration: bool
    enabled: bool = True
    notes: str = ""

    @classmethod
    def from_template(cls, template: EffectTemplate) -> "Effect":
        """
        Creates an Effect instance from an EffectTemplate.
        """
        return cls(
            template=template,
            remaining_rounds=template.default_duration,
            concentration=template.concentration,
            notes=template.notes,
        )
    
    def tick(self) -> None:
        """
        Advances the effect by one round, reducing the remaining rounds by 1.
        """

        self.remaining_rounds -= 1