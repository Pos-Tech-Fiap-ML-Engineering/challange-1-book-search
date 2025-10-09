from typing import Any, Callable, Awaitable

from fastapi.responses import JSONResponse, Response

from src.application.boundaries.use_case.output.UseCaseOutputHandlerHandlerError import UseCaseOutputHandlerHandlerError
from src.application.boundaries.use_case.output.UseCaseOutputHandlerInvalidInput import UseCaseOutputHandlerInvalidInput
from src.application.boundaries.use_case.validator.UseCaseInputNotificationErrors import UseCaseInputNotificationErrors


class BasePresenter(UseCaseOutputHandlerInvalidInput, UseCaseOutputHandlerHandlerError):
    def __init__(self) -> None:
        async def _not_impl(*args: Any, **kwargs: Any) -> Response:
            return JSONResponse(
                status_code=500,
                content={'message': "Output not implemented"},
            )

        self._response_func: Callable[..., Awaitable[Response]] = _not_impl

    def _set_result(self, result: Response) -> None:
        async def _resp() -> Response:
            return result

        self._response_func = _resp

    async def result_async(self) -> Response:
        return await self._response_func()

    async def invalid_input_async(self, input_errors: UseCaseInputNotificationErrors) -> None:
        self._set_result(JSONResponse(status_code=400,
                                      content={"detail": "Invalid input", "errors": input_errors.flatten_errors}))

    async def handler_error_async(self, error: Exception) -> None:
        self._set_result(JSONResponse(
            status_code=500,
            content={"detail": "Internal error", "error": str(error)})
        )
