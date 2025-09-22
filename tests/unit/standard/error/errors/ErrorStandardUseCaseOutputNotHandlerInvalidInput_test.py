from src.standard.error.ApplicationErrorCode import ApplicationErrorCode
from src.standard.error.ApplicationErrorInfo import ApplicationErrorInfo
from src.standard.error.errors.ErrorStandardUseCaseOutputNotHandlerInvalidInput import \
    ErrorStandardUseCaseOutputNotHandlerInvalidInput


class TestErrorStandardUseCaseOutputNotHandlerInvalidInput:
    def test_validate_error_successfully(self) -> None:
        # arrange
        class Output:
            ...

        # act
        error = ErrorStandardUseCaseOutputNotHandlerInvalidInput(Output)

        # assert
        assert str(error) == "UseCaseOutputHandler Output not handler invalid input"
        assert error.error_info == ApplicationErrorInfo(
            code=ApplicationErrorCode.STANDARD_ERROR_USE_CASE_OUTPUT_NOT_HANDLER_INVALID_INPUT,
            message=f"UseCaseOutputHandler {Output.__name__} not handler invalid input",
            cause=None,
            error=None)
