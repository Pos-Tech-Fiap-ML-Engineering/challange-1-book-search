from src.application.boundaries.use_case.UseCase import UseCase
from src.application.use_cases.category.list_categories.ListCategoriesUseCaseInput import ListCategoriesUseCaseInput
from src.application.use_cases.category.list_categories.ListCategoriesUseCaseOutputHandler import \
    ListCategoriesUseCaseOutputHandler
from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository


class ListCategoriesUseCaseImpl(UseCase[ListCategoriesUseCaseInput, ListCategoriesUseCaseOutputHandler]):
    input_type: type[ListCategoriesUseCaseInput] = ListCategoriesUseCaseInput

    def __init__(self, scrape_book_repository: ScrapeBookRepository) -> None:
        self._scrape_book_repository = scrape_book_repository

    async def execute_async(self,
                            use_case_input: ListCategoriesUseCaseInput,
                            use_case_output: ListCategoriesUseCaseOutputHandler) -> None:
        books = await self._scrape_book_repository.get_all_books_async()

        use_case_output.success(books.categories)
