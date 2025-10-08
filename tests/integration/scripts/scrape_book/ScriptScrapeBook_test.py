import csv
from pathlib import Path
from typing import Any
from collections.abc import Iterator, Coroutine, Callable

import pytest
import respx
from _pytest.monkeypatch import MonkeyPatch

from src.AppBuilder import AppBuilder
from src.domain.scrape_book.vos.Money import Money
from src.infrastructure.utils.RootDir import RootDir
from tests.assets.utils.scraper_book.ScraperBookUtilsMock import ScraperBookUtilsMock


class TestScriptScrapeBook:
    _PATH_BOOKS: Path = Path(__file__).parent.resolve() / "book.csv"
    _PATH_BOOKS_EXPECTED: Path = (
        RootDir.find_root_by_file_name(filename="conftest.py", file=__file__)
        / "data"
        / "integration-test-book.csv"
    )

    _script_scrape_books: Callable[[], Coroutine[Any, Any, None]]

    def clean_to_test(self) -> None:
        if self._PATH_BOOKS.exists():
            self._PATH_BOOKS.unlink(missing_ok=True)

    @pytest.fixture(autouse=True)
    def setup_teardown(self, app_builder: AppBuilder, monkeypatch: MonkeyPatch) -> Iterator[None]:
        self.clean_to_test()

        monkeypatch.setattr(app_builder.scrape_book_repository, "_root_dir", self._PATH_BOOKS)

        self._script_scrape_books = app_builder.script_scrape_books

        yield

        self.clean_to_test()

    async def test_script_scrape_successfully(self, http_request_mock: respx.MockRouter) -> None:
        # arrange
        ScraperBookUtilsMock.mock_http_books_to_scrape_valid(http_request_mock)

        # act
        await self._script_scrape_books()

        # assert
        books = self._load_books_from_csv(self._PATH_BOOKS)
        books_expected = self._load_books_from_csv(self._PATH_BOOKS_EXPECTED)

        assert len(books) == len(books_expected)
        for i in range(len(books)):
            actual = books[i]
            expected = books_expected[i]
            assert actual == expected

    async def test_raise_exception_when_failed_to_load_site(
        self, http_request_mock: respx.MockRouter
    ) -> None:
        # arrange
        ScraperBookUtilsMock.mock_http_failed_load_site(http_request_mock)

        # act - assert
        with pytest.raises(Exception) as excInfo:
            await self._script_scrape_books()

        assert str(excInfo.value) == "Failed to load site"

    async def test_raise_exception_when_failed_to_load_link(
        self, http_request_mock: respx.MockRouter
    ) -> None:
        # arrange
        ScraperBookUtilsMock.mock_http_failed_to_load_link(http_request_mock)

        # act - assert
        with pytest.raises(Exception) as excInfo:
            await self._script_scrape_books()

        assert (
            str(excInfo.value)
            == "Failed to load link: https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
        )

    @staticmethod
    def _load_books_from_csv(path: Path) -> list[dict[str, str]]:
        books: list[dict[str, Any]] = []
        with path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                books.append(
                    {
                        "id": row["id"],
                        "category": row["category"],
                        "title": row["title"],
                        "rating": str(int(row["rating"])),
                        "product_description": row["product_description"],
                        "upc": row["upc"],
                        "product_type": row["product_type"],
                        "price_full": str(Money.from_string(row["price_full"]).amount),
                        "price_excl_tax": str(Money.from_string(row["price_excl_tax"]).amount),
                        "tax": str(Money.from_string(row["tax"]).amount),
                        "availability": str(int(row["availability"])),
                        "number_reviews": str(int(row["number_reviews"])),
                        "image_url": row["image_url"],
                        "product_page_url": row["product_page_url"],
                    }
                )

        return books
