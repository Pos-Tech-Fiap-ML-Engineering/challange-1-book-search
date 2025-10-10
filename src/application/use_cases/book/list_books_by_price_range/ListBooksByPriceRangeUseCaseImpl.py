from src.application.boundaries.use_case.UseCase import UseCase
from src.application.boundaries.use_case.UseCaseInputValidator import UseCaseInputValidator
from src.application.boundaries.use_case.validator.UseCaseInputNotificationErrors import (
    UseCaseInputNotificationErrors,
)
from src.application.use_cases.book.list_books_by_price_range.ListBooksByPriceRangeUseCaseInput import (
    ListBooksByPriceRangeUseCaseInput,
)
from src.application.use_cases.book.list_books_by_price_range.ListBooksByPriceRangeUseCaseOutputHandler import (
    ListBooksByPriceRangeUseCaseOutputHandler,
)
from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository


class ListBooksByPriceRangeUseCaseImpl(
    UseCase[ListBooksByPriceRangeUseCaseInput, ListBooksByPriceRangeUseCaseOutputHandler],
    UseCaseInputValidator,
):
    input_type: type[ListBooksByPriceRangeUseCaseInput] = ListBooksByPriceRangeUseCaseInput

    def __init__(self, scrape_book_repository: ScrapeBookRepository) -> None:
        self._scrape_book_repository = scrape_book_repository

    async def impl_validate_async(
        self,
        use_case_input: ListBooksByPriceRangeUseCaseInput,
        errors: UseCaseInputNotificationErrors,
    ) -> None:
        use_case_input.validate_input(errors)

    async def execute_async(
        self,
        use_case_input: ListBooksByPriceRangeUseCaseInput,
        use_case_output: ListBooksByPriceRangeUseCaseOutputHandler,
    ) -> None:
        books = await self._scrape_book_repository.get_all_books_async()

        filtered_books_by_price_range = books.list_books_by_price_range(
            use_case_input.min_price, use_case_input.max_price
        )

        use_case_output.success(filtered_books_by_price_range)
