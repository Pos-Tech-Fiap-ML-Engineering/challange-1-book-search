from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.application.use_cases.book.scrape_books.ScrapeBooksUseCaseInput import (
    ScrapeBooksUseCaseInput,
)


class TestScrapeBooksUseCaseInput:
    def test_class_is_subclass_input(self) -> None:
        # arrange - act - assert
        assert issubclass(ScrapeBooksUseCaseInput, UseCaseInput)

    def test_class_initialized_successfully(self) -> None:
        # arrange - act - assert
        ScrapeBooksUseCaseInput()
