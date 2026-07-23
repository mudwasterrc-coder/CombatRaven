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

    _reaction_available: bool = field(default=True, init=False, repr=False)
    _concentrating: bool = field(default=False, init=False, repr=False)
    
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

    def can_react(self) -> bool:
        """
        Checks if the combatant can use a reaction.
        """
        return self._reaction_available

    def use_reaction(self) -> None:
        """
        Marks the combatant's reaction as used for the current round.
        """
        self._reaction_available = False

    def reset_reaction(self) -> None:
        """
        Resets the combatant's reaction availability for the next round.
        """
        self._reaction_available = True

    def is_concentrating(self) -> bool:
        """
        Checks if the combatant is currently concentrating on any effect.
        """
        return self._concentrating

    def start_concentration(self) -> None:
        """
        Marks the combatant as concentrating on an effect.
        """
        self._concentrating = True

    def end_concentration(self) -> None:
        """
        Marks the combatant as no longer concentrating on any effect.
        """
        self._concentrating = False