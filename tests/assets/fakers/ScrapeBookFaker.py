from decimal import Decimal

from src.domain.scrape_book.ScrapeBook import ScrapeBook
from src.domain.scrape_book.vos.Money import Money
from src.domain.scrape_book.vos.Rating import Rating
from src.domain.scrape_book.vos.Upc import Upc
from src.standard.built_in.Static import Static
from tests.assets.fakers.base.AppTestFaker import AppTestFaker


class ScrapeBookFaker(Static):
    _CATEGORIES = ["Fiction", "Technology", "Science", "Poetry", "History"]

    @classmethod
    def fake(
        cls,
        *,
        category: str | None = None,
        title: str | None = None,
        rating: Rating | None = None,
        product_description: str | None = None,
        upc: Upc | None = None,
        product_type: str | None = None,
        price_full: Money | None = None,
        price_excl_tax: Money | None = None,
        tax: Money | None = None,
        availability: int | None = None,
        number_reviews: int | None = None,
        image_url: str | None = None,
        product_page_url: str | None = None,
        model_id: int | None = None,
    ) -> ScrapeBook:
        price = Money(Decimal(AppTestFaker.fake.random_number(digits=2)))
        return ScrapeBook(
            category=category or AppTestFaker.fake.random_element(cls._CATEGORIES),
            title=title or AppTestFaker.fake.sentence(nb_words=1),
            rating=rating or Rating(AppTestFaker.fake.random_int(min=1, max=5)),
            product_description=product_description or AppTestFaker.fake.sentence(nb_words=1),
            upc=upc or Upc("a897fe39b1053632"),
            product_type=product_type or "Books",
            price_full=price_full or price,
            price_excl_tax=price_excl_tax or price,
            tax=tax or Money(Decimal(0)),
            availability=availability or AppTestFaker.fake.random_int(min=0, max=100),
            number_reviews=number_reviews or AppTestFaker.fake.random_int(min=0, max=50),
            image_url=image_url or AppTestFaker.fake.image_url(),
            product_page_url=product_page_url or AppTestFaker.fake.url(),
            model_id=model_id,
        )
