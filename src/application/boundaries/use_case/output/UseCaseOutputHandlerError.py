from abc import abstractmethod

from .UseCaseOutputHandler import UseCaseOutputHandler


class UseCaseOutputHandlerHandlerError(UseCaseOutputHandler):
    @abstractmethod
    async def handler_error_async(self, error: Exception) -> None:
        pass
