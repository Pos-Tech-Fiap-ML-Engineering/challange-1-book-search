from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar
from src.standard.built_in.Abstract import Abstract
from .input.UseCaseInput import UseCaseInput
from .output.UseCaseOutputHandler import UseCaseOutputHandler

TInput = TypeVar("TInput", bound=UseCaseInput)
TOutput = TypeVar("TOutput", bound=UseCaseOutputHandler)


class UseCase[TInput, TOutput](Abstract):
    input_type: type[UseCaseInput]
    output_type: type[UseCaseOutputHandler]

    @abstractmethod
    async def execute_async(self, use_case_input: TInput, use_case_output: TOutput) -> None:
        pass
