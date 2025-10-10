from decimal import Decimal

import pytest

from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.application.boundaries.use_case.validator.UseCaseInputNotificationErrors import (
    UseCaseInputNotificationErrors,
)
from src.application.use_cases.book.list_books_by_price_range.ListBooksByPriceRangeUseCaseInput import (
    ListBooksByPriceRangeUseCaseInput,
)


class TestListBooksByPriceRangeUseCaseInput:
    def test_class_is_subclass_input(self) -> None:
        # arrange - act - assert
        assert issubclass(ListBooksByPriceRangeUseCaseInput, UseCaseInput)

    def test_class_initialized_successfully(self) -> None:
        # arrange - act - assert
        ListBooksByPriceRangeUseCaseInput(Decimal(10), Decimal(20))

    @pytest.mark.parametrize(
        "min_price, max_price",
        [
            (Decimal(0), Decimal(0)),
            (Decimal(10), Decimal(20)),
            (Decimal(20), Decimal(20)),
        ],
    )
    def test_validate_input_successfully(self, min_price: Decimal, max_price: Decimal) -> None:
        # arrange
        use_case_input: ListBooksByPriceRangeUseCaseInput = ListBooksByPriceRangeUseCaseInput(
            min_price, max_price
        )

        errors = UseCaseInputNotificationErrors.empty()

        # act
        use_case_input.validate_input(errors)

        # assert
        assert errors.has_errors is False
        assert errors.flatten_errors == {}

    @pytest.mark.parametrize(
        ("min_price", "max_price", "expected_result"),
        [
            (
                None,
                None,
                {
                    "max_price_1": "max_price cannot be None or negative",
                    "min_price_1": "min_price cannot be None or negative",
                },
            ),
            (
                Decimal(-1),
                Decimal(-1),
                {
                    "max_price_1": "max_price cannot be None or negative",
                    "min_price_1": "min_price cannot be None or negative",
                },
            ),
            (
                Decimal(20),
                Decimal(10),
                {"min_price_1": "min_price cannot be greater than max_price"},
            ),
        ],
    )
    def test_validate_input_invalid_when_all_params_invalid(
        self, min_price: Decimal, max_price: Decimal, expected_result: dict
    ) -> None:
        # arrange
        use_case_input: ListBooksByPriceRangeUseCaseInput = ListBooksByPriceRangeUseCaseInput(
            min_price, max_price
        )

        errors = UseCaseInputNotificationErrors.empty()

        # act
        use_case_input.validate_input(errors)

        # assert
        assert errors.has_errors is True
        assert errors.flatten_errors == expected_result
