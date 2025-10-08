from __future__ import annotations

import csv
from pathlib import Path
from collections.abc import Iterator

import pytest

import src.infrastructure.domain.scrape_book.ScrapeBookRepositoryImpl as repo_mod
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from src.domain.scrape_book.vos.Upc import Upc
from src.infrastructure.domain.scrape_book.ScrapeBookRepositoryImpl import ScrapeBookRepositoryImpl
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker


class TestScrapeBookRepositoryImpl:
    _repository: ScrapeBookRepositoryImpl

    @pytest.fixture(autouse=True)
    def setup_teardown(self, tmp_path: Path) -> Iterator[None]:
        repo_mod._CACHE = None
        path = tmp_path / "books.csv"

        path.parent.mkdir(parents=True, exist_ok=True)
        self._repository = ScrapeBookRepositoryImpl(root_dir=path)

        yield

        if path.exists():
            path.unlink(missing_ok=True)

    def test_to_row_serialization(self) -> None:
        # arrange
        b = ScrapeBookFaker.fake()

        # act
        row = self._repository._to_row(b)

        # arrange
        expected_keys = {
            "id",
            "category",
            "title",
            "rating",
            "product_description",
            "upc",
            "product_type",
            "price_full",
            "price_excl_tax",
            "tax",
            "availability",
            "number_reviews",
            "image_url",
            "product_page_url",
        }
        assert set(row.keys()) == expected_keys

        assert all(isinstance(v, str) for v in row.values())

        assert row["id"] == str(b.id)
        assert row["category"] == b.category
        assert row["title"] == b.title
        assert row["rating"] == str(b.rating)
        assert row["upc"] == b.upc
        assert row["price_full"] == str(b.price_full)
        assert row["price_excl_tax"] == str(b.price_excl_tax)
        assert row["tax"] == str(b.tax)
        assert row["availability"] == str(b.availability)
        assert row["number_reviews"] == str(b.number_reviews)

    async def test_save_and_load_roundtrip(self) -> None:
        # arrange
        b1 = ScrapeBookFaker.fake(model_id=1, title="Dune", upc=Upc("A1B2C3"))
        b2 = ScrapeBookFaker.fake(model_id=2, title="Neuromancer", upc=Upc("Z9Y8X7"))

        # act
        await self._repository.save_books_async([b1, b2])

        loaded = self._repository._load_store()

        # assert
        assert isinstance(loaded, ScrapeBooks)
        assert len(loaded) == 2

        titles: list[str] = [bk.title for bk in loaded]
        assert titles == ["Dune", "Neuromancer"]
        upcs: list[str] = [bk.upc for bk in loaded]
        assert upcs == ["A1B2C3", "Z9Y8X7"]

    async def test_get_all_books_async_uses_cache_and_reload_on_reset(self) -> None:
        # arrange - act - assert
        b1 = ScrapeBookFaker.fake(model_id=10, title="Book A")
        await self._repository.save_books_async([b1])

        first = await self._repository.get_all_books_async()
        assert [b.title for b in first] == ["Book A"]

        b2 = ScrapeBookFaker.fake(model_id=20, title="Book B", upc=Upc("XYZ999"))
        await self._repository.save_books_async([b2])

        cached = await self._repository.get_all_books_async()
        assert [b.title for b in cached] == ["Book A"]

        repo_mod._CACHE = None
        reloaded = await self._repository.get_all_books_async()
        assert [b.title for b in reloaded] == ["Book B"]

    def test_load_store_returns_empty_when_file_missing(self, tmp_path: Path) -> None:
        # arrange
        repo = ScrapeBookRepositoryImpl(root_dir=tmp_path / "missing.csv")

        # act
        books = repo._load_store()

        # assert
        assert isinstance(books, ScrapeBooks)
        assert len(books) == 0

    async def test_save_overwrites_file(self) -> None:
        # arrange - act
        await self._repository.save_books_async(
            [ScrapeBookFaker.fake(model_id=1), ScrapeBookFaker.fake(model_id=2, title="Other")]
        )

        await self._repository.save_books_async(
            [ScrapeBookFaker.fake(model_id=3, title="Only One", upc=Upc("ONLY1"))]
        )

        path: Path = self._repository._root_dir
        with path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows: list[dict[str, str]] = list(reader)

        assert len(rows) == 1
        assert rows[0]["id"] == "3"
        assert rows[0]["title"] == "Only One"
        assert rows[0]["upc"] == "ONLY1"
