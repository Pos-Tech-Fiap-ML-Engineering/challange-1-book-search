from typing import cast
from unittest.mock import Mock
from pytest_mock import MockerFixture

from src.application.use_cases.category.list_stats_books_by_categories.ListStatsBooksByCategoriesUseCaseOutputHandler import \
    ListStatsBooksByCategoriesUseCaseOutputHandler
from tests.assets.utils.pytest.StrictMock import StrictMock


class ListStatsBooksByCategoriesUseCaseOutputHandlerMock:
    @staticmethod
    def create(mocker: MockerFixture) -> Mock:
        return cast(Mock, StrictMock.make_strict_mock(ListStatsBooksByCategoriesUseCaseOutputHandler, mocker=mocker))
