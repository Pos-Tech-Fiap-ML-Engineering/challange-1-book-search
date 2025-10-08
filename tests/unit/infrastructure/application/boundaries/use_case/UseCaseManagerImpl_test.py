import pytest
from pytest_mock import MockerFixture
from unittest.mock import Mock, AsyncMock, call
from typing import NoReturn, Any, cast
from collections.abc import Iterator

from src.application.boundaries.use_case.UseCase import UseCase
from src.application.boundaries.use_case.UseCaseInputValidator import UseCaseInputValidator, TInput
from src.application.boundaries.use_case.UseCaseManager import UseCaseManager
from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler
from src.application.boundaries.use_case.output.UseCaseOutputHandlerHandlerError import (
    UseCaseOutputHandlerHandlerError,
)
from src.application.boundaries.use_case.output.UseCaseOutputHandlerInvalidInput import (
    UseCaseOutputHandlerInvalidInput,
)
from src.application.boundaries.use_case.validator.UseCaseInputNotificationErrors import (
    UseCaseInputNotificationErrors,
)
from src.infrastructure.application.boundaries.use_case.UseCaseManagerImpl import UseCaseManagerImpl
from src.standard.error.errors.ErrorStandardUseCaseInputInvalidType import (
    ErrorStandardUseCaseInputInvalidType,
)
from src.standard.error.errors.ErrorStandardUseCaseNotFound import ErrorStandardUseCaseNotFound
from src.standard.error.errors.ErrorStandardUseCaseOutputHandlerInvalidType import (
    ErrorStandardUseCaseOutputHandlerInvalidType,
)
from src.standard.error.errors.ErrorStandardUseCaseOutputNotHandlerInvalidInput import (
    ErrorStandardUseCaseOutputNotHandlerInvalidInput,
)
from tests.assets.mocks.AppLoggerMock import AppLoggerMock
from tests.assets.utils.pytest.StrictMock import StrictMock


class _UseCaseInputTest(UseCaseInput): ...


class _UseCaseOutputHandlerTest(UseCaseOutputHandler): ...


# noinspection PyUnresolvedReferences
class _UseCaseOutputHandlerTestHandlerErrorAndInvalidInput(
    UseCaseOutputHandlerHandlerError, UseCaseOutputHandlerInvalidInput
):
    def __init__(self) -> None:
        self.handler_error_async_mock = StrictMock.make_async_strict_mock()
        self.invalid_input_async_mock = StrictMock.make_async_strict_mock()

    async def handler_error_async(self, error: Exception) -> None:
        await self.handler_error_async_mock(error)

    async def invalid_input_async(self, errors: UseCaseInputNotificationErrors) -> None:
        await self.invalid_input_async_mock(errors)


# noinspection PyUnresolvedReferences
class _UseCaseOk(UseCase[_UseCaseInputTest, _UseCaseOutputHandlerTest]):
    input_type: type[_UseCaseInputTest] = _UseCaseInputTest

    def __init__(self) -> None:
        self.execute_async_mock: AsyncMock = StrictMock.make_async_strict_mock()

    async def execute_async(
        self,
        use_case_input: _UseCaseInputTest,
        use_case_output_handler: _UseCaseOutputHandlerTest,
    ) -> None:
        await self.execute_async_mock(use_case_input, use_case_output_handler)


# noinspection PyUnresolvedReferences
class _UseCaseValidator(
    UseCase[_UseCaseInputTest, _UseCaseOutputHandlerTestHandlerErrorAndInvalidInput],
    UseCaseInputValidator,
):
    input_type: type[_UseCaseInputTest] = _UseCaseInputTest

    def __init__(self) -> None:
        self.execute_async_mock = StrictMock.make_async_strict_mock()
        self.validate_async_mock = StrictMock.make_async_strict_mock()

    async def impl_validate_async(
        self, use_case_input: TInput, errors: UseCaseInputNotificationErrors
    ) -> None:
        await self.validate_async_mock(use_case_input, errors)

    async def execute_async(
        self,
        use_case_input: _UseCaseInputTest,
        use_case_output_handler: _UseCaseOutputHandlerTestHandlerErrorAndInvalidInput,
    ) -> None:
        await self.execute_async_mock(use_case_input, use_case_output_handler)


# noinspection PyUnresolvedReferences
class _UseCaseValidatorWithoutOutputUseCaseHandlerValidatorInput(
    UseCase[_UseCaseInputTest, _UseCaseOutputHandlerTest],
    UseCaseInputValidator,
):
    input_type: type[_UseCaseInputTest] = _UseCaseInputTest

    def __init__(self) -> None:
        self.execute_async_mock = StrictMock.make_async_strict_mock()
        self.validate_async_mock = StrictMock.make_async_strict_mock()

    async def impl_validate_async(
        self, use_case_input: TInput, errors: UseCaseInputNotificationErrors
    ) -> None:
        await self.validate_async_mock(use_case_input, errors)

    async def execute_async(
        self,
        use_case_input: _UseCaseInputTest,
        use_case_output_handler: _UseCaseOutputHandlerTest,
    ) -> None:
        await self.execute_async_mock(use_case_input, use_case_output_handler)


# noinspection PyUnresolvedReferences
class _OutputWithInvalidInputAndHandler(
    UseCaseOutputHandlerInvalidInput,
    UseCaseOutputHandlerHandlerError,
):

    def __init__(self) -> None:
        self.invalid_input_async_mock = StrictMock.make_async_strict_mock()
        self.handler_error_async_mock = StrictMock.make_async_strict_mock()

    async def invalid_input_async(self, errors: UseCaseInputNotificationErrors) -> None:
        await self.invalid_input_async_mock(errors)

    async def handler_error_async(self, error: Exception) -> None:
        await self.handler_error_async_mock(error)


class TestUseCaseManagerImpl:
    _logger_mock: Mock
    _useCaseManager: UseCaseManager
    _use_cases: list[UseCase]

    @pytest.fixture(autouse=True)
    def setup_teardown(
        self, request: pytest.FixtureRequest, mocker: MockerFixture
    ) -> Iterator[None]:
        self._logger_mock = AppLoggerMock.create(mocker)

        scope_cm = mocker.MagicMock()
        scope_cm.__enter__.return_value = None
        scope_cm.__exit__.return_value = None

        self._logger_mock.new_scope.side_effect = None
        self._logger_mock.new_scope.return_value = scope_cm

        yield

    async def test_execute_successfully_use_case(self) -> None:
        # arrange
        inp = _UseCaseInputTest()
        out = _UseCaseOutputHandlerTest()
        meta = {"req-id": "123"}

        uc = _UseCaseOk()

        use_case_manager = UseCaseManagerImpl(self._logger_mock, [uc])

        self._logger_mock.info.side_effect = None

        uc.execute_async_mock.side_effect = None

        # act
        await use_case_manager.execute_async(inp, out, meta_information=meta)

        # assert
        self._logger_mock.new_scope.assert_called_once_with(type(uc).__name__, meta)

        assert self._logger_mock.info.call_count == 2
        self._logger_mock.info.assert_has_calls(
            [
                call("Running use case _UseCaseOk"),
                call("End of execution use case _UseCaseOk"),
            ]
        )

        uc.execute_async_mock.assert_awaited_once_with(inp, out)

    async def test_execute_successfully_use_case_with_input_validator_output_handler_input_and_error(
        self,
    ) -> None:
        # arrange
        inp = _UseCaseInputTest()
        out = _UseCaseOutputHandlerTestHandlerErrorAndInvalidInput()
        meta = {"req-id": "123"}

        uc = _UseCaseValidator()

        use_case_manager = UseCaseManagerImpl(self._logger_mock, [uc])

        self._logger_mock.info.side_effect = None

        uc.execute_async_mock.side_effect = None

        uc.validate_async_mock.side_effect = None

        # act
        await use_case_manager.execute_async(inp, out, meta_information=meta)

        # assert
        self._logger_mock.new_scope.assert_called_once_with(type(uc).__name__, meta)

        assert self._logger_mock.info.call_count == 2
        self._logger_mock.info.assert_has_calls(
            [
                call("Running use case _UseCaseValidator"),
                call("End of execution use case _UseCaseValidator"),
            ]
        )

        uc.execute_async_mock.assert_awaited_once_with(inp, out)

        assert uc.validate_async_mock.call_count == 1
        called_args, called_kwargs = uc.validate_async_mock.call_args
        assert called_args[0] is inp
        assert isinstance(called_args[1], UseCaseInputNotificationErrors)

    async def test_raise_when_input_is_not_instance_use_case_input(self) -> None:
        # arrange
        class _InvalidInput: ...

        use_case_input = _InvalidInput()
        use_case_manager = UseCaseManagerImpl(self._logger_mock, [])

        # act - assert
        with pytest.raises(ErrorStandardUseCaseInputInvalidType):
            # noinspection PyInvalidCast
            await use_case_manager.execute_async(
                cast(UseCaseInput, use_case_input),
                _UseCaseOutputHandlerTest(),
                meta_information=None,
            )

    async def test_raise_when_output_is_not_instance_use_case_output_handler(self) -> None:
        # arrange
        class _InvalidOutputHandler: ...

        use_case_output_handler = _InvalidOutputHandler()
        use_case_manager = UseCaseManagerImpl(self._logger_mock, [])

        # act - assert
        with pytest.raises(ErrorStandardUseCaseOutputHandlerInvalidType):
            # noinspection PyInvalidCast
            await use_case_manager.execute_async(
                _UseCaseInputTest(),
                cast(UseCaseOutputHandler, use_case_output_handler),
                meta_information=None,
            )

    async def test_raise_when_not_found_use_case(self) -> None:
        # arrange
        use_case_manager = UseCaseManagerImpl(self._logger_mock, [])

        # act - assert
        with pytest.raises(ErrorStandardUseCaseNotFound):
            await use_case_manager.execute_async(
                _UseCaseInputTest(), _UseCaseOutputHandlerTest(), meta_information=None
            )

    async def test_use_case_invalid_input_raise_when_use_case_output_not_handler_invalid_input(
        self,
    ) -> None:
        # arrange
        inp = _UseCaseInputTest()
        out = _UseCaseOutputHandlerTest()
        meta = {"req-id": "123"}

        uc = _UseCaseValidatorWithoutOutputUseCaseHandlerValidatorInput()

        use_case_manager = UseCaseManagerImpl(self._logger_mock, [uc])

        self._logger_mock.info.side_effect = None
        self._logger_mock.error.side_effect = None

        def _inject_errors(_i, errs) -> None:  # type: ignore
            errs.add("prop1", "error_1")

        uc.validate_async_mock.side_effect = _inject_errors

        # act - assert
        with pytest.raises(ErrorStandardUseCaseOutputNotHandlerInvalidInput):
            await use_case_manager.execute_async(inp, out, meta_information=meta)

        # assert
        self._logger_mock.new_scope.assert_called_once_with(type(uc).__name__, meta)

        self._logger_mock.info.assert_called_once_with(
            "Running use case _UseCaseValidatorWithoutOutputUseCaseHandlerValidatorInput"
        )

        assert self._logger_mock.error.call_count == 2
        called_args, called_kwargs = self._logger_mock.error.call_args_list[0]
        assert len(called_args) == 1
        assert called_args[0] == "Invalid input _UseCaseInputTest"
        assert called_kwargs["extra"] == {"prop1_1": "error_1"}

        called_args, called_kwargs = self._logger_mock.error.call_args_list[1]
        assert len(called_args) == 1
        assert (
            called_args[0]
            == "Unhandled error: ErrorStandardUseCaseOutputNotHandlerInvalidInput('UseCaseOutputHandler _UseCaseOutputHandlerTest not handler invalid input')"
        )
        assert isinstance(
            called_kwargs["exc_info"], ErrorStandardUseCaseOutputNotHandlerInvalidInput
        )

        assert uc.validate_async_mock.call_count == 1
        called_args, called_kwargs = uc.validate_async_mock.call_args
        assert len(called_args) == 2
        assert called_args[0] == inp
        assert isinstance(called_args[1], UseCaseInputNotificationErrors)
        assert called_kwargs == {}

    async def test_use_case_invalid_input_with_output_handler_invalid_input(self) -> None:
        # arrange
        inp = _UseCaseInputTest()
        out = _UseCaseOutputHandlerTestHandlerErrorAndInvalidInput()
        meta = {"req-id": "123"}

        uc = _UseCaseValidator()

        use_case_manager = UseCaseManagerImpl(self._logger_mock, [uc])

        self._logger_mock.info.side_effect = None
        self._logger_mock.error.side_effect = None

        def _inject_errors(_i, errs) -> None:  # type: ignore
            errs.add("prop1", "error_1")
            errs.add("prop1", "error_2")
            errs.add("prop2", "error_3")
            errs.add("prop2", "error_4")

        uc.validate_async_mock.side_effect = _inject_errors

        out.invalid_input_async_mock.side_effect = None

        # act
        await use_case_manager.execute_async(inp, out, meta_information=meta)

        # assert
        self._logger_mock.new_scope.assert_called_once_with(type(uc).__name__, meta)

        self._logger_mock.info.assert_called_once_with("Running use case _UseCaseValidator")
        self._logger_mock.error.assert_called_once_with(
            f"Invalid input {type(inp).__name__}",
            extra={
                "prop1_1": "error_1",
                "prop1_2": "error_2",
                "prop2_1": "error_3",
                "prop2_2": "error_4",
            },
        )

        assert uc.validate_async_mock.call_count == 1
        called_args, called_kwargs = uc.validate_async_mock.call_args
        assert called_args[0] == inp
        assert isinstance(called_args[1], UseCaseInputNotificationErrors)
        assert called_kwargs == {}

        assert out.invalid_input_async_mock.call_count == 1
        called_args, called_kwargs = out.invalid_input_async_mock.call_args
        assert isinstance(called_args[0], UseCaseInputNotificationErrors)
        assert called_args[0].errors == {
            "prop1": ["error_1", "error_2"],
            "prop2": ["error_3", "error_4"],
        }
        assert called_kwargs == {}

    async def test_execute_use_case_unexpected_exception_with_output_handler_error(self) -> None:
        # arrange
        inp = _UseCaseInputTest()
        out = _UseCaseOutputHandlerTestHandlerErrorAndInvalidInput()
        meta = {"req-id": "123"}
        exc = Exception("FAIL")

        uc = _UseCaseValidator()

        use_case_manager = UseCaseManagerImpl(self._logger_mock, [uc])

        self._logger_mock.info.side_effect = None
        self._logger_mock.error.side_effect = None

        def side_effect_execute_async(*args: tuple, **kwargs: dict[str, Any]) -> NoReturn:
            raise exc

        uc.execute_async_mock.side_effect = side_effect_execute_async

        uc.validate_async_mock.side_effect = None

        out.handler_error_async_mock.side_effect = None

        # act
        await use_case_manager.execute_async(inp, out, meta_information=meta)

        # assert
        self._logger_mock.new_scope.assert_called_once_with(type(uc).__name__, meta)

        self._logger_mock.info.assert_called_once_with("Running use case _UseCaseValidator")

        self._logger_mock.error.call_count = 1
        called_args, called_kwargs = self._logger_mock.error.call_args_list[0]
        assert len(called_args) == 1
        assert called_args[0] == "Unhandled error: Exception('FAIL')"
        assert isinstance(called_kwargs["exc_info"], Exception)

        uc.execute_async_mock.assert_awaited_once_with(inp, out)

        assert uc.validate_async_mock.call_count == 1
        called_args, called_kwargs = uc.validate_async_mock.call_args
        assert len(called_args) == 2
        assert called_args[0] is inp
        assert isinstance(called_args[1], UseCaseInputNotificationErrors)
        assert called_kwargs == {}

        out.handler_error_async_mock.assert_called_once_with(exc)

    async def test_execute_use_case_unexpected_exception_and_raise_exception_when_output_not_handler_error(
        self,
    ) -> None:
        # arrange
        inp = _UseCaseInputTest()
        out = _UseCaseOutputHandlerTest()
        meta = {"req-id": "123"}
        exc = Exception("FAIL")

        uc = _UseCaseOk()

        use_case_manager = UseCaseManagerImpl(self._logger_mock, [uc])

        self._logger_mock.info.side_effect = None
        self._logger_mock.error.side_effect = None

        def side_effect_execute_async(*args: tuple, **kwargs: dict[str, Any]) -> NoReturn:
            raise exc

        uc.execute_async_mock.side_effect = side_effect_execute_async

        # act - assert
        with pytest.raises(Exception):
            await use_case_manager.execute_async(inp, out, meta_information=meta)

        self._logger_mock.new_scope.assert_called_once_with(type(uc).__name__, meta)

        self._logger_mock.info.assert_called_once_with("Running use case _UseCaseOk")

        self._logger_mock.error.call_count = 1
        called_args, called_kwargs = self._logger_mock.error.call_args_list[0]
        assert len(called_args) == 1
        assert called_args[0] == "Unhandled error: Exception('FAIL')"
        assert isinstance(called_kwargs["exc_info"], Exception)

        uc.execute_async_mock.assert_awaited_once_with(inp, out)
