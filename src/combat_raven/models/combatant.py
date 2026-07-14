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
    