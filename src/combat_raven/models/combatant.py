from dataclasses import dataclass, field

from combat_raven.models.effect import Effect
 


@dataclass
class Combatant:
    """
    Represents a participant in combat.
    """
    name: str
    initiative: int
    current_hp: int
    max_hp: int

    effects: list[Effect] = field(default_factory=list)
    
    def damage(self, amount: int) -> None:
        """
        Reduces the combatant's current HP by the specified amount.
        """
        self.current_hp = max(0, self.current_hp - amount)

    @property
    def is_dead(self) -> bool:
      """
      Returns True if the combatant's current HP is 0 or less, indicating they are dead.
      """

      return self.current_hp <= 0  

    def heal(self, amount: int) -> None:
        """
        Increases the combatant's current HP by the specified amount, up to their maximum HP.
        """
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def add_effect(self, effect: Effect) -> None:
        """
        Adds an effect to the combatant's list of effects.
        """
        self.effects.append(effect)

    def has_effect(self, name:str) -> bool:
        """
        Checks if the combatant has an effect with the specified name.
        """
        return any(effect.template.name == name for effect in self.effects)
    
    def advance_effects(self) -> None:
        """
        Advances all effects on the combatant by one round, reducing their remaining rounds.
        Removes any effects that have expired (remaining rounds <= 0).
        """
        for effect in self.effects:
            effect.tick()

        self.effects = [
            effect
            for effect in self.effects
            if effect.remaining_rounds > 0  
        ]
        