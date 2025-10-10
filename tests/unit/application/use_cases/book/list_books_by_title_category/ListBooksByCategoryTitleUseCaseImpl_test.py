from typing import Iterator
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from src.application.use_cases.book.list_books_by_title_category.ListBooksByCategoryTitleUseCaseImpl import \
    ListBooksByCategoryTitleUseCaseImpl
from src.application.use_cases.book.list_books_by_title_category.ListBooksByCategoryTitleUseCaseInput import \
    ListBooksByCategoryTitleUseCaseInput
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker
from tests.assets.mocks.ListBooksByCategoryTitleUseCaseOutputHandlerMock import \
    ListBooksByCategoryTitleUseCaseOutputHandlerMock
from tests.assets.mocks.ScrapeBookRepositoryMock import ScrapeBookRepositoryMock


class TestListBooksByCategoryTitleUseCaseImpl:
    _scrape_book_repository_mock: Mock
    _use_case_input: ListBooksByCategoryTitleUseCaseInput
    _use_case_output_mock: Mock
    _use_case: ListBooksByCategoryTitleUseCaseImpl

    @pytest.fixture(autouse=True)
    def setup_teardown(
            self,
            mocker: MockerFixture,
    ) -> Iterator[None]:
        self._scrape_book_repository_mock = ScrapeBookRepositoryMock.create(mocker)
        self._use_case_input = ListBooksByCategoryTitleUseCaseInput('Title 01', 'Category 01')
        self._use_case_output_mock = ListBooksByCategoryTitleUseCaseOutputHandlerMock.create(mocker)
        self._use_case = ListBooksByCategoryTitleUseCaseImpl(scrape_book_repository=self._scrape_book_repository_mock)

        yield

    async def test_execute_use_case_successfully(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake(title=self._use_case_input.title, category=self._use_case_input.category))

        self._scrape_book_repository_mock.get_all_books_async.side_effect = lambda *args, **kwargs: books
        self._use_case_output_mock.success.side_effect = None

        # act
        await self._use_case.execute_async(self._use_case_input, self._use_case_output_mock)

        # assert
        self._scrape_book_repository_mock.get_all_books_async.assert_called_once()
        self._use_case_output_mock.success.assert_called_once_with([books[0]])
