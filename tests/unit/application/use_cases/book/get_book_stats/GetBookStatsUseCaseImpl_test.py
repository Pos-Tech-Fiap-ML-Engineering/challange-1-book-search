from typing import Iterator
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from src.application.boundaries.use_case.UseCase import UseCase
from src.application.use_cases.book.get_book_stats.GetBookStatsUseCaseImpl import GetBookStatsUseCaseImpl
from src.application.use_cases.book.get_book_stats.GetBookStatsUseCaseInput import GetBookStatsUseCaseInput
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker
from tests.assets.mocks.GetBookStatsUseCaseOutputHandlerMock import GetBookStatsUseCaseOutputHandlerMock
from tests.assets.mocks.ScrapeBookRepositoryMock import ScrapeBookRepositoryMock


class TestGetBookStatsUseCaseImpl:
    _scrape_book_repository_mock: Mock
    _use_case_input: GetBookStatsUseCaseInput
    _use_case_output_mock: Mock
    _use_case: UseCase

    @pytest.fixture(autouse=True)
    def setup_teardown(
            self,
            mocker: MockerFixture,
    ) -> Iterator[None]:
        self._scrape_book_repository_mock = ScrapeBookRepositoryMock.create(mocker)
        self._use_case_input = GetBookStatsUseCaseInput()
        self._use_case_output_mock = GetBookStatsUseCaseOutputHandlerMock.create(mocker)
        self._use_case = GetBookStatsUseCaseImpl(scrape_book_repository=self._scrape_book_repository_mock)

        yield

    async def test_execute_async(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        self._scrape_book_repository_mock.get_all_books_async.side_effect = lambda *args, **kwargs: books
        self._use_case_output_mock.success.side_effect = None

        expected_result = books.get_stats_books()

        # act
        await self._use_case.execute_async(self._use_case_input, self._use_case_output_mock)

        # assert
        self._scrape_book_repository_mock.get_all_books_async.assert_called_once()
        self._use_case_output_mock.success.assert_called_once_with(expected_result)