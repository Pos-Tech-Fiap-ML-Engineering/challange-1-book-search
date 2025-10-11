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
from src.standard.app_log.AppLogger import AppLogger


class GetBookByIdUseCaseImpl(
    UseCase[GetBookByIdUseCaseInput, GetBookByIdUseCaseOutputHandler],
    UseCaseInputValidator[GetBookByIdUseCaseInput],
):
    input_type: type[GetBookByIdUseCaseInput] = GetBookByIdUseCaseInput

    def __init__(self, scrape_book_repository: ScrapeBookRepository,
                 logger: AppLogger) -> None:
        self._scrape_book_repository = scrape_book_repository
        self._logger = logger


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

        self._logger.info(f"Recovery Book id: {book.id if book else None}", )

        if book:
            self._logger.info(f"Book Info in log attributes", {
                "id": str(book.id),
                "category": str(book.category),
                "title": str(book.title),
                "price_full": str(book.price_full),
            })
            use_case_output.success(book)
        else:
            use_case_output.not_found()
