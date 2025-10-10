from fastapi.responses import JSONResponse

from src.api.presenters.base.BasePresenter import BasePresenter
from src.api.schemas.output.BookOutput import BookOutput
from src.application.use_cases.book.list_all_books.ListAllBooksUseCaseOutputHandler import \
    ListAllBooksUseCaseOutputHandler
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks


class ListAllBooksUseCaseOutputPresenterImpl(BasePresenter, ListAllBooksUseCaseOutputHandler):
    def success(self, result: ScrapeBooks) -> None:
        self._set_result(JSONResponse(status_code=200,
                                      content=BookOutput.to_output_list_json(result)))
