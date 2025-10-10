from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.application.use_cases.category.list_stats_books_by_categories.ListStatsBooksByCategoriesUseCaseInput import (
    ListStatsBooksByCategoriesUseCaseInput,
)


class TestListStatsBooksByCategoriesUseCaseInput:
    def test_class_is_subclass_input(self) -> None:
        # arrange - act - assert
        assert issubclass(ListStatsBooksByCategoriesUseCaseInput, UseCaseInput)

    def test_class_initialized_successfully(self) -> None:
        # arrange - act - assert
        ListStatsBooksByCategoriesUseCaseInput()
