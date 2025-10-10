from collections.abc import Iterator
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from src.application.use_cases.book.list_top_rated_books.ListTopRatedBooksUseCaseImpl import (
    ListTopRatedBooksUseCaseImpl,
)
from src.application.use_cases.book.list_top_rated_books.ListTopRatedBooksUseCaseInput import (
    ListTopRatedBooksUseCaseInput,
)
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from src.domain.scrape_book.vos.Rating import Rating
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker
from tests.assets.mocks.ListTopRatedBooksUseCaseOutputHandlerMock import (
    ListTopRatedBooksUseCaseOutputHandlerMock,
)
from tests.assets.mocks.ScrapeBookRepositoryMock import ScrapeBookRepositoryMock


class TestListTopRatedBooksUseCaseImpl:
    _scrape_book_repository_mock: Mock
    _use_case_input: ListTopRatedBooksUseCaseInput
    _use_case_output_mock: Mock
    _use_case: ListTopRatedBooksUseCaseImpl

    @pytest.fixture(autouse=True)
    def setup_teardown(
        self,
        mocker: MockerFixture,
    ) -> Iterator[None]:
        self._scrape_book_repository_mock = ScrapeBookRepositoryMock.create(mocker)
        self._use_case_input = ListTopRatedBooksUseCaseInput()
        self._use_case_output_mock = ListTopRatedBooksUseCaseOutputHandlerMock.create(mocker)
        self._use_case = ListTopRatedBooksUseCaseImpl(
            scrape_book_repository=self._scrape_book_repository_mock
        )

        yield

    async def test_execute_use_case_successfully(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake(rating=Rating(5)))
        books.append(ScrapeBookFaker.fake(rating=Rating(4)))
        books.append(ScrapeBookFaker.fake(rating=Rating(3)))
        books.append(ScrapeBookFaker.fake(rating=Rating(2)))
        books.append(ScrapeBookFaker.fake(rating=Rating(1)))

        self._scrape_book_repository_mock.get_all_books_async.side_effect = (
            lambda *args, **kwargs: books
        )
        self._use_case_output_mock.success.side_effect = None

        # act
        await self._use_case.execute_async(self._use_case_input, self._use_case_output_mock)

        # assert
        self._scrape_book_repository_mock.get_all_books_async.assert_called_once()
        self._use_case_output_mock.success.assert_called_once_with(books.list_top_rated_books())
