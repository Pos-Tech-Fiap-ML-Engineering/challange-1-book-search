from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class BookStats:
    total_books: int
    avg_price: Decimal
    rating_distribution: dict[int, int]

    def to_dict(self) -> dict[str, object]:
        return {
            "total_books": self.total_books,
            "avg_price": self.avg_price,
            "rating_distribution": self.rating_distribution,
        }
