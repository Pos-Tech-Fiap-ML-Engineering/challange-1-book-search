import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Upc:
    value: str

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[A-Za-z0-9]+", self.value):
            raise ValueError("Upc invalid (only [A-Za-z0-9]).")
