from src.standard.error.ApplicationError import ApplicationError
from src.standard.error.ApplicationErrorCode import ApplicationErrorCode
from src.standard.error.ApplicationErrorInfo import ApplicationErrorInfo


class ErrorStandardUseCaseOutputHandlerInvalidType(ApplicationError):
    def __init__(self, use_case_output_handler: type):
        super().__init__(
            ApplicationErrorInfo(
                code=ApplicationErrorCode.STANDARD_ERROR_USE_CASE_OUTPUT_HANDLER_INVALID_TYPE,
                message=f"{use_case_output_handler.__name__} must be of type UseCaseOutputHandler",
                cause=None,
                error=None,
            )
        )
