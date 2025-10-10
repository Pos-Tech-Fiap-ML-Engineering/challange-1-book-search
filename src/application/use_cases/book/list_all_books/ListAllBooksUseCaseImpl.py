from src.application.boundaries.use_case.UseCase import UseCase
from src.application.use_cases.book.list_all_books.ListAllBooksUseCaseInput import (
    ListAllBooksUseCaseInput,
)
from src.application.use_cases.book.list_all_books.ListAllBooksUseCaseOutputHandler import (
    ListAllBooksUseCaseOutputHandler,
)
from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository


class ListAllBooksUseCaseImpl(UseCase[ListAllBooksUseCaseInput, ListAllBooksUseCaseOutputHandler]):
    input_type: type[ListAllBooksUseCaseInput] = ListAllBooksUseCaseInput

    def __init__(self, scrape_book_repository: ScrapeBookRepository) -> None:
        self._repository = scrape_book_repository

    async def execute_async(
        self,
        use_case_input: ListAllBooksUseCaseInput,
        use_case_output: ListAllBooksUseCaseOutputHandler,
    ) -> None:
        books = await self._repository.get_all_books_async()

        use_case_output.success(books)
