from dataclasses import dataclass


@dataclass
class EffectTemplate:
    """
    Represents a reusable effect template.
    """

    name: str
    default_duration: int | None
    concentration: bool = False
    notes: str = ""
