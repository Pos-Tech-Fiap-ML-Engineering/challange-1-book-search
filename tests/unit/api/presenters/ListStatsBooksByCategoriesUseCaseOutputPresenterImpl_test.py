import json

from fastapi.responses import Response, JSONResponse

from src.api.presenters.ListStatsBooksByCategoriesUseCaseOutputPresenterImpl import \
    ListStatsBooksByCategoriesUseCaseOutputPresenterImpl
from src.api.schemas.output.BookStatsOutput import BookStatsOutput
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker


class TestListStatsBooksByCategoriesUseCaseOutputPresenterImpl:
    async def test_output_handler_success(self) -> None:
        # arrange
        presenter = ListStatsBooksByCategoriesUseCaseOutputPresenterImpl()

        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        stats_books_by_categories = books.get_stats_books_by_category()

        expected_result = {k: BookStatsOutput.to_output_json(v) for k, v in stats_books_by_categories.items()}

        # act
        presenter.success(stats_books_by_categories)
        result: Response = await presenter.result_async()

        # Assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 200
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == expected_result

    async def test_output_handler_success_empty_books(self) -> None:
        # arrange
        presenter = ListStatsBooksByCategoriesUseCaseOutputPresenterImpl()

        books = ScrapeBooks()

        stats_books_by_categories = books.get_stats_books_by_category()

        # act
        presenter.success(stats_books_by_categories)
        result: Response = await presenter.result_async()

        # Assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 200
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == {}

    async def test_result_async_default_output_not_implemented_before_success(self) -> None:
        # arrange
        presenter = ListStatsBooksByCategoriesUseCaseOutputPresenterImpl()

        # act
        result: Response = await presenter.result_async()

        # assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 500
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == {"message": "Output not implemented"}
