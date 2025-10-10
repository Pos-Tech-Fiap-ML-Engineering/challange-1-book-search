from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.application.use_cases.book.list_books_by_title_category.ListBooksByCategoryTitleUseCaseInput import \
    ListBooksByCategoryTitleUseCaseInput


class TestListBooksByCategoryTitleUseCaseInput:
    def test_class_is_subclass_input(self) -> None:
        # arrange - act - assert
        assert issubclass(ListBooksByCategoryTitleUseCaseInput, UseCaseInput)

    def test_class_initialized_successfully(self) -> None:
        # arrange - act - assert
        result = ListBooksByCategoryTitleUseCaseInput(title="TITLE", category="CATEGORY")
        assert result.title == "TITLE"
        assert result.category == "CATEGORY"
