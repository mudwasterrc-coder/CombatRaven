from dataclasses import dataclass

from combat_raven.models.effect_template import EffectTemplate




@dataclass(eq=False)
class Effect:
    """
    Represents an effect applied to a combatant.
    """

    template: EffectTemplate
    remaining_rounds: int | None
    concentration: bool
    enabled: bool = True
    notes: str = ""
    source_id: str | None = None
    concentration_id: str | None = None

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
        Effects without a duration never tick down.
        """
        if self.remaining_rounds is None:
            return

        self.remaining_rounds -= 1

    @property
    def is_expired(self) -> bool:
        """
        Returns True if the effect has run out of rounds.
        Effects without a duration never expire on their own.
        """
        return (
            self.remaining_rounds is not None
            and self.remaining_rounds <= 0
        )