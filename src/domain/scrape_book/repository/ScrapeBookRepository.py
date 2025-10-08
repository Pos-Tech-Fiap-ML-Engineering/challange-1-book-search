import abc

from src.domain.scrape_book.ScrapeBook import ScrapeBook
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from src.standard.built_in.Abstract import Abstract


class ScrapeBookRepository(Abstract):
    @abc.abstractmethod
    async def save_books_async(self, scrape_books: list[ScrapeBook]) -> None:
        pass

    @abc.abstractmethod
    async def get_all_books_async(self) -> ScrapeBooks:
        pass
