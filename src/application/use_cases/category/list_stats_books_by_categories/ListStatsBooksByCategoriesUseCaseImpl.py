from src.application.boundaries.use_case.UseCase import UseCase
from src.application.use_cases.category.list_stats_books_by_categories.ListStatsBooksByCategoriesUseCaseInput import (  # noqa: E501
    ListStatsBooksByCategoriesUseCaseInput,
)
from src.application.use_cases.category.list_stats_books_by_categories.ListStatsBooksByCategoriesUseCaseOutputHandler import (  # noqa: E501
    ListStatsBooksByCategoriesUseCaseOutputHandler,
)
from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository


class ListStatsBooksByCategoriesUseCaseImpl(
    UseCase[ListStatsBooksByCategoriesUseCaseInput, ListStatsBooksByCategoriesUseCaseOutputHandler]
):
    input_type: type[ListStatsBooksByCategoriesUseCaseInput] = (
        ListStatsBooksByCategoriesUseCaseInput
    )

    def __init__(self, scrape_book_repository: ScrapeBookRepository) -> None:
        self._scrape_book_repository = scrape_book_repository

    async def execute_async(
        self,
        use_case_input: ListStatsBooksByCategoriesUseCaseInput,
        use_case_output: ListStatsBooksByCategoriesUseCaseOutputHandler,
    ) -> None:
        books = await self._scrape_book_repository.get_all_books_async()

        use_case_output.success(books.get_stats_books_by_category())
