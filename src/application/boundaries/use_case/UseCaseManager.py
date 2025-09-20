from __future__ import annotations

from typing import Generic, TypeVar, Optional, Dict, Type
from abc import abstractmethod

from src.standard.built_in.Abstract import Abstract
from .input.UseCaseInput import UseCaseInput
from .output.UseCaseOutputHandler import UseCaseOutputHandler

TInput = TypeVar("TInput", bound=UseCaseInput)
TOutput = TypeVar("TOutput", bound=UseCaseOutputHandler)


class UseCaseManager(Abstract, Generic[TInput, TOutput]):
    @abstractmethod
    async def execute_async(self, use_case_input: UseCaseInput, use_case_output_handler: UseCaseOutputHandler,
                            meta_information: Optional[Dict[str, str]]) -> None:
        pass
