from typing import Iterator, cast

import pytest
from httpx import AsyncClient

from src.AppBuilder import AppBuilder
from src.api.schemas.output.BookOutput import BookOutput
from src.domain.scrape_book.ScrapeBook import ScrapeBook
from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository


class TestBooksController:
    _http_client: AsyncClient
    _scrape_book_repository: ScrapeBookRepository

    @pytest.fixture(autouse=True)
    def setup_teardown(self, http_client: AsyncClient, app_builder: AppBuilder) -> Iterator[None]:
        self._http_client = http_client
        self._scrape_book_repository = app_builder.scrape_book_repository

        yield

    async def test_list_all_books_successfully(self) -> None:
        # arrange
        books = await self._scrape_book_repository.get_all_books_async()

        expected_result = BookOutput.to_output_list_json(books)

        # act
        result = await self._http_client.get("/api/v1/books")

        # assert
        assert result.status_code == 200
        assert result.json() == expected_result

    @pytest.mark.parametrize(
        "book_id",
        [
            1, 4,
        ]
    )
    async def test_get_book_by_id_successfully(self, book_id: int) -> None:
        # arrange
        books = await self._scrape_book_repository.get_all_books_async()
        expected_result = BookOutput.to_output_json(cast(ScrapeBook, books.get_by_id(book_id)))

        # act
        result = await self._http_client.get(f"/api/v1/books/{book_id}")

        # assert
        assert result.status_code == 200
        assert result.json() == expected_result

    async def test_get_book_by_id_not_found(self) -> None:
        # arrange - act
        result = await self._http_client.get(f"/api/v1/books/{5000}")

        # assert
        assert result.status_code == 404
        assert result.json() == {}

    async def test_get_book_by_id_invalid_input_bad_request(self) -> None:
        # arrange - act
        result = await self._http_client.get(f"/api/v1/books/{-5000}")

        # assert
        assert result.status_code == 400
        assert result.json() == {'detail': 'Invalid input', 'errors': {'id_1': 'id cannot be None or negative'}}

    async def test_list_books_by_title_and_category_successfully(self) -> None:
        # arrange
        books = await self._scrape_book_repository.get_all_books_async()

        expected_result = BookOutput.to_output_list_json([books[0]])

        # act
        result = await self._http_client.get(
            f"/api/v1/books/search?title={books[0].title}&category={books[0].category}")

        # assert
        assert result.status_code == 200
        assert result.json() == expected_result

    async def test_list_books_by_title_and_category_without_query_params_successfully(self) -> None:
        # arrange
        books = await self._scrape_book_repository.get_all_books_async()

        expected_result = BookOutput.to_output_list_json(books)

        # act
        result = await self._http_client.get(
            f"/api/v1/books/search")

        # assert
        assert result.status_code == 200
        assert result.json() == expected_result

    async def test_list_books_by_title_and_category_with_title_successfully(self) -> None:
        # arrange
        books = await self._scrape_book_repository.get_all_books_async()

        expected_result = BookOutput.to_output_list_json([books[1]])

        # act
        result = await self._http_client.get(
            f"/api/v1/books/search?title={books[1].title}")

        # assert
        assert result.status_code == 200
        assert result.json() == expected_result

    async def test_list_books_by_title_and_category_with_category_successfully(self) -> None:
        # arrange
        books = await self._scrape_book_repository.get_all_books_async()

        filtered_books_by_category: list[ScrapeBook] = list(
            filter(lambda book: book.category == books[0].category, books))

        expected_result = BookOutput.to_output_list_json(filtered_books_by_category)

        # act
        result = await self._http_client.get(
            f"/api/v1/books/search?category={books[0].category}")

        # assert
        assert result.status_code == 200
        assert result.json() == expected_result


    async def test_list_books_by_title_and_category_empty_return_when_mismatch_title_and_category_successfully(self) -> None:
        # arrange
        books = await self._scrape_book_repository.get_all_books_async()

        # act
        result = await self._http_client.get(
            f"/api/v1/books/search?title={books[-1].title}?category={books[0].category}")

        # assert
        assert result.status_code == 200
        assert result.json() == []


    async def test_list_to_rated_books_successfully(self) -> None:
        # arrange
        books = await self._scrape_book_repository.get_all_books_async()

        expected_result = BookOutput.to_output_list_json(books.list_top_rated_books())

        # act
        result = await self._http_client.get(
            f"/api/v1/books/top-rated")

        # assert
        assert result.status_code == 200
        assert result.json() == expected_result
