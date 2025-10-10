import pytest

from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler
from src.application.use_cases.book.list_books_by_title_category.ListBooksByCategoryTitleUseCaseOutputHandler import \
    ListBooksByCategoryTitleUseCaseOutputHandler


class TestListBooksByCategoryTitleUseCaseOutputHandler:
    def test_class_is_subclass_useCase_output_handler(self) -> None:
        # arrange - act - assert
        assert issubclass(ListBooksByCategoryTitleUseCaseOutputHandler, UseCaseOutputHandler)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            ListBooksByCategoryTitleUseCaseOutputHandler()  # type: ignore