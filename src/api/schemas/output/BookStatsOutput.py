from __future__ import annotations

from decimal import Decimal
from typing import Any

from pydantic import BaseModel

from src.domain.scrape_book.vos.BookStats import BookStats


class BookStatsOutput(BaseModel):
    total_books: int
    avg_price: Decimal
    rating_distribution: dict[int, int]

    @staticmethod
    def to_output(book_stats: BookStats) -> BookStatsOutput:
        return BookStatsOutput.model_validate(book_stats.to_dict())

    @staticmethod
    def to_output_json(book_stats: BookStats) -> dict[str, Any]:
        return BookStatsOutput.to_output(book_stats).model_dump(mode="json")
