import json

from fastapi.responses import JSONResponse, Response

from src.api.presenters.GetBookByIdUseCaseOutputPresenterImpl import (
    GetBookByIdUseCaseOutputPresenterImpl,
)
from src.api.schemas.output.BookOutput import BookOutput
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker


class TestGetBookByIdUseCaseOutputPresenterImpl:
    async def test_output_handler_success(self) -> None:
        # arrange
        presenter = GetBookByIdUseCaseOutputPresenterImpl()

        book = ScrapeBookFaker.fake()

        expected_result = BookOutput.to_output_json(book)

        # act
        presenter.success(book)

        result: Response = await presenter.result_async()

        # assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 200
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == expected_result

    async def test_output_handler_not_found(self) -> None:
        # arrange
        presenter: GetBookByIdUseCaseOutputPresenterImpl = GetBookByIdUseCaseOutputPresenterImpl()

        # act
        presenter.not_found()

        result: Response = await presenter.result_async()

        # assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 404
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == {}

    async def test_result_async_default_output_not_implemented_before_success(self) -> None:
        # arrange
        presenter = GetBookByIdUseCaseOutputPresenterImpl()

        # act
        result: Response = await presenter.result_async()

        # assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 500
        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == {"message": "Output not implemented"}
