from typing import cast
from unittest.mock import Mock

from pytest_mock import MockerFixture

from src.application.use_cases.book.list_top_rated_books.ListTopRatedBooksUseCaseOutputHandler import \
    ListTopRatedBooksUseCaseOutputHandler
from src.standard.built_in.Static import Static
from tests.assets.utils.pytest.StrictMock import StrictMock


class ListTopRatedBooksUseCaseOutputHandlerMock(Static):
    @staticmethod
    def create(mocker: MockerFixture) -> Mock:
        return cast(Mock, StrictMock.make_strict_mock(ListTopRatedBooksUseCaseOutputHandler, mocker=mocker))