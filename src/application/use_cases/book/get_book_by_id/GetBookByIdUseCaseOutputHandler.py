import abc

from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler
from src.domain.scrape_book.ScrapeBook import ScrapeBook


class GetBookByIdUseCaseOutputHandler(UseCaseOutputHandler):
    @abc.abstractmethod
    def success(self, book: ScrapeBook) -> None:
        pass

    @abc.abstractmethod
    def not_found(self) -> None:
        pass
