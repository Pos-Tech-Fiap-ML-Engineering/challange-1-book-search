import json
from fastapi.responses import Response, JSONResponse

from src.api.presenters.GetBookStatsUseCaseOutputPresenterImpl import GetBookStatsUseCaseOutputPresenterImpl
from src.api.schemas.output.BookStatsOutput import BookStatsOutput
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker


class TestGetBookStatsUseCaseOutputPresenterImpl:
    async def test_output_handler_success(self) -> None:
        # arrange
        presenter = GetBookStatsUseCaseOutputPresenterImpl()

        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        book_stats = books.get_stats_books()

        expected_result = BookStatsOutput.to_output_json(book_stats)

        # act
        presenter.success(book_stats)
        result: Response = await presenter.result_async()

        # Assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 200
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == expected_result

    async def test_output_handler_success_empty_books(self) -> None:
        # arrange
        presenter = GetBookStatsUseCaseOutputPresenterImpl()

        books = ScrapeBooks()

        book_stats = books.get_stats_books()

        expected_result = BookStatsOutput.to_output_json(book_stats)

        # act
        presenter.success(book_stats)
        result: Response = await presenter.result_async()

        # Assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 200
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == expected_result

    async def test_result_async_default_output_not_implemented_before_success(self) -> None:
        # arrange
        presenter = GetBookStatsUseCaseOutputPresenterImpl()

        # act
        result: Response = await presenter.result_async()

        # assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 500
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == {"message": "Output not implemented"}
