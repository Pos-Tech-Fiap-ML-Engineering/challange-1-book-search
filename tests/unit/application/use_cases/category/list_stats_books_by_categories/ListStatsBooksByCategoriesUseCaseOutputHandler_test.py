import pytest

from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler
from src.application.use_cases.category.list_stats_books_by_categories.ListStatsBooksByCategoriesUseCaseOutputHandler import (
    ListStatsBooksByCategoriesUseCaseOutputHandler,
)


class TestListStatsBooksByCategoriesUseCaseOutputHandler:
    def test_class_is_subclass_useCase_output_handler(self) -> None:
        # arrange - act - assert
        assert issubclass(ListStatsBooksByCategoriesUseCaseOutputHandler, UseCaseOutputHandler)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            ListStatsBooksByCategoriesUseCaseOutputHandler()  # type: ignore
