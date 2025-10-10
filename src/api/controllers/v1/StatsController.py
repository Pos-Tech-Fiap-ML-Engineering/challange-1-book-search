from fastapi import APIRouter
from fastapi.responses import Response

from src.api.controllers.abstractions.BaseController import BaseController
from src.api.presenters.GetBookStatsUseCaseOutputPresenterImpl import GetBookStatsUseCaseOutputPresenterImpl
from src.api.presenters.ListStatsBooksByCategoriesUseCaseOutputPresenterImpl import \
    ListStatsBooksByCategoriesUseCaseOutputPresenterImpl
from src.api.schemas.output.BookStatsOutput import BookStatsOutput
from src.application.boundaries.use_case.UseCaseManager import UseCaseManager
from src.application.use_cases.book.get_book_stats.GetBookStatsUseCaseInput import GetBookStatsUseCaseInput
from src.application.use_cases.category.list_stats_books_by_categories.ListStatsBooksByCategoriesUseCaseInput import \
    ListStatsBooksByCategoriesUseCaseInput


class StatsController(BaseController):
    _router: APIRouter = APIRouter(prefix="/stats", tags=["stats"])

    def __init__(self, user_case_manager: UseCaseManager) -> None:
        self._user_case_manager = user_case_manager

        self._router.add_api_route(
            path="/overview",
            endpoint=self.get_book_stats_async,
            methods=["GET"],
            response_model=BookStatsOutput,
            summary="Get overview book stats ",
        )

        self._router.add_api_route(
            path="/categories",
            endpoint=self.list_book_stats_by_categories_async,
            methods=["GET"],
            response_model=dict[str, BookStatsOutput],
            summary="Get overview book stats by category",
        )

    async def get_book_stats_async(self) -> Response:
        use_case_input: GetBookStatsUseCaseInput = GetBookStatsUseCaseInput()
        use_case_output_handler: GetBookStatsUseCaseOutputPresenterImpl = GetBookStatsUseCaseOutputPresenterImpl()

        await self._user_case_manager.execute_async(use_case_input, use_case_output_handler, meta_information=None)

        return await use_case_output_handler.result_async()

    async def list_book_stats_by_categories_async(self) -> Response:
        use_case_input: ListStatsBooksByCategoriesUseCaseInput = ListStatsBooksByCategoriesUseCaseInput()
        use_case_output_handler: ListStatsBooksByCategoriesUseCaseOutputPresenterImpl = (
            ListStatsBooksByCategoriesUseCaseOutputPresenterImpl())

        await self._user_case_manager.execute_async(use_case_input, use_case_output_handler, meta_information=None)

        return await use_case_output_handler.result_async()
