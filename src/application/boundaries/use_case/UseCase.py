from __future__ import annotations

from abc import abstractmethod
from typing import Generic, TypeVar, Type
from src.standard.built_in.Abstract import Abstract
from .input.UseCaseInput import UseCaseInput
from .output.UseCaseOutput import UseCaseOutput

TInput = TypeVar("TInput", bound=UseCaseInput)
TOutput = TypeVar("TOutput", bound=UseCaseOutput)


class UseCase(Abstract, Generic[TInput, TOutput]):
    input_type: Type[UseCaseInput]
    output_type: Type[UseCaseOutput]

    @abstractmethod
    async def execute_async(self, use_case_input: TInput, use_case_output: TOutput) -> None:
        pass
