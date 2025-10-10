from typing import cast
from unittest.mock import Mock

from pytest_mock import MockerFixture

from src.application.use_cases.book.get_book_by_id.GetBookByIdUseCaseOutputHandler import (
    GetBookByIdUseCaseOutputHandler,
)
from src.standard.built_in.Static import Static
from tests.assets.utils.pytest.StrictMock import StrictMock


class GetBookByIdUseCaseOutputHandlerMock(Static):
    @staticmethod
    def create(mocker: MockerFixture) -> Mock:
        return cast(
            Mock, StrictMock.make_strict_mock(GetBookByIdUseCaseOutputHandler, mocker=mocker)
        )
