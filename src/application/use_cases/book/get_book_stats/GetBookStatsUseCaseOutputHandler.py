import abc

from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler
from src.domain.scrape_book.vos.BookStats import BookStats


class GetBookStatsUseCaseOutputHandler(UseCaseOutputHandler):

    @abc.abstractmethod
    def success(self, result: BookStats) -> None:
        pass
