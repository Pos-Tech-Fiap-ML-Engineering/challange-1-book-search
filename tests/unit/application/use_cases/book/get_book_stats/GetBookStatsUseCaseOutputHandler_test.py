import pytest

from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler
from src.application.use_cases.book.get_book_stats.GetBookStatsUseCaseOutputHandler import \
    GetBookStatsUseCaseOutputHandler


class TestGetBookStatsUseCaseOutputHandler:
    def test_class_is_subclass_useCase_output_handler(self) -> None:
        # arrange - act - assert
        assert issubclass(GetBookStatsUseCaseOutputHandler, UseCaseOutputHandler)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            GetBookStatsUseCaseOutputHandler()  # type: ignore