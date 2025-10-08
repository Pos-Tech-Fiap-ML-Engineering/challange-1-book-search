from src.standard.error.ApplicationErrorCode import ApplicationErrorCode
from src.standard.error.ApplicationErrorInfo import ApplicationErrorInfo
from src.standard.error.errors.ErrorStandardUseCaseInputInvalidType import (
    ErrorStandardUseCaseInputInvalidType,
)


class TestErrorStandardUseCaseInputInvalidType:
    def test_validate_error_successfully(self) -> None:
        # arrange
        class Input: ...

        # act
        error = ErrorStandardUseCaseInputInvalidType(Input)

        # assert
        assert str(error) == f"{Input.__name__} must be of type UseCase"
        assert error.error_info == ApplicationErrorInfo(
            code=ApplicationErrorCode.STANDARD_ERROR_USE_CASE_INPUT_INVALID_TYPE,
            message=f"{Input.__name__} must be of type UseCase",
            cause=None,
            error=None,
        )
