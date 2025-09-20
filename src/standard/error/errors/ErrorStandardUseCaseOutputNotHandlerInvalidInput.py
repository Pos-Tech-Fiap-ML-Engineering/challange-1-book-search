from src.standard.error.ApplicationError import ApplicationError
from src.standard.error.ApplicationErrorCode import ApplicationErrorCode
from src.standard.error.ApplicationErrorInfo import ApplicationErrorInfo


class ErrorStandardUseCaseOutputNotHandlerInvalidInput(ApplicationError):
    def __init__(self, use_case_output_handler: type) -> None:
        super().__init__(
            ApplicationErrorInfo(code=ApplicationErrorCode.STANDARD_ERROR_USE_CASE_OUTPUT_NOT_HANDLER_INVALID_INPUT,
                                 message=f"UseCaseOutputHandler {use_case_output_handler.__name__} not handler invalid input",
                                 cause=None,
                                 error=None)
        )
