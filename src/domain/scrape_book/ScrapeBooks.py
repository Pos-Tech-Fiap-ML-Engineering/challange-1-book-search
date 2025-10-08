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
