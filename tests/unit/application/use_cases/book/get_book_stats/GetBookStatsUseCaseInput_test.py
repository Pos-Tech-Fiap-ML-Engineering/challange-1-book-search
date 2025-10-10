from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.application.use_cases.book.get_book_stats.GetBookStatsUseCaseInput import GetBookStatsUseCaseInput


class TestGetBookStatsUseCaseInput:
    def test_class_is_subclass_input(self) -> None:
        # arrange - act - assert
        assert issubclass(GetBookStatsUseCaseInput, UseCaseInput)

    def test_class_initialized_successfully(self) -> None:
        # arrange - act - assert
        GetBookStatsUseCaseInput()