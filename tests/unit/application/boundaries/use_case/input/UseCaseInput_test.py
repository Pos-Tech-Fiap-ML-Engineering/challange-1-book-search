import pytest

from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.standard.built_in.Abstract import Abstract


class TestUseCaseInput:
    def test_class_is_subclass_abstract(self) -> None:
        # arrange - act - assert
        assert issubclass(UseCaseInput, Abstract)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            UseCaseInput()
