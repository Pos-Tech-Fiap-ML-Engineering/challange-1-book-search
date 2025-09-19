from abc import abstractmethod
from .UseCaseOutput import UseCaseOutput
from ..validator.UseCaseInputNotificationErrors import UseCaseInputNotificationErrors


class UseCaseOutputInvalidInput(UseCaseOutput):
    @abstractmethod
    async def invalid_input_async(self, input_errors: UseCaseInputNotificationErrors) -> None:
        pass
