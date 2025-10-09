from fastapi import APIRouter
from fastapi.responses import Response

from src.api.controllers.abstractions.BaseController import BaseController
from src.api.presenters.GetBookByIdUseCaseOutputPresenterImpl import GetBookByIdUseCaseOutputPresenterImpl
from src.api.presenters.ListAllBooksUseCaseOutputPresenterImpl import ListAllBooksUseCaseOutputPresenterImpl
from src.api.schemas.output.BookOutput import BookOutput
from src.application.boundaries.use_case.UseCaseManager import UseCaseManager
from src.application.use_cases.book.get_book_by_id.GetBookByIdUseCaseInput import GetBookByIdUseCaseInput
from src.application.use_cases.book.list_all_books.ListAllBooksUseCaseInput import ListAllBooksUseCaseInput


class BooksController(BaseController):
    _router: APIRouter = APIRouter(prefix="/books", tags=["books"])

    def __init__(self, user_case_manager: UseCaseManager) -> None:
        self._user_case_manager = user_case_manager

        self._router.add_api_route(
            path="",
            endpoint=self.list_all_books_async,
            methods=["GET"],
            response_model=list[BookOutput],
            summary="List all books",
        )

        self._router.add_api_route(
            path="/{book_id}",
            endpoint=self.get_book_by_id_async,
            methods=["GET"],
            response_model=BookOutput | None,
            summary="Get book by id",
        )

    async def list_all_books_async(self) -> Response:
        use_case_input: ListAllBooksUseCaseInput = ListAllBooksUseCaseInput()
        use_case_output_handler: ListAllBooksUseCaseOutputPresenterImpl = ListAllBooksUseCaseOutputPresenterImpl()

        await self._user_case_manager.execute_async(use_case_input, use_case_output_handler, meta_information=None)

        return await use_case_output_handler.result_async()

    async def get_book_by_id_async(self, book_id: int) -> Response:
        use_case_input: GetBookByIdUseCaseInput = GetBookByIdUseCaseInput(book_id)
        use_case_output_handler: GetBookByIdUseCaseOutputPresenterImpl = GetBookByIdUseCaseOutputPresenterImpl()

        await self._user_case_manager.execute_async(use_case_input, use_case_output_handler,
                                                    meta_information={"book_id": str(book_id)})

        return await use_case_output_handler.result_async()
