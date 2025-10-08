from src.standard.error.ApplicationError import ApplicationError
from src.standard.error.ApplicationErrorCode import ApplicationErrorCode
from src.standard.error.ApplicationErrorInfo import ApplicationErrorInfo


class ErrorStandardUseCaseNotFound(ApplicationError):
    def __init__(self, input_type: type):
        super().__init__(
            ApplicationErrorInfo(
                code=ApplicationErrorCode.STANDARD_ERROR_USE_CASE_NOT_FOUND,
                message=f"Not found UseCase to {input_type.__name__}",
                cause={
                    "use_case_input_type": input_type,
                },
                error=None,
            )
        )
