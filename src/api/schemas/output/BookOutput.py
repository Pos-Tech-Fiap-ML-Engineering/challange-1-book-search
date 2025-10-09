from __future__ import annotations
from decimal import Decimal
from typing import Any

from pydantic import BaseModel

from src.domain.scrape_book.ScrapeBooks import ScrapeBooks


class BookOutput(BaseModel):
    id: int
    category: str
    title: str
    rating: int
    product_description: str
    upc: str
    product_type: str
    price_full: Decimal
    price_excl_tax: Decimal
    tax: Decimal
    availability: int
    number_reviews: int
    image_url: str
    product_page_url: str

    @staticmethod
    def to_output_list(books: ScrapeBooks) -> list[BookOutput]:
        return [BookOutput.model_validate(b.to_dict()) for b in books]

    @staticmethod
    def to_output_list_json(books: ScrapeBooks) -> list[dict[str, Any]]:
        return [b.model_dump(mode="json") for b in BookOutput.to_output_list(books)]


