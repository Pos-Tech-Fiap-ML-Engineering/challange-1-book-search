from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.application.use_cases.book.list_all_books.ListAllBooksUseCaseInput import ListAllBooksUseCaseInput


class TestListAllBooksUseCaseInput:
    def test_class_is_subclass_input(self) -> None:
        # arrange - act - assert
        assert issubclass(ListAllBooksUseCaseInput, UseCaseInput)

    def test_class_initialized_successfully(self) -> None:
        # arrange - act - assert
        ListAllBooksUseCaseInput()