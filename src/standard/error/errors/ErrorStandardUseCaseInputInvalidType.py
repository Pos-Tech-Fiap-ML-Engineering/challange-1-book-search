from src.standard.error.ApplicationError import ApplicationError
from src.standard.error.ApplicationErrorCode import ApplicationErrorCode
from src.standard.error.ApplicationErrorInfo import ApplicationErrorInfo


class ErrorStandardUseCaseInputInvalidType(ApplicationError):
    def __init__(self, use_case_input: type):
        super().__init__(
            ApplicationErrorInfo(
                code=ApplicationErrorCode.STANDARD_ERROR_USE_CASE_INPUT_INVALID_TYPE,
                message=f"{use_case_input.__name__} must be of type UseCase",
                cause=None,
                error=None,
            )
        )
