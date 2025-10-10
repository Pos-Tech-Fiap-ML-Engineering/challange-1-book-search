from typing import cast
from unittest.mock import Mock

from pytest_mock import MockerFixture

from src.application.use_cases.category.list_categories.ListCategoriesUseCaseOutputHandler import \
    ListCategoriesUseCaseOutputHandler
from tests.assets.utils.pytest.StrictMock import StrictMock


class ListCategoriesUseCaseOutputHandlerMock:
    @staticmethod
    def create(mocker: MockerFixture) -> Mock:
        return cast(Mock, StrictMock.make_strict_mock(ListCategoriesUseCaseOutputHandler, mocker=mocker))