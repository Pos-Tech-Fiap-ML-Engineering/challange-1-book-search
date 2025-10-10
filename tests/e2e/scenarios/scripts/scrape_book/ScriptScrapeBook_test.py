import csv
from pathlib import Path
from typing import Any
from collections.abc import Iterator

import pytest

from src.domain.scrape_book.vos.Money import Money
from src.infrastructure.domain.scrape_book.ScrapeBookRepositoryImpl import ScrapeBookRepositoryImpl
from src.infrastructure.utils.RootDir import RootDir
from src.scripts.Main import app_builder, script_scrape_books


class TestScriptScrapeBook:
    _PATH_BOOKS: Path = Path(__file__).parent.resolve() / "book.csv"
    _PATH_EXPECTED_BOOKS: Path = (
        RootDir.find_root_by_file_name(filename="conftest.py", file=__file__)
        / "data"
        / "expected_books.csv"
    )

    @pytest.fixture(autouse=True)
    def setup_teardown(self, request: pytest.FixtureRequest) -> Iterator[None]:

        if self._PATH_BOOKS.exists():
            self._PATH_BOOKS.unlink(missing_ok=True)

        app_builder.override_instances(
            param_scrape_book_repository=ScrapeBookRepositoryImpl(
                Path(__file__).parent.resolve() / "book.csv"
            ),
        )

        yield

        if self._PATH_BOOKS.exists():
            self._PATH_BOOKS.unlink(missing_ok=True)

    async def test_script_scrape_books_successfully(self) -> None:
        # arrange - act
        await script_scrape_books()

        # assert
        def key_by_id(d: dict[str, str]) -> str:
            return d["id"]

        actual_books = sorted(self.load_books_from_csv(self._PATH_EXPECTED_BOOKS), key=key_by_id)
        expected_books = sorted(self.load_books_from_csv(self._PATH_BOOKS), key=key_by_id)

        assert len(actual_books) == len(expected_books)
        for i in range(len(actual_books)):
            actual = actual_books[i]
            expected = expected_books[i]
            assert actual == expected

    @staticmethod
    def load_books_from_csv(path: Path) -> list[dict[str, str]]:
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
