import pytest

from src.application.boundaries.use_case.output.UseCaseOutputHandlerInvalidInput import (
    UseCaseOutputHandlerInvalidInput,
)
from src.standard.built_in.Abstract import Abstract


class TestUseCaseOutputHandlerInvalidInput:
    def test_class_is_subclass_abstract(self) -> None:
        # arrange - act - assert
        assert issubclass(UseCaseOutputHandlerInvalidInput, Abstract)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            UseCaseOutputHandlerInvalidInput()  # type: ignore
