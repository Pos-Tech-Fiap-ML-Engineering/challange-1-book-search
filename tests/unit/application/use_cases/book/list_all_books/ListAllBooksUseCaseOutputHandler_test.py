import pytest

from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler
from src.application.use_cases.book.list_all_books.ListAllBooksUseCaseOutputHandler import \
    ListAllBooksUseCaseOutputHandler


class TestListAllBooksUseCaseOutputHandler:
    def test_class_is_subclass_useCase_output_handler(self) -> None:
        # arrange - act - assert
        assert issubclass(ListAllBooksUseCaseOutputHandler, UseCaseOutputHandler)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            ListAllBooksUseCaseOutputHandler()  # type: ignore
