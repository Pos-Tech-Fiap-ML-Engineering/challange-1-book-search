import pytest

from src.application.boundaries.use_case.UseCaseInputValidator import UseCaseInputValidator
from src.standard.built_in.Abstract import Abstract


class TestUseCaseInputValidator:
    def test_class_is_subclass_abstract(self) -> None:
        # arrange - act - assert
        assert issubclass(UseCaseInputValidator, Abstract)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            UseCaseInputValidator()  # type: ignore
