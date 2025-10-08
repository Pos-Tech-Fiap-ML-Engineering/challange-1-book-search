from src.standard.error.ApplicationErrorCode import ApplicationErrorCode
from src.standard.error.ApplicationErrorInfo import ApplicationErrorInfo
from src.standard.error.errors.ErrorStandardUseCaseOutputHandlerInvalidType import (
    ErrorStandardUseCaseOutputHandlerInvalidType,
)


class TestErrorStandardUseCaseOutputHandlerInvalidType:
    def test_validate_error_successfully(self) -> None:
        # arrange
        class Input: ...

        # act
        error = ErrorStandardUseCaseOutputHandlerInvalidType(Input)

        # assert
        assert str(error) == f"{Input.__name__} must be of type UseCaseOutputHandler"
        assert error.error_info == ApplicationErrorInfo(
            code=ApplicationErrorCode.STANDARD_ERROR_USE_CASE_OUTPUT_HANDLER_INVALID_TYPE,
            message=f"{Input.__name__} must be of type UseCaseOutputHandler",
            cause=None,
            error=None,
        )
