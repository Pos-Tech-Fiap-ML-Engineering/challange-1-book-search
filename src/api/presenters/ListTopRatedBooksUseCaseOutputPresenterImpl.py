from fastapi.responses import JSONResponse
from src.api.presenters.base.BasePresenter import BasePresenter
from src.api.schemas.output.BookOutput import BookOutput
from src.application.use_cases.book.list_top_rated_books.ListTopRatedBooksUseCaseOutputHandler import \
    ListTopRatedBooksUseCaseOutputHandler
from src.domain.scrape_book.ScrapeBook import ScrapeBook


class ListTopRatedBooksUseCaseOutputPresenterImpl(BasePresenter, ListTopRatedBooksUseCaseOutputHandler):
    def success(self, result: list[ScrapeBook]) -> None:
        self._set_result(JSONResponse(status_code=200,
                                      content=BookOutput.to_output_list_json(result)))
