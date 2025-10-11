from collections.abc import Iterator
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from src.application.use_cases.book.get_book_by_id.GetBookByIdUseCaseImpl import (
    GetBookByIdUseCaseImpl,
)
from src.application.use_cases.book.get_book_by_id.GetBookByIdUseCaseInput import (
    GetBookByIdUseCaseInput,
)
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker
from tests.assets.mocks.AppLoggerMock import AppLoggerMock
from tests.assets.mocks.GetBookByIdUseCaseOutputHandlerMock import (
    GetBookByIdUseCaseOutputHandlerMock,
)
from tests.assets.mocks.ScrapeBookRepositoryMock import ScrapeBookRepositoryMock


class TestGetBookByIdUseCaseImpl:
    _BOOK_ID: int = 10
    _scrape_book_repository_mock: Mock
    _logger_mock: Mock
    _use_case_input: GetBookByIdUseCaseInput
    _use_case_output_mock: Mock
    _use_case: GetBookByIdUseCaseImpl

    @pytest.fixture(autouse=True)
    def setup_teardown(
            self,
            mocker: MockerFixture,
    ) -> Iterator[None]:
        self._scrape_book_repository_mock = ScrapeBookRepositoryMock.create(mocker)
        self._logger_mock = AppLoggerMock.create(mocker)
        self._use_case_input = GetBookByIdUseCaseInput(self._BOOK_ID)
        self._use_case_output_mock = GetBookByIdUseCaseOutputHandlerMock.create(mocker)
        self._use_case = GetBookByIdUseCaseImpl(
            scrape_book_repository=self._scrape_book_repository_mock,
            logger=self._logger_mock
        )

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

        self._scrape_book_repository_mock.get_all_books_async.side_effect = (
            lambda *args, **kwargs: books
        )
        self._use_case_output_mock.success.side_effect = None

        self._logger_mock.info.side_effect = None

        # act
        await self._use_case.execute_async(self._use_case_input, self._use_case_output_mock)

        # assert
        self._scrape_book_repository_mock.get_all_books_async.assert_called_once()
        self._use_case_output_mock.success.assert_called_once_with(books[0])
        called_args, called_kwargs = self._logger_mock.info.call_args_list
        assert(len(called_args) == 2)
        assert(len(called_kwargs) == 2)
        assert called_args[0][0] == f'Recovery Book id: {str(books[0].id)}'
        assert called_args[1] == {}
        assert called_kwargs[0][0] == 'Book Info in log attributes'
        assert called_kwargs[0][1] == {
                "id": str(books[0].id),
                "category": str(books[0].category),
                "title": str(books[0].title),
                "price_full": str(books[0].price_full),
            }
        assert called_kwargs[1] == {}

    async def test_execute_async_and_return_not_found(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake(model_id=self._BOOK_ID + 2300))

        self._scrape_book_repository_mock.get_all_books_async.side_effect = (
            lambda *args, **kwargs: books
        )
        self._use_case_output_mock.not_found.side_effect = None

        self._logger_mock.info.side_effect = None

        # act
        await self._use_case.execute_async(self._use_case_input, self._use_case_output_mock)

        # assert
        self._scrape_book_repository_mock.get_all_books_async.assert_called_once()
        self._use_case_output_mock.not_found.assert_called_once()
        called_args = self._logger_mock.info.call_args_list
        assert (len(called_args) == 1)
        assert called_args[0][0][0] == 'Recovery Book id: None'
        assert called_args[0][1] == {}
