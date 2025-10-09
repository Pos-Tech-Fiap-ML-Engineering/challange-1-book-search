from typing import Iterator
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from src.application.use_cases.book.get_book_by_id.GetBookByIdUseCaseImpl import GetBookByIdUseCaseImpl
from src.application.use_cases.book.get_book_by_id.GetBookByIdUseCaseInput import GetBookByIdUseCaseInput
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker
from tests.assets.mocks.GetBookByIdUseCaseOutputHandlerMock import GetBookByIdUseCaseOutputHandlerMock
from tests.assets.mocks.ScrapeBookRepositoryMock import ScrapeBookRepositoryMock


class TestGetBookByIdUseCaseImpl:
    _BOOK_ID: int = 10
    _scrape_book_repository_mock: Mock
    _use_case_input: GetBookByIdUseCaseInput
    _use_case_output_mock: Mock
    _use_case: GetBookByIdUseCaseImpl

    @pytest.fixture(autouse=True)
    def setup_teardown(
            self,
            mocker: MockerFixture,
    ) -> Iterator[None]:
        self._scrape_book_repository_mock = ScrapeBookRepositoryMock.create(mocker)
        self._use_case_input = GetBookByIdUseCaseInput(self._BOOK_ID)
        self._use_case_output_mock = GetBookByIdUseCaseOutputHandlerMock.create(mocker)
        self._use_case = GetBookByIdUseCaseImpl(scrape_book_repository=self._scrape_book_repository_mock)

        yield

    async def test_validate_async_successfully(self) -> None:
        # arrange - act
        errors = await self._use_case.validate_async(self._use_case_input)

        # assert
        assert errors.has_errors is False

    async def test_validate_async_with_error(self) -> None:
        # arrange
        self._use_case_input._id = -10

        # act
        errors = await self._use_case.validate_async(self._use_case_input)

        # assert
        assert errors.has_errors is True

    async def test_execute_async_and_return_success(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake(model_id=self._BOOK_ID))

        self._scrape_book_repository_mock.get_all_books_async.side_effect = lambda *args, **kwargs: books
        self._use_case_output_mock.success.side_effect = None

        # act
        await self._use_case.execute_async(self._use_case_input, self._use_case_output_mock)

        # assert
        self._scrape_book_repository_mock.get_all_books_async.assert_called_once()
        self._use_case_output_mock.success.assert_called_once_with(books[0])

    async def test_execute_async_and_return_not_found(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake(model_id=self._BOOK_ID + 2300))

        self._scrape_book_repository_mock.get_all_books_async.side_effect = lambda *args, **kwargs: books
        self._use_case_output_mock.not_found.side_effect = None

        # act
        await self._use_case.execute_async(self._use_case_input, self._use_case_output_mock)

        # assert
        self._scrape_book_repository_mock.get_all_books_async.assert_called_once()
        self._use_case_output_mock.not_found.assert_called_once()
