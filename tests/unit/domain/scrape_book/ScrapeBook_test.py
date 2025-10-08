from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from enum import IntEnum

from src.domain.scrape_book.vos.Money import Money
from src.domain.scrape_book.vos.Rating import Rating
from src.domain.scrape_book.vos.Upc import Upc
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker


class FakeRating(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class TestScrapeBook:

    def test_id_autoincrement_and_override(self) -> None:
        # arrange - act
        a = ScrapeBookFaker.fake()
        b = ScrapeBookFaker.fake()

        # assert
        assert a.id != b.id
        assert b.id == a.id + 1

        explicit = ScrapeBookFaker.fake(model_id=999)
        assert explicit.id == 999

        c = ScrapeBookFaker.fake()
        assert c.id > b.id

    def test_properties_and_types(self) -> None:
        # arrange - act
        upc = Upc("Z9Y8X7")
        price_full = Money(Decimal("51.77"), "GBP")
        price_excl = Money(Decimal("51.77"), "GBP")
        tax = Money(Decimal("0.00"), "GBP")
        rating = FakeRating.FIVE

        b = ScrapeBookFaker.fake(
            category="Computers",
            title="The Pragmatic Programmer",
            rating=Rating(rating),
            product_description="Classic",
            upc=upc,
            product_type="Books",
            price_full=price_full,
            price_excl_tax=price_excl,
            tax=tax,
            availability=22,
            number_reviews=13,
            image_url="http://example.com/p.jpg",
            product_page_url="http://example.com/p",
        )

        # assert
        assert b.category == "Computers"
        assert b.title == "The Pragmatic Programmer"
        assert int(b.rating) == int(rating)
        assert b.product_description == "Classic"
        assert b.upc == "Z9Y8X7"
        assert b.product_type == "Books"
        assert b.price_full == Decimal("51.77")
        assert b.price_excl_tax == Decimal("51.77")
        assert b.tax == Decimal("0.00")
        assert b.availability == 22
        assert b.number_reviews == 13
        assert b.image_url == "http://example.com/p.jpg"
        assert b.product_page_url == "http://example.com/p"

    def test_to_dict_structure_and_values(self) -> None:
        # arrange - act
        upc = Upc("A1B2C3")
        price_full = Money(Decimal("12.34"), "GBP")
        price_excl = Money(Decimal("10.00"), "GBP")
        tax = Money(Decimal("2.34"), "GBP")
        rating = FakeRating.THREE

        b = ScrapeBookFaker.fake(
            category="Sci-Fi",
            title="Dune",
            rating=Rating(rating),
            product_description="Spice must flow",
            upc=upc,
            product_type="Books",
            price_full=price_full,
            price_excl_tax=price_excl,
            tax=tax,
            availability=5,
            number_reviews=2,
            image_url="http://example.com/dune.jpg",
            product_page_url="http://example.com/dune",
            model_id=123,
        )

        d: dict[str, object] = b.to_dict()

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

        # assert
        assert set(d.keys()) == expected_keys

        assert d["id"] == 123
        assert d["category"] == "Sci-Fi"
        assert d["title"] == "Dune"
        assert d["rating"] == int(rating)
        assert d["product_description"] == "Spice must flow"
        assert d["upc"] == "A1B2C3"
        assert d["product_type"] == "Books"
        assert d["price_full"] == Decimal("12.34")
        assert d["price_excl_tax"] == Decimal("10.00")
        assert d["tax"] == Decimal("2.34")
        assert d["availability"] == 5
        assert d["number_reviews"] == 2
        assert d["image_url"] == "http://example.com/dune.jpg"
        assert d["product_page_url"] == "http://example.com/dune"

    def test_id_generation_is_thread_safe_basic(self) -> None:
        # arrange
        def create_one() -> int:
            return ScrapeBookFaker.fake().id

        n = 50
        ids: list[int] = []

        # act
        with ThreadPoolExecutor(max_workers=10) as ex:
            for i in ex.map(lambda _: create_one(), range(n)):
                ids.append(i)

        # assert
        assert len(ids) == n
        assert len(set(ids)) == n
        assert min(ids) > 0
