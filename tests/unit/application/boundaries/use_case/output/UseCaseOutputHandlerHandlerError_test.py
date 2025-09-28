import pytest

from src.application.boundaries.use_case.output.UseCaseOutputHandlerHandlerError import (
    UseCaseOutputHandlerHandlerError,
)
from src.standard.built_in.Abstract import Abstract


class TestUseCaseOutputHandlerHandlerError:
    def test_class_is_subclass_abstract(self) -> None:
        # arrange - act - assert
        assert issubclass(UseCaseOutputHandlerHandlerError, Abstract)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            UseCaseOutputHandlerHandlerError()  # type: ignore
