import pytest

from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler
from src.application.use_cases.book.scrape_books.ScrapeBooksUseCaseOutputHandler import (
    ScrapeBooksUseCaseOutputHandler,
)


class TestScrapeBooksUseCaseOutputHandler:
    def test_class_is_subclass_useCase_output_handler(self) -> None:
        # arrange - act - assert
        assert issubclass(ScrapeBooksUseCaseOutputHandler, UseCaseOutputHandler)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            ScrapeBooksUseCaseOutputHandler()  # type: ignore
