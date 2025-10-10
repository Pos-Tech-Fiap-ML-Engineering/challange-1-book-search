import abc

from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler
from src.domain.scrape_book.ScrapeBook import ScrapeBook


class ListTopRatedBooksUseCaseOutputHandler(UseCaseOutputHandler):
    @abc.abstractmethod
    def success(self, result: list[ScrapeBook]) -> None:
        pass
