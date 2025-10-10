from src.application.boundaries.use_case.UseCase import UseCase
from src.application.boundaries.use_case.UseCaseInputValidator import UseCaseInputValidator
from src.application.boundaries.use_case.validator.UseCaseInputNotificationErrors import (
    UseCaseInputNotificationErrors,
)
from src.application.use_cases.book.get_book_by_id.GetBookByIdUseCaseInput import (
    GetBookByIdUseCaseInput,
)
from src.application.use_cases.book.get_book_by_id.GetBookByIdUseCaseOutputHandler import (
    GetBookByIdUseCaseOutputHandler,
)
from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository


class GetBookByIdUseCaseImpl(
    UseCase[GetBookByIdUseCaseInput, GetBookByIdUseCaseOutputHandler],
    UseCaseInputValidator[GetBookByIdUseCaseInput],
):
    input_type: type[GetBookByIdUseCaseInput] = GetBookByIdUseCaseInput

    def __init__(self, scrape_book_repository: ScrapeBookRepository) -> None:
        self._scrape_book_repository = scrape_book_repository

    async def impl_validate_async(
        self,
        use_case_input: GetBookByIdUseCaseInput,
        errors: UseCaseInputNotificationErrors,
    ) -> None:
        use_case_input.validate_input(errors)

    async def execute_async(
        self,
        use_case_input: GetBookByIdUseCaseInput,
        use_case_output: GetBookByIdUseCaseOutputHandler,
    ) -> None:
        books = await self._scrape_book_repository.get_all_books_async()
        book = books.get_by_id(use_case_input.id)

        if book:
            use_case_output.success(book)
        else:
            use_case_output.not_found()
