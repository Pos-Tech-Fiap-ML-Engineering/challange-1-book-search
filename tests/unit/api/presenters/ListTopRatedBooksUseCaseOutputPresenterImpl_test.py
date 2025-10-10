import json

from fastapi.responses import Response, JSONResponse

from src.api.presenters.ListTopRatedBooksUseCaseOutputPresenterImpl import ListTopRatedBooksUseCaseOutputPresenterImpl
from src.api.schemas.output.BookOutput import BookOutput
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker


class TestListTopRatedBooksUseCaseOutputPresenterImpl:
    async def test_output_handler_success(self) -> None:
        # arrange
        presenter = ListTopRatedBooksUseCaseOutputPresenterImpl()

        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        top_rated_books = books.list_top_rated_books()

        expected_result = BookOutput.to_output_list_json(top_rated_books)

        # act
        presenter.success(top_rated_books)
        result: Response = await presenter.result_async()

        # Assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 200
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == expected_result

    async def test_output_handler_success_empty_books(self) -> None:
        # arrange
        presenter = ListTopRatedBooksUseCaseOutputPresenterImpl()

        books = ScrapeBooks()

        top_rated_books = books.list_top_rated_books()

        # act
        presenter.success(top_rated_books)
        result: Response = await presenter.result_async()

        # Assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 200
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == []

    async def test_result_async_default_output_not_implemented_before_success(self) -> None:
        # arrange
        presenter = ListTopRatedBooksUseCaseOutputPresenterImpl()

        # act
        result: Response = await presenter.result_async()

        # assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 500
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == {"message": "Output not implemented"}
