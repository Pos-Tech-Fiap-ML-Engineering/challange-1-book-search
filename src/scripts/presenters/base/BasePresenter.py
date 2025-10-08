from typing import Any
from collections.abc import Callable, Awaitable

from src.application.boundaries.use_case.output.UseCaseOutputHandlerHandlerError import (
    UseCaseOutputHandlerHandlerError,
)
from src.application.boundaries.use_case.output.UseCaseOutputHandlerInvalidInput import (
    UseCaseOutputHandlerInvalidInput,
)
from src.application.boundaries.use_case.validator.UseCaseInputNotificationErrors import (
    UseCaseInputNotificationErrors,
)


class BasePresenter(UseCaseOutputHandlerInvalidInput, UseCaseOutputHandlerHandlerError):

    def __init__(self) -> None:
        async def _not_impl(*args: Any, **kwargs: Any) -> None:
            raise NotImplementedError("Must implements _response_func")

        self._response_func: Callable[..., Awaitable[None]] = _not_impl

    async def result_async(self) -> None:
        await self._response_func()

    async def invalid_input_async(self, input_errors: UseCaseInputNotificationErrors) -> None:
        raise Exception(input_errors.flatten_errors)

    async def handler_error_async(self, error: Exception) -> None:
        raise error
