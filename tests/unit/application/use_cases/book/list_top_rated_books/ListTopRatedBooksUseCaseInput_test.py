from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.application.use_cases.book.list_top_rated_books.ListTopRatedBooksUseCaseInput import \
    ListTopRatedBooksUseCaseInput


class TestListTopRatedBooksUseCaseInput:
    def test_class_is_subclass_input(self) -> None:
        # arrange - act - assert
        assert issubclass(ListTopRatedBooksUseCaseInput, UseCaseInput)

    def test_class_initialized_successfully(self) -> None:
        # arrange - act - assert
        ListTopRatedBooksUseCaseInput()