from src.standard.error.ApplicationErrorInfo import ApplicationErrorInfo


class ApplicationError(Exception):

    def __init__(self, error_info: ApplicationErrorInfo):
        self._error_info = error_info
        super().__init__(error_info.message)

    @property
    def error_info(self) -> ApplicationErrorInfo:
        return self._error_info
