from __future__ import annotations
from decimal import Decimal
from typing import Any

from pydantic import BaseModel

from src.domain.scrape_book.ScrapeBook import ScrapeBook
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
    def to_output(book: ScrapeBook) -> BookOutput:
        return BookOutput.model_validate(book.to_dict())

    @staticmethod
    def to_output_list(books: ScrapeBooks | list[ScrapeBook]) -> list[BookOutput]:
        return [BookOutput.to_output(b) for b in books]

    @staticmethod
    def to_output_json(book: ScrapeBook) -> dict[str, Any]:
        return BookOutput.to_output(book).model_dump(mode="json")

    @staticmethod
    def to_output_list_json(books: ScrapeBooks | list[ScrapeBook]) -> list[dict[str, Any]]:
        return [b.model_dump(mode="json") for b in BookOutput.to_output_list(books)]
