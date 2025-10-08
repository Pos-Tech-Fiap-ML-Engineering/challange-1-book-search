from typing import cast
from unittest.mock import Mock

from pytest_mock import MockerFixture

from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository
from tests.assets.utils.pytest.StrictMock import StrictMock


class ScrapeBookRepositoryMock:
    @staticmethod
    def create(mocker: MockerFixture) -> Mock:
        return cast(Mock, StrictMock.make_strict_mock(ScrapeBookRepository, mocker=mocker))
