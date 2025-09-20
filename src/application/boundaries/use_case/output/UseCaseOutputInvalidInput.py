from abc import abstractmethod
from .UseCaseOutputHandler import UseCaseOutputHandler
from ..validator.UseCaseInputNotificationErrors import UseCaseInputNotificationErrors


class UseCaseOutputHandlerInvalidInput(UseCaseOutputHandler):
    @abstractmethod
    async def invalid_input_async(self, input_errors: UseCaseInputNotificationErrors) -> None:
        pass
