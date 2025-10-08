from collections.abc import Iterator
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from src.application.boundaries.use_case.UseCase import UseCase
from src.application.use_cases.book.scrape_books.ScrapeBooksUseCaseImpl import (
    ScrapeBooksUseCaseImpl,
)
from src.application.use_cases.book.scrape_books.ScrapeBooksUseCaseInput import (
    ScrapeBooksUseCaseInput,
)
from tests.assets.mocks.HttpClientFactoryMock import HttpClientFactoryMock
from tests.assets.mocks.ScrapeBookRepositoryMock import ScrapeBookRepositoryMock
from tests.assets.mocks.ScrapeBooksUseCaseOutputHandlerMock import (
    ScrapeBooksUseCaseOutputHandlerMock,
)
from tests.assets.utils.pytest.StrictMock import StrictMock
from tests.assets.utils.scraper_book.ScraperBookUtilsMock import ScraperBookUtilsMock


class TestScrapeBooksUseCaseImpl:
    _USER_AGENT_DEFAULT_VALUE: str = "UA/1"
    _BASE_URL: str = "https://books.toscrape.com"

    _http_client_mock: Mock

    _scrape_book_repository_mock: Mock
    _use_case_output_mock: Mock
    _use_case: UseCase

    @pytest.fixture(autouse=True)
    def patch_user_agent(self, mocker: MockerFixture) -> Iterator[None]:
        class _UA:
            random = self._USER_AGENT_DEFAULT_VALUE

        p = mocker.patch(
            "src.application.use_cases.book.scrape_books.ScrapeBooksUseCaseImpl.UserAgent",
            return_value=_UA(),
        )
        yield
        p.stop()

    @pytest.fixture(autouse=True)
    def setup_teardown(
        self,
        request: pytest.FixtureRequest,
        mocker: MockerFixture,
        patch_user_agent: Iterator[None],
    ) -> Iterator[None]:
        self._http_client_mock = StrictMock.make_async_strict_mock()

        http_client_factory_mock = HttpClientFactoryMock.create(mocker)
        http_client_factory_mock.create_async_factory.side_effect = None
        http_client_factory_mock.create_async_factory.return_value = self._http_client_mock

        self._scrape_book_repository_mock = ScrapeBookRepositoryMock.create(mocker)
        self._use_case_output_mock = ScrapeBooksUseCaseOutputHandlerMock.create(mocker)

        self._use_case = ScrapeBooksUseCaseImpl(
            http_client_factory_mock, self._scrape_book_repository_mock
        )

        yield

    async def test_scrape_output_handler_failed_to_load_site(
        self,
        mocker: MockerFixture,
    ) -> None:
        # arrange
        _use_case_input = ScrapeBooksUseCaseInput()

        self._http_client_mock.get = mocker.AsyncMock(
            side_effect=ScraperBookUtilsMock.invalid_books
        )
        self._use_case_output_mock.failed_to_load_site.side_effect = None

        # act
        await self._use_case.execute_async(_use_case_input, self._use_case_output_mock)

        # assert
        assert self._http_client_mock.get.call_count == 1
        called_args, called_kwargs = self._http_client_mock.get.call_args
        assert called_args[0] == self._BASE_URL
        assert called_kwargs == {"headers": {"User-Agent": self._USER_AGENT_DEFAULT_VALUE}}

        self._use_case_output_mock.failed_to_load_site.assert_called_once()

    async def test_scrape_output_handler_failed_to_load_link(
        self,
        mocker: MockerFixture,
    ) -> None:
        # arrange
        _use_case_input = ScrapeBooksUseCaseInput()

        self._http_client_mock.get = mocker.AsyncMock(
            side_effect=ScraperBookUtilsMock.invalid_link_book
        )
        self._use_case_output_mock.failed_to_load_link.side_effect = None

        # act
        await self._use_case.execute_async(_use_case_input, self._use_case_output_mock)

        # assert
        assert self._http_client_mock.get.call_count == 2
        called_args, called_kwargs = self._http_client_mock.get.call_args_list[0]
        assert called_args[0] == self._BASE_URL
        assert called_kwargs == {"headers": {"User-Agent": self._USER_AGENT_DEFAULT_VALUE}}

        self._use_case_output_mock.failed_to_load_link.assert_called_once()

    async def test_scrape_successfully(self, mocker: MockerFixture) -> None:
        _use_case_input = ScrapeBooksUseCaseInput()

        self._http_client_mock.get = mocker.AsyncMock(
            side_effect=ScraperBookUtilsMock.get_valid_books
        )
        self._use_case_output_mock.success.side_effect = None
        self._scrape_book_repository_mock.save_books_async.side_effect = None

        # act
        await self._use_case.execute_async(_use_case_input, self._use_case_output_mock)

        # assert
        self._use_case_output_mock.success.assert_called_once()

        assert self._scrape_book_repository_mock.save_books_async.call_count == 1
        called_args, called_kwargs = (
            self._scrape_book_repository_mock.save_books_async.call_args_list[0]
        )

        inserted_books = called_args[0]
        expected_books = ScraperBookUtilsMock.scraped_books()

        assert len(inserted_books) == len(expected_books)
        for i in range(len(inserted_books)):
            assert_book = inserted_books[i].to_dict()
            expected_book = expected_books[i].to_dict()
            assert assert_book == expected_book
