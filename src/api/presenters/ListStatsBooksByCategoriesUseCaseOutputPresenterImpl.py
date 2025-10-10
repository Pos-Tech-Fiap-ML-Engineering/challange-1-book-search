from fastapi.responses import JSONResponse
from src.api.presenters.base.BasePresenter import BasePresenter
from src.api.schemas.output.BookStatsOutput import BookStatsOutput
from src.application.use_cases.category.list_stats_books_by_categories.ListStatsBooksByCategoriesUseCaseOutputHandler import \
    ListStatsBooksByCategoriesUseCaseOutputHandler
from src.domain.scrape_book.vos.BookStats import BookStats


class ListStatsBooksByCategoriesUseCaseOutputPresenterImpl(BasePresenter,
                                                           ListStatsBooksByCategoriesUseCaseOutputHandler):
    def success(self, stats_books_by_categories: dict[str, BookStats]) -> None:
        parsed_result = {k: BookStatsOutput.to_output_json(v) for k, v in stats_books_by_categories.items()}
        self._set_result(JSONResponse(status_code=200,
                                      content=parsed_result))
