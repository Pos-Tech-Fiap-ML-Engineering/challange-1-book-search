from src.application.boundaries.use_case.UseCase import UseCase
from src.application.use_cases.book.list_top_rated_books.ListTopRatedBooksUseCaseInput import (
    ListTopRatedBooksUseCaseInput,
)
from src.application.use_cases.book.list_top_rated_books.ListTopRatedBooksUseCaseOutputHandler import (
    ListTopRatedBooksUseCaseOutputHandler,
)
from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository


class ListTopRatedBooksUseCaseImpl(
    UseCase[ListTopRatedBooksUseCaseInput, ListTopRatedBooksUseCaseOutputHandler]
):
    input_type: type[ListTopRatedBooksUseCaseInput] = ListTopRatedBooksUseCaseInput

    def __init__(self, scrape_book_repository: ScrapeBookRepository) -> None:
        self._scrape_book_repository = scrape_book_repository

    async def execute_async(
        self,
        use_case_input: ListTopRatedBooksUseCaseInput,
        use_case_output: ListTopRatedBooksUseCaseOutputHandler,
    ) -> None:
        books = await self._scrape_book_repository.get_all_books_async()
        top_rated_books = books.list_top_rated_books()
        use_case_output.success(top_rated_books)
