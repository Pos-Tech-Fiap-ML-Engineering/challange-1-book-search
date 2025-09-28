from src.application.boundaries.use_case.UseCase import UseCase
from src.application.boundaries.use_case.UseCaseManager import UseCaseManager
from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler
from src.application.boundaries.use_case.output.UseCaseOutputHandlerHandlerError import (
    UseCaseOutputHandlerHandlerError,
)
from src.application.boundaries.use_case.output.UseCaseOutputHandlerInvalidInput import (
    UseCaseOutputHandlerInvalidInput,
)
from src.application.boundaries.use_case.UseCaseInputValidator import UseCaseInputValidator
from src.standard.app_log.AppLogger import AppLogger
from src.standard.error.errors.ErrorStandardUseCaseNotFound import ErrorStandardUseCaseNotFound
from src.standard.error.errors.ErrorStandardUseCaseOutputNotHandlerInvalidInput import (
    ErrorStandardUseCaseOutputNotHandlerInvalidInput,
)


class UseCaseManagerImpl(UseCaseManager):

    def __init__(self, logger: AppLogger, use_cases: list[UseCase]) -> None:
        self._logger: AppLogger = logger
        self._use_cases: dict[tuple[type[UseCaseInput], type[UseCaseOutputHandler]], UseCase] = {
            (uc.input_type, uc.output_type): uc for uc in use_cases
        }

    async def execute_async(
        self,
        use_case_input: UseCaseInput,
        use_case_output_handler: UseCaseOutputHandler,
        meta_information: dict[str, str] | None,
    ) -> None:
        uc = self._find_use_case(use_case_input, use_case_output_handler)
        uc_name = type(uc).__name__
        with self._logger.new_scope(uc_name, extra=meta_information):
            try:
                self._logger.info(f"Running use case {uc_name}")

                if await self._is_invalid_input_async(use_case_input, use_case_output_handler, uc):
                    return

                await uc.execute_async(use_case_input, use_case_output_handler)

                self._logger.info(f"End of execution use case {uc_name}")
            except Exception as e:
                await self._handler_error_async(e, use_case_output_handler)

    def _find_use_case(
        self, use_case_input: UseCaseInput, use_case_output_handler: UseCaseOutputHandler
    ) -> UseCase:
        use_case_input_type = type(use_case_input)
        use_case_output_type = type(use_case_output_handler)

        uc = self._use_cases.get((use_case_input_type, use_case_output_type), None)
        if uc is not None:
            return uc

        raise ErrorStandardUseCaseNotFound(use_case_input_type, use_case_output_type)

    async def _is_invalid_input_async(
        self,
        use_case_input: UseCaseInput,
        use_case_output_handler: UseCaseOutputHandler,
        use_case: UseCase,
    ) -> bool:
        if not isinstance(use_case, UseCaseInputValidator):
            return False

        errors = await use_case.validate_async(use_case_input)
        if not errors.has_errors:
            return False

        flat_errors: dict[str, str] = errors.flatten_errors

        self._logger.error(f"Invalid input {type(use_case_input).__name__}", extra=flat_errors)

        if not isinstance(use_case_output_handler, UseCaseOutputHandlerInvalidInput):
            raise ErrorStandardUseCaseOutputNotHandlerInvalidInput(type(use_case_output_handler))

        await use_case_output_handler.invalid_input_async(errors)

        return True

    async def _handler_error_async(
        self, error: Exception, use_case_output: UseCaseOutputHandler
    ) -> None:
        self._logger.error(f"Unhandled error: {error!r}", exc_info=error)

        if not isinstance(use_case_output, UseCaseOutputHandlerHandlerError):
            raise error

        await use_case_output.handler_error_async(error)
