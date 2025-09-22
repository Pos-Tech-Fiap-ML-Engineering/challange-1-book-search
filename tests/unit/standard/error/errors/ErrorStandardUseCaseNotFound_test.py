from src.standard.error.ApplicationErrorCode import ApplicationErrorCode
from src.standard.error.ApplicationErrorInfo import ApplicationErrorInfo
from src.standard.error.errors.ErrorStandardUseCaseNotFound import ErrorStandardUseCaseNotFound


class TestErrorStandardUseCaseNotFound:
    def test_validate_error_successfully(self) -> None:
        # arrange
        class Input:
            ...

        class Output:
            ...

        # act
        error = ErrorStandardUseCaseNotFound(Input, Output)

        # assert
        assert str(error) == "Not found UseCase to Input/Output"
        assert error.error_info == ApplicationErrorInfo(code=ApplicationErrorCode.STANDARD_ERROR_USE_CASE_NOT_FOUND,
                                                        message=f"Not found UseCase to {Input.__name__}/{Output.__name__}",
                                                        cause={
                                                            'use_case_input_type': Input,
                                                            'use_case_outpu_type': Output,
                                                        },
                                                        error=None)
