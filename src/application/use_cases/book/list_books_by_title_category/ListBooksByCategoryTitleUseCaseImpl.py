from src.application.boundaries.use_case.UseCase import UseCase
from src.application.use_cases.book.list_books_by_title_category.ListBooksByCategoryTitleUseCaseInput import (
    ListBooksByCategoryTitleUseCaseInput,
)
from src.application.use_cases.book.list_books_by_title_category.ListBooksByCategoryTitleUseCaseOutputHandler import (
    ListBooksByCategoryTitleUseCaseOutputHandler,
)
from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository


class ListBooksByCategoryTitleUseCaseImpl(
    UseCase[ListBooksByCategoryTitleUseCaseInput, ListBooksByCategoryTitleUseCaseOutputHandler]
):
    input_type: type[ListBooksByCategoryTitleUseCaseInput] = ListBooksByCategoryTitleUseCaseInput

    def __init__(self, scrape_book_repository: ScrapeBookRepository) -> None:
        self._scrape_book_repository = scrape_book_repository

    async def execute_async(
        self,
        use_case_input: ListBooksByCategoryTitleUseCaseInput,
        use_case_output: ListBooksByCategoryTitleUseCaseOutputHandler,
    ) -> None:
        books = await self._scrape_book_repository.get_all_books_async()

        books_result = books.list_books_by_category_or_title(
            title=use_case_input.title, category=use_case_input.category
        )

        use_case_output.success(books_result)
