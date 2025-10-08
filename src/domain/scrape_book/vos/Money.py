from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Self


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "GBP"

    def __post_init__(self) -> None:
        object.__setattr__(self, "amount", self._to_decimal(self.amount))

        if self.amount < 0:
            raise ValueError("Money cannot be negative")

    @classmethod
    def from_float(cls, amount: float, currency: str = "GBP") -> Self:
        return cls(cls._to_decimal(amount), currency)

    @classmethod
    def from_string(cls, amount: str, currency: str = "GBP") -> Self:
        return cls(cls._to_decimal(amount), currency)

    @staticmethod
    def _to_decimal(value: float | Decimal | str) -> Decimal:
        if isinstance(value, Decimal):
            return value

        if isinstance(value, float):
            value = format(value, "f")
        return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
