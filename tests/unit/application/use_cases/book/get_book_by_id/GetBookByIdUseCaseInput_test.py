import pytest

from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.application.boundaries.use_case.validator.UseCaseInputNotificationErrors import (
    UseCaseInputNotificationErrors,
)
from src.application.use_cases.book.get_book_by_id.GetBookByIdUseCaseInput import (
    GetBookByIdUseCaseInput,
)


class TestGetBookByIdUseCaseInput:
    def test_class_is_subclass_input(self) -> None:
        # arrange - act - assert
        assert issubclass(GetBookByIdUseCaseInput, UseCaseInput)

    def test_class_initialized_successfully(self) -> None:
        # arrange - act - assert
        GetBookByIdUseCaseInput(10)

    @pytest.mark.parametrize("book_id", [10, 0])
    def test_validate_input_successfully(self, book_id: int) -> None:
        # arrange
        use_case_input: GetBookByIdUseCaseInput = GetBookByIdUseCaseInput(book_id)

        errors = UseCaseInputNotificationErrors.empty()

        # act
        use_case_input.validate_input(errors)

        # assert
        assert errors.has_errors is False
        assert errors.flatten_errors == {}

    @pytest.mark.parametrize("book_id", [-10, None])
    def test_validate_input_with_errors_when_id_invalid(self, book_id: int) -> None:
        # arrange
        use_case_input: GetBookByIdUseCaseInput = GetBookByIdUseCaseInput(book_id)

        errors = UseCaseInputNotificationErrors.empty()

        # act
        use_case_input.validate_input(errors)

        # assert
        assert errors.has_errors is True
        assert errors.flatten_errors == {"id_1": "id cannot be None or negative"}
