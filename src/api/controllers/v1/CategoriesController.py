from fastapi import APIRouter
from fastapi.responses import Response

from src.api.controllers.abstractions.BaseController import BaseController
from src.api.presenters.ListCategoriesUseCaseOutputPresenterImpl import ListCategoriesUseCaseOutputPresenterImpl
from src.application.boundaries.use_case.UseCaseManager import UseCaseManager
from src.application.use_cases.category.list_categories.ListCategoriesUseCaseInput import ListCategoriesUseCaseInput


class CategoriesController(BaseController):
    _router: APIRouter = APIRouter(prefix="/categories", tags=["categories"])

    def __init__(self, user_case_manager: UseCaseManager) -> None:
        self._user_case_manager = user_case_manager

        self._router.add_api_route(
            path="",
            endpoint=self.list_all_categories_async,
            methods=["GET"],
            response_model=list[str],
            summary="List all categories",
        )


    async def list_all_categories_async(self) -> Response:
        use_case_input: ListCategoriesUseCaseInput = ListCategoriesUseCaseInput()
        use_case_output_handler: ListCategoriesUseCaseOutputPresenterImpl = ListCategoriesUseCaseOutputPresenterImpl()

        await self._user_case_manager.execute_async(use_case_input, use_case_output_handler, meta_information=None)

        return await use_case_output_handler.result_async()
