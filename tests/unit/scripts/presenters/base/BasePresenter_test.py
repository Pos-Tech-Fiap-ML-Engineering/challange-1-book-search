from __future__ import annotations

import pytest

from src.application.boundaries.use_case.validator.UseCaseInputNotificationErrors import (
    UseCaseInputNotificationErrors,
)
from src.scripts.presenters.base.BasePresenter import BasePresenter


class TestBasePresenter:

    async def test_result_async_without_response_func_raises_not_implemented(self) -> None:
        # arrange
        presenter = BasePresenter()

        # act - assert
        with pytest.raises(NotImplementedError):
            await presenter.result_async()

    async def test_result_async_with_injected_response_func_is_called(self) -> None:
        # arrange
        presenter = BasePresenter()

        called: list[str] = []

        async def ok_handler() -> None:
            called.append("ok")

        # act
        presenter._response_func = ok_handler

        await presenter.result_async()

        # assert
        assert called == ["ok"]

    async def test_invalid_input_async_raises_exception_with_flatten_errors(self) -> None:
        # arrange
        presenter = BasePresenter()
        errors = UseCaseInputNotificationErrors()
        errors.add("prop1", "Erro1")
        errors.add("prop1", "Erro2")
        errors.add("prop2", "Erro3")

        # act - assert
        with pytest.raises(Exception) as exc_info:
            await presenter.invalid_input_async(errors)

        assert "{'prop1_1': 'Erro1', 'prop1_2': 'Erro2', 'prop2_1': 'Erro3'}" in str(exc_info.value)

    async def test_handler_error_async_re_raises_original_exception(self) -> None:
        # arrange - act
        presenter = BasePresenter()
        original = RuntimeError("boom")

        # assert
        with pytest.raises(RuntimeError) as exc_info:
            await presenter.handler_error_async(original)
        assert exc_info.value is original
