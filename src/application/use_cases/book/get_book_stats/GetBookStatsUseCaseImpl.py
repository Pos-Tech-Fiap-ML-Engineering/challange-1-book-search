from src.application.boundaries.use_case.UseCase import UseCase
from src.application.use_cases.book.get_book_stats.GetBookStatsUseCaseInput import GetBookStatsUseCaseInput
from src.application.use_cases.book.get_book_stats.GetBookStatsUseCaseOutputHandler import \
    GetBookStatsUseCaseOutputHandler
from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository


class GetBookStatsUseCaseImpl(UseCase[GetBookStatsUseCaseInput, GetBookStatsUseCaseOutputHandler]):
    input_type: type[GetBookStatsUseCaseInput] = GetBookStatsUseCaseInput

    def __init__(self, scrape_book_repository: ScrapeBookRepository) -> None:
        self._scrape_book_repository = scrape_book_repository

    async def execute_async(self, use_case_input: GetBookStatsUseCaseInput,
                            use_case_output: GetBookStatsUseCaseOutputHandler) -> None:
        books = await self._scrape_book_repository.get_all_books_async()

        use_case_output.success(books.get_stats_books())
