import abc

from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks


class ListAllBooksUseCaseOutputHandler(UseCaseOutputHandler):

    @abc.abstractmethod
    def success(self, result: ScrapeBooks) -> None:
        pass
