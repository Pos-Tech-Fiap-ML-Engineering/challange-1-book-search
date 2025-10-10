import abc

from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler
from src.domain.scrape_book.vos.BookStats import BookStats


class ListStatsBooksByCategoriesUseCaseOutputHandler(UseCaseOutputHandler):
    @abc.abstractmethod
    def success(self, stats_books_by_categories: dict[str, BookStats]) -> None:
        pass