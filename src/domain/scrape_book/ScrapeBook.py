from threading import Lock
from decimal import Decimal
from typing import ClassVar

from src.domain.scrape_book.vos.Rating import Rating
from src.domain.scrape_book.vos.Upc import Upc
from src.domain.scrape_book.vos.Money import Money


class ScrapeBook:
    __slot__ = (
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
        "id",
    )

    _id_seq: ClassVar[int] = 0
    _id_lock: ClassVar[Lock] = Lock()

    @classmethod
    def _next_id(cls) -> int:
        # thread-safe
        with cls._id_lock:
            cls._id_seq += 1
            return cls._id_seq

    def __init__(
        self,
        *,
        category: str,
        title: str,
        rating: Rating,
        product_description: str,
        upc: Upc,
        product_type: str,
        price_full: Money,
        price_excl_tax: Money,
        tax: Money,
        availability: int,
        number_reviews: int,
        image_url: str,
        product_page_url: str,
        model_id: int | None = None,
    ) -> None:
        self._id = model_id or self._next_id()
        self._category = category
        self._title = title
        self._rating = rating
        self._product_description = product_description
        self._upc = upc
        self._product_type = product_type
        self._price_full = price_full
        self._price_excl_tax = price_excl_tax
        self._tax = tax
        self._availability = availability
        self._number_reviews = number_reviews
        self._image_url = image_url
        self._product_page_url = product_page_url

    @property
    def id(self) -> int:
        return self._id

    @property
    def category(self) -> str:
        return self._category

    @property
    def title(self) -> str:
        return self._title

    @property
    def rating(self) -> int:
        return self._rating

    @property
    def product_description(self) -> str:
        return self._product_description

    @property
    def upc(self) -> str:
        return self._upc.value

    @property
    def product_type(self) -> str:
        return self._product_type

    @property
    def price_full(self) -> Decimal:
        return self._price_full.amount

    @property
    def price_excl_tax(self) -> Decimal:
        return self._price_excl_tax.amount

    @property
    def tax(self) -> Decimal:
        return self._tax.amount

    @property
    def availability(self) -> int:
        return self._availability

    @property
    def number_reviews(self) -> int:
        return self._number_reviews

    @property
    def image_url(self) -> str:
        return self._image_url

    @property
    def product_page_url(self) -> str:
        return self._product_page_url

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self._id,
            "category": self._category,
            "title": self._title,
            "rating": int(self._rating),
            "product_description": self._product_description,
            "upc": self._upc.value,
            "product_type": self._product_type,
            "price_full": self._price_full.amount,
            "price_excl_tax": self._price_excl_tax.amount,
            "tax": self._tax.amount,
            "availability": self._availability,
            "number_reviews": self._number_reviews,
            "image_url": self._image_url,
            "product_page_url": self._product_page_url,
        }
