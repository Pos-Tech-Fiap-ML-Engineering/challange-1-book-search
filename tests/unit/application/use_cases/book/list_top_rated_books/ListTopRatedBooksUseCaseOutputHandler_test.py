import pytest

from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler
from src.application.use_cases.book.list_top_rated_books.ListTopRatedBooksUseCaseOutputHandler import (
    ListTopRatedBooksUseCaseOutputHandler,
)


class TestListTopRatedBooksUseCaseOutputHandler:
    def test_class_is_subclass_useCase_output_handler(self) -> None:
        # arrange - act - assert
        assert issubclass(ListTopRatedBooksUseCaseOutputHandler, UseCaseOutputHandler)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            ListTopRatedBooksUseCaseOutputHandler()  # type: ignore
