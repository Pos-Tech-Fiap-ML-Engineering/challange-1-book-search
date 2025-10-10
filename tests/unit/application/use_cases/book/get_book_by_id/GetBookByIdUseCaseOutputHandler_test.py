import pytest

from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler
from src.application.use_cases.book.get_book_by_id.GetBookByIdUseCaseOutputHandler import (
    GetBookByIdUseCaseOutputHandler,
)


class TestGetBookByIdUseCaseOutputHandler:
    def test_class_is_subclass_useCase_output_handler(self) -> None:
        # arrange - act - assert
        assert issubclass(GetBookByIdUseCaseOutputHandler, UseCaseOutputHandler)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            GetBookByIdUseCaseOutputHandler()  # type: ignore
