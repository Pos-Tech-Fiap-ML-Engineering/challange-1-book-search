from abc import abstractmethod

from .UseCaseOutput import UseCaseOutput


class UseCaseOutputHandler(UseCaseOutput):
    @abstractmethod
    async def handler_error_async(self, error: Exception) -> None:
        pass
