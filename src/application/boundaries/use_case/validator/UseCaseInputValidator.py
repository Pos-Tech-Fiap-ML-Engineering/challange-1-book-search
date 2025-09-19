from __future__ import annotations

from abc import abstractmethod
from typing import Generic, TypeVar

from src.standard.built_in.Abstract import Abstract
from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.application.boundaries.use_case.validator.UseCaseInputNotificationErrors import UseCaseInputNotificationErrors

TInput = TypeVar("TInput", bound=UseCaseInput)


class UseCaseInputValidator(Abstract, Generic[TInput]):
    @abstractmethod
    async def validate_async(self, use_case_input: TInput, errors: UseCaseInputNotificationErrors, ) -> None:
        pass
