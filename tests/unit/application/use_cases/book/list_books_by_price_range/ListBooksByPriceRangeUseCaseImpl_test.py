from decimal import Decimal
from collections.abc import Iterator
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from src.application.use_cases.book.list_books_by_price_range.ListBooksByPriceRangeUseCaseImpl import (
    ListBooksByPriceRangeUseCaseImpl,
)
from src.application.use_cases.book.list_books_by_price_range.ListBooksByPriceRangeUseCaseInput import (
    ListBooksByPriceRangeUseCaseInput,
)
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from src.domain.scrape_book.vos.Money import Money
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker
from tests.assets.mocks.ListBooksByPriceRangeUseCaseOutputHandlerMock import (
    ListBooksByPriceRangeUseCaseOutputHandlerMock,
)
from tests.assets.mocks.ScrapeBookRepositoryMock import ScrapeBookRepositoryMock


class TestListBooksByPriceRangeUseCaseImpl:
    _scrape_book_repository_mock: Mock
    _use_case_input: ListBooksByPriceRangeUseCaseInput
    _use_case_output_mock: Mock
    _use_case: ListBooksByPriceRangeUseCaseImpl

    @pytest.fixture(autouse=True)
    def setup_teardown(
        self,
        mocker: MockerFixture,
    ) -> Iterator[None]:
        self._scrape_book_repository_mock = ScrapeBookRepositoryMock.create(mocker)
        self._use_case_input = ListBooksByPriceRangeUseCaseInput(Decimal(10), Decimal(20))
        self._use_case_output_mock = ListBooksByPriceRangeUseCaseOutputHandlerMock.create(mocker)
        self._use_case = ListBooksByPriceRangeUseCaseImpl(
            scrape_book_repository=self._scrape_book_repository_mock
        )

        yield

    async def test_validate_async_successfully(self) -> None:
        # arrange - act
        errors = await self._use_case.validate_async(self._use_case_input)

        # assert
        assert errors.has_errors is False

    async def test_validate_async_with_error(self) -> None:
        # arrange
        self._use_case_input._min_price = Decimal(-10)

        # act
        errors = await self._use_case.validate_async(self._use_case_input)

        # assert
        assert errors.has_errors is True

    async def test_execute_use_case_successfully(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake(price_full=Money.from_float(10)))
        books.append(ScrapeBookFaker.fake(price_full=Money.from_float(50)))
        books.append(ScrapeBookFaker.fake(price_full=Money.from_float(30)))
        books.append(ScrapeBookFaker.fake(price_full=Money.from_float(40)))
        books.append(ScrapeBookFaker.fake(price_full=Money.from_float(5)))

        self._scrape_book_repository_mock.get_all_books_async.side_effect = (
            lambda *args, **kwargs: books
        )
        self._use_case_output_mock.success.side_effect = None

        # act
        await self._use_case.execute_async(self._use_case_input, self._use_case_output_mock)

        # assert
        self._scrape_book_repository_mock.get_all_books_async.assert_called_once()
        self._use_case_output_mock.success.assert_called_once_with(
            books.list_books_by_price_range(
                self._use_case_input.min_price,
                self._use_case_input.max_price,
            )
        )
