from typing import Iterator

import httpx
import pytest

from src.api.schemas.output.BookOutput import BookOutput
from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository


class TestBooksController:
    _http_client: httpx.AsyncClient
    _scrape_book_repository: ScrapeBookRepository

    @pytest.fixture(autouse=True)
    def setup_teardown(self, http_client: httpx.AsyncClient, scrape_book_repository: ScrapeBookRepository) -> Iterator[
        None]:
        self._http_client = http_client
        self._scrape_book_repository = scrape_book_repository
        yield

    async def test_list_all_books_successfully(self) -> None:
        # arrange - act
        result = await self._http_client.get("/api/v1/books")

        books = await self._scrape_book_repository.get_all_books_async()

        expected_result = BookOutput.to_output_list_json(books)

        # assert
        assert result.status_code == 200
        assert result.json() == expected_result
