from fastapi.responses import JSONResponse

from src.api.presenters.base.BasePresenter import BasePresenter
from src.api.schemas.output.BookStatsOutput import BookStatsOutput
from src.application.use_cases.book.get_book_stats.GetBookStatsUseCaseOutputHandler import \
    GetBookStatsUseCaseOutputHandler
from src.domain.scrape_book.vos.BookStats import BookStats


class GetBookStatsUseCaseOutputPresenterImpl(BasePresenter, GetBookStatsUseCaseOutputHandler):

    def success(self, result: BookStats) -> None:
        self._set_result(JSONResponse(status_code=200,
                                      content=BookStatsOutput.to_output_json(result)))
