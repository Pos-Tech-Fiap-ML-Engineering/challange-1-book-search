import json

from fastapi.responses import Response, JSONResponse

from src.api.presenters.ListCategoriesUseCaseOutputPresenterImpl import (
    ListCategoriesUseCaseOutputPresenterImpl,
)
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker


class TestListCategoriesUseCaseOutputPresenterImpl:
    async def test_output_handler_success(self) -> None:
        # arrange
        presenter = ListCategoriesUseCaseOutputPresenterImpl()

        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        expected_result = list(books.categories)

        # act
        presenter.success(books.categories)
        result: Response = await presenter.result_async()

        # Assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 200
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == expected_result

    async def test_output_handler_success_empty_books(self) -> None:
        # arrange
        presenter = ListCategoriesUseCaseOutputPresenterImpl()

        books = ScrapeBooks()

        # act
        presenter.success(books.categories)

        result: Response = await presenter.result_async()

        # Assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 200
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == []

    async def test_result_async_default_output_not_implemented_before_success(self) -> None:
        # arrange
        presenter = ListCategoriesUseCaseOutputPresenterImpl()

        # act
        result: Response = await presenter.result_async()

        # assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 500
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == {"message": "Output not implemented"}
