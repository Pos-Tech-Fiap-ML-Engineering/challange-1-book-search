from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar

from src.standard.built_in.Abstract import Abstract
from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.application.boundaries.use_case.validator.UseCaseInputNotificationErrors import (
    UseCaseInputNotificationErrors,
)

TInput = TypeVar("TInput", bound=UseCaseInput)


class UseCaseInputValidator[TInput](Abstract):

    async def validate_async(self, use_case_input: TInput) -> UseCaseInputNotificationErrors:
        errors = UseCaseInputNotificationErrors.empty()
        await self.impl_validate_async(use_case_input, errors)
        return errors

    @abstractmethod
    async def impl_validate_async(
        self,
        use_case_input: TInput,
        errors: UseCaseInputNotificationErrors,
    ) -> None:
        pass
