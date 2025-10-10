from decimal import Decimal

from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.application.boundaries.use_case.validator.UseCaseInputNotificationErrors import (
    UseCaseInputNotificationErrors,
)


class ListBooksByPriceRangeUseCaseInput(UseCaseInput):

    def __init__(self, min_price: Decimal, max_price: Decimal) -> None:
        self._min_price = min_price
        self._max_price = max_price

    @property
    def min_price(self) -> Decimal:
        return self._min_price

    @property
    def max_price(self) -> Decimal:
        return self._max_price

    def validate_input(self, errors: UseCaseInputNotificationErrors) -> None:
        if self._min_price is None or self._min_price < 0:
            errors.add("min_price", "min_price cannot be None or negative")

        if self._max_price is None or self._max_price < 0:
            errors.add("max_price", "max_price cannot be None or negative")

        if self._min_price and self._max_price and self._min_price > self._max_price:
            errors.add("min_price", "min_price cannot be greater than max_price")
