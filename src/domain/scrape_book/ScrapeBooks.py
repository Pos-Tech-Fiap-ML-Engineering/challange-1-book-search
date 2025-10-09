from src.domain.scrape_book.ScrapeBook import ScrapeBook


class ScrapeBooks(list[ScrapeBook]):

    def __init__(self) -> None:
        self.categories: set[str] = set()
        super().__init__()

    def append(self, item: ScrapeBook) -> None:
        if not isinstance(item, ScrapeBook):
            raise TypeError("Only allowed add ScrapeBook instance")

        self.categories.add(item.category)

        super().append(item)


    def get_by_id(self, book_id: int) -> ScrapeBook | None:
        return next(filter(lambda book: book.id == book_id, self), None)
