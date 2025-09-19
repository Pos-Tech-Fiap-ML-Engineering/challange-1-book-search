from __future__ import annotations

from abc import abstractmethod
from typing import Generic, TypeVar

from src.standard import Abstract
from .input.UseCaseInput import UseCaseInput
from .validator.UseCaseInputNotificationErrors import UseCaseInputNotificationErrors

TInput = TypeVar("TInput", bound=UseCaseInput)


class UseCaseInputValidator(Abstract, Generic[TInput]):
    @abstractmethod
    async def validate_async(self, use_case_input: TInput, errors: UseCaseInputNotificationErrors, ) -> None:
        pass
