from src.api.presenters.base.BasePresenter import BasePresenter
from src.api.schemas.output.BookOutput import BookOutput
from src.application.use_cases.book.get_book_by_id.GetBookByIdUseCaseOutputHandler import \
    GetBookByIdUseCaseOutputHandler
from src.domain.scrape_book.ScrapeBook import ScrapeBook

from fastapi.responses import JSONResponse


class GetBookByIdUseCaseOutputPresenterImpl(BasePresenter, GetBookByIdUseCaseOutputHandler):
    def success(self, book: ScrapeBook) -> None:
        self._set_result(JSONResponse(status_code=200, content=BookOutput.to_output_json(book)))

    def not_found(self) -> None:
        self._set_result(JSONResponse(status_code=404, content={}))
