from collections.abc import Iterator

import pytest
from httpx import AsyncClient

from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository


class TestCategoriesController:
    _http_client: AsyncClient
    _scrape_book_repository: ScrapeBookRepository

    @pytest.fixture(autouse=True)
    def setup_teardown(
        self, http_client: AsyncClient, scrape_book_repository: ScrapeBookRepository
    ) -> Iterator[None]:
        self._http_client = http_client
        self._scrape_book_repository = scrape_book_repository

        yield

    async def test_list_all_categories_successfully(self) -> None:
        # arrange
        books = await self._scrape_book_repository.get_all_books_async()

        expected_result = sorted(list(books.categories))

        # act
        result = await self._http_client.get("/api/v1/categories")

        # assert
        assert result.status_code == 200
        body_result = sorted(result.json())
        assert body_result == expected_result
