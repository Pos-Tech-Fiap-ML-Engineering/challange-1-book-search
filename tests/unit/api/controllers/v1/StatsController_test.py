import json

from typing import cast, Any
from collections.abc import Iterator
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from src.api.controllers.v1.StatsController import StatsController
from src.api.presenters.GetBookStatsUseCaseOutputPresenterImpl import (
    GetBookStatsUseCaseOutputPresenterImpl,
)
from src.api.presenters.ListStatsBooksByCategoriesUseCaseOutputPresenterImpl import (
    ListStatsBooksByCategoriesUseCaseOutputPresenterImpl,
)
from src.api.schemas.output.BookStatsOutput import BookStatsOutput
from src.application.use_cases.book.get_book_stats.GetBookStatsUseCaseInput import (
    GetBookStatsUseCaseInput,
)
from src.application.use_cases.category.list_stats_books_by_categories.ListStatsBooksByCategoriesUseCaseInput import (
    ListStatsBooksByCategoriesUseCaseInput,
)
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker
from tests.assets.mocks.UseCaseManagerMock import UseCaseManagerMock


class TestStatsController:
    _use_case_manager_mock: Mock
    _controller: StatsController

    @pytest.fixture(autouse=True)
    def setup_teardown(self, mocker: MockerFixture) -> Iterator[None]:
        self._use_case_manager_mock = UseCaseManagerMock.create(mocker)
        self._controller = StatsController(self._use_case_manager_mock)

        yield

    async def test_book_stats_successfully(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        book_stats = books.get_stats_books()

        expected_result = BookStatsOutput.to_output_json(book_stats)

        def a(*args: tuple[Any], **kwargs: dict[str, Any]) -> None:
            cast(GetBookStatsUseCaseOutputPresenterImpl, cast(object, args[1])).success(book_stats)

        self._use_case_manager_mock.execute_async.side_effect = a

        # act
        result = await self._controller.get_book_stats_async()

        router = self._controller.get_router()

        # assert
        assert result.status_code == 200
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == expected_result
        assert router.prefix == "/stats"

        assert self._use_case_manager_mock.execute_async.call_count == 1
        called_args, called_kwargs = self._use_case_manager_mock.execute_async.call_args_list[0]
        assert isinstance(called_args[0], GetBookStatsUseCaseInput)
        assert isinstance(called_args[1], GetBookStatsUseCaseOutputPresenterImpl)
        assert called_kwargs == {"meta_information": None}

    async def test_list_book_stats_by_categories_successfully(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        book_stats = books.get_stats_books_by_category()

        expected_result = {k: BookStatsOutput.to_output_json(v) for k, v in book_stats.items()}

        def a(*args: tuple[Any], **kwargs: dict[str, Any]) -> None:
            cast(
                ListStatsBooksByCategoriesUseCaseOutputPresenterImpl, cast(object, args[1])
            ).success(book_stats)

        self._use_case_manager_mock.execute_async.side_effect = a

        # act
        result = await self._controller.list_book_stats_by_categories_async()

        router = self._controller.get_router()

        # assert
        assert result.status_code == 200
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == expected_result
        assert router.prefix == "/stats"

        assert self._use_case_manager_mock.execute_async.call_count == 1
        called_args, called_kwargs = self._use_case_manager_mock.execute_async.call_args_list[0]
        assert isinstance(called_args[0], ListStatsBooksByCategoriesUseCaseInput)
        assert isinstance(called_args[1], ListStatsBooksByCategoriesUseCaseOutputPresenterImpl)
        assert called_kwargs == {"meta_information": None}
