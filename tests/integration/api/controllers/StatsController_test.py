from typing import Iterator

import pytest
from httpx import AsyncClient

from src.AppBuilder import AppBuilder
from src.api.schemas.output.BookStatsOutput import BookStatsOutput
from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository


class TestStatsController:
    _http_client: AsyncClient
    _scrape_book_repository: ScrapeBookRepository

    @pytest.fixture(autouse=True)
    def setup_teardown(self, http_client: AsyncClient, app_builder: AppBuilder) -> Iterator[None]:
        self._http_client = http_client
        self._scrape_book_repository = app_builder.scrape_book_repository

        yield

    async def test_get_book_stats_overview_successfully(self) -> None:
        # arrange
        books = await self._scrape_book_repository.get_all_books_async()

        book_stats = books.get_stats_books()

        expected_result = BookStatsOutput.to_output_json(book_stats)

        # act
        result = await self._http_client.get("/api/v1/stats/overview")

        # assert
        assert result.status_code == 200
        assert result.json() == expected_result

    async def test_list_book_stats_by_categories_successfully(self) -> None:
        # arrange
        books = await self._scrape_book_repository.get_all_books_async()

        book_stats = books.get_stats_books_by_category()

        expected_result = {k: BookStatsOutput.to_output_json(v) for k, v in book_stats.items()}

        # act
        result = await self._http_client.get("/api/v1/stats/categories")

        # assert
        assert result.status_code == 200
        assert result.json() == expected_result