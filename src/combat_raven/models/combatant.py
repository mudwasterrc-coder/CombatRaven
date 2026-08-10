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
    legendary_action_limit: int = 0

    effects: list[Effect] = field(default_factory=list)

    _reaction_available: bool = field(default=True, init=False, repr=False)

    _concentration_effects: list[Effect] = field(
        default_factory=list, 
        init=False,
        repr=False 
    )

    _legendary_actions_used: int = field(
        default=0,
        init=False,
        repr=False 
    )
    @property
    def legendary_actions_used(self) -> int:
        """
        Returns the number of legendary actions used during the current round.
        """
        return self._legendary_actions_used
    
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

    def use_legendary_action(self) -> bool:
        """
        Uses one legendary action if one is available.

        Returns True if the action was successfully used, or False if no legendary actions are available.
        """

        if not self.can_use_legendary_action():
            return False
        
        self._legendary_actions_used += 1
        return True

    def reset_legendary_actions(self) -> None:
        """
        Resets legendary actions for the next round.
        """
        self._legendary_actions_used = 0

    def can_use_legendary_action(self) -> bool:
        """
        Returns True if the combatant has a legendary action available to use.
        """
        return self._legendary_actions_used < self.legendary_action_limit

    def is_concentrating(self) -> bool:
        """
        Checks if the combatant is currently concentrating on any effect.
        """
        return len(self._concentration_effects) > 0

    def start_concentration(self, effect: Effect) -> None:
        """
        Starts concentration on an effect, replacing any existing concentration.
        """
        self._concentration_effects.clear()
        self._concentration_effects.append(effect)

    @property
    def concentration_effects(self) -> tuple[Effect, ...]:
        """
        Returns the effects the combatant is currently concentrating on.
        """
        return tuple(self._concentration_effects)
        

    def end_concentration(self) -> None:
        """
       Ends concentration on all concentration effects.
        """

        for effect in self._concentration_effects:
            if effect in self.effects:
                self.effects.remove(effect)

        self._concentration_effects.clear()