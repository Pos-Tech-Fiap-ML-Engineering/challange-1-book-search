from typing import cast
from unittest.mock import Mock

from pytest_mock import MockerFixture

from src.application.use_cases.book.scrape_books.ScrapeBooksUseCaseOutputHandler import (
    ScrapeBooksUseCaseOutputHandler,
)
from tests.assets.utils.pytest.StrictMock import StrictMock


class ScrapeBooksUseCaseOutputHandlerMock:
    @staticmethod
    def create(mocker: MockerFixture) -> Mock:
        return cast(
            Mock, StrictMock.make_strict_mock(ScrapeBooksUseCaseOutputHandler, mocker=mocker)
        )
