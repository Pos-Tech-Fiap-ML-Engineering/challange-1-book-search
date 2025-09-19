from typing import Type, Optional, Dict, List, Tuple

from src.application.boundaries.use_case.UseCase import UseCase
from src.application.boundaries.use_case.UseCaseManager import UseCaseManager
from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.application.boundaries.use_case.output.UseCaseOutput import UseCaseOutput
from src.standard.app_log.AppLogger import AppLogger
from src.standard.error.errors.ErrorStandardUseCaseNotFound import ErrorStandardUseCaseNotFound


class UseCaseManagerImpl(UseCaseManager):

    def __init__(self, logger: AppLogger, use_cases: List[UseCase]) -> None:
        self._logger: AppLogger = logger
        self._use_cases: Dict[Tuple[Type[UseCaseInput], Type[UseCaseOutput]], UseCase] = {
            (uc.input_type, uc.output_type): uc
            for uc in use_cases
        }

    async def execute_async(self, use_case_input: UseCaseInput, use_case_output: UseCaseOutput,
                            meta_information: Optional[Dict[str, str]]) -> None:
        uc = self._find_use_case(use_case_input, use_case_output)

    def _find_use_case(self, use_case_input: UseCaseInput, use_case_output: UseCaseOutput) -> UseCase:
        use_case_input_type = type(use_case_input)
        use_case_output_type = type(use_case_output)

        uc = self._use_cases.get((use_case_input_type, use_case_output_type), None)

        if uc is not None:
            return uc

        raise ErrorStandardUseCaseNotFound(use_case_input_type, use_case_output_type)
