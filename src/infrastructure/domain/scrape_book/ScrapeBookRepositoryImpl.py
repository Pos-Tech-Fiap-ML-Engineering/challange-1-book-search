import csv
from pathlib import Path

from src.domain.scrape_book.ScrapeBook import ScrapeBook
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository
from src.domain.scrape_book.vos.Money import Money
from src.domain.scrape_book.vos.Rating import Rating
from src.domain.scrape_book.vos.Upc import Upc
from src.infrastructure.utils.RootDir import RootDir

_CACHE: ScrapeBooks | None = None
_ROOT_DIR = Path.joinpath(RootDir.find_root_by_file_name(), "src", "data") / "books.csv"


class ScrapeBookRepositoryImpl(ScrapeBookRepository):

    def __init__(self, root_dir: Path = _ROOT_DIR) -> None:
        self._root_dir = root_dir

    async def save_books_async(self, scrape_books: list[ScrapeBook]) -> None:
        rows = [self._to_row(b) for b in scrape_books]
        with open(self._root_dir, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    async def get_all_books_async(self) -> ScrapeBooks:
        return self._get_store()

    @staticmethod
    def _to_row(b: ScrapeBook) -> dict[str, str]:
        return {
            "id": str(b.id),
            "category": b.category,
            "title": b.title,
            "rating": str(b.rating),
            "product_description": b.product_description,
            "upc": b.upc,
            "product_type": b.product_type,
            "price_full": str(b.price_full),
            "price_excl_tax": str(b.price_excl_tax),
            "tax": str(b.tax),
            "availability": str(b.availability),
            "number_reviews": str(b.number_reviews),
            "image_url": b.image_url,
            "product_page_url": b.product_page_url,
        }

    def _get_store(self) -> ScrapeBooks:
        global _CACHE
        if _CACHE is None:
            _CACHE = self._load_store()

        return _CACHE

    def _load_store(self) -> ScrapeBooks:
        books: ScrapeBooks = ScrapeBooks()

        if not self._root_dir.exists():
            return books

        with self._root_dir.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                books.append(
                    ScrapeBook(
                        category=row["category"],
                        title=row["title"],
                        rating=Rating(int(row["rating"])),
                        product_description=row["product_description"],
                        upc=Upc(row["upc"]),
                        product_type=row["product_type"],
                        price_full=Money.from_string(row["price_full"]),
                        price_excl_tax=Money.from_string(row["price_excl_tax"]),
                        tax=Money.from_string(row["tax"]),
                        availability=int(row["availability"]),
                        number_reviews=int(row["number_reviews"]),
                        image_url=row["image_url"],
                        product_page_url=row["product_page_url"],
                        model_id=int(row["id"]),
                    )
                )

        return books
