import pytest

from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler
from src.application.use_cases.book.list_books_by_price_range.ListBooksByPriceRangeUseCaseOutputHandler import (
    ListBooksByPriceRangeUseCaseOutputHandler,
)


class TestListBooksByPriceRangeUseCaseOutputHandler:
    def test_class_is_subclass_useCase_output_handler(self) -> None:
        # arrange - act - assert
        assert issubclass(ListBooksByPriceRangeUseCaseOutputHandler, UseCaseOutputHandler)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            ListBooksByPriceRangeUseCaseOutputHandler()  # type: ignore
