from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from src.domain.scrape_book.ScrapeBook import ScrapeBook
from src.domain.scrape_book.vos.BookStats import BookStats


class ScrapeBooks(list[ScrapeBook]):

    def __init__(self) -> None:
        self._categories: set[str] = set()
        super().__init__()

    def append(self, item: ScrapeBook) -> None:
        if not isinstance(item, ScrapeBook):
            raise TypeError("Only allowed add ScrapeBook instance")

        self._categories.add(item.category)

        super().append(item)

    @property
    def categories(self) -> set[str]:
        return self._categories

    def get_by_id(self, book_id: int) -> ScrapeBook | None:
        return next(filter(lambda book: book.id == book_id, self), None)

    def list_books_by_category_or_title(self, title: str | None = None, category: str | None = None) -> list[
        ScrapeBook]:
        if title is None and category is None:
            return self

        title_lower = title.lower() if title else None
        category_lower = category.lower() if category else None

        def _filter(book: ScrapeBook) -> bool:
            title_match = title_lower == book.title.lower() if title_lower else False
            category_match = category_lower == book.category.lower() if category_lower else False

            if title_lower and category_lower:
                return title_match and category_match

            return title_match or category_match

        return list(filter(_filter, self))

    def get_stats_books(self) -> BookStats:
        return self._internal_get_books_stats(self)

    def get_stats_books_by_category(self) -> dict[str, BookStats]:
        out: dict[str, BookStats] = {}

        if len(self) == 0:
            return out

        for category in self.categories:
            books: list[ScrapeBook] = list(filter(lambda book: book.category == category, self))
            out[category] = self._internal_get_books_stats(books)

        return out

    @staticmethod
    def _internal_get_books_stats(books: ScrapeBooks | list[ScrapeBook]) -> BookStats:
        total_books = len(books)
        sum_price = Decimal("0")
        rating_distribution: dict[int, int] = {}

        if total_books == 0:
            return BookStats(total_books=total_books, avg_price=sum_price, rating_distribution=rating_distribution)

        for book in books:
            price = book.price_full if isinstance(book.price_full, Decimal) else Decimal(str(book.price_full))
            sum_price += price

            r: int = int(book.rating)
            rating_distribution[r] = rating_distribution.get(r, 0) + 1

        avg = (sum_price / Decimal(total_books)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return BookStats(total_books, avg, rating_distribution)

    def list_top_rated_books(self, limit: int = 10) -> list[ScrapeBook]:
        return sorted(self, key=lambda book: book.rating, reverse=True)[:limit]
