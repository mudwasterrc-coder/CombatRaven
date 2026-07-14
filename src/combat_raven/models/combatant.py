from dataclasses import dataclass

@dataclass
class Combatant:
    """
    Represents a participant in combat.
    """
    name: str
    initiative: int
    current_hp: int
    max_hp: int
    
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