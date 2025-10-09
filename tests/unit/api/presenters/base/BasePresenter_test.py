import json

from src.api.presenters.base.BasePresenter import BasePresenter
from fastapi.responses import JSONResponse, Response

from src.application.boundaries.use_case.validator.UseCaseInputNotificationErrors import UseCaseInputNotificationErrors


class TestBasePresenter:
    async def test_result_async_default_output_not_implemented(self) -> None:
        # arrange
        presenter = BasePresenter()

        # act
        result: Response = await presenter.result_async()

        # assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 500

        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body == {"message": "Output not implemented"}

    async def test_set_result_should_override_response_function(self) -> None:
        # arrange
        presenter = BasePresenter()

        expected_response = JSONResponse(status_code=201, content={"ok": True})
        presenter._set_result(expected_response)

        # act
        result: Response = await presenter.result_async()

        # assert
        assert result is expected_response
        assert result.status_code == 201
        assert json.loads(result.body.decode("utf-8")) == {"ok": True}  # type: ignore

    async def test_invalid_input_async_should_set_bad_request_response(self) -> None:
        # arranger
        presenter = BasePresenter()
        errors = UseCaseInputNotificationErrors()
        errors.add("prop1", "Erro1")
        errors.add("prop1", "Erro2")
        errors.add("prop2", "Erro3")

        # act
        await presenter.invalid_input_async(errors)
        result: Response = await presenter.result_async()

        # assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 400

        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body["detail"] == "Invalid input"
        assert body["errors"] == errors.flatten_errors

    async def test_handler_error_async_should_set_internal_error_response(self) -> None:
        # arrange
        presenter = BasePresenter()
        error = RuntimeError("boom")

        # act
        await presenter.handler_error_async(error)
        result: Response = await presenter.result_async()

        # assert
        assert isinstance(result, JSONResponse)
        assert result.status_code == 500

        body = json.loads(result.body.decode("utf-8"))  # type: ignore
        assert body["detail"] == "Internal error"
        assert body["error"] == "boom"
