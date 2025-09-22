import pytest

from src.standard.built_in.Abstract import Abstract
from src.standard.error.ApplicationError import ApplicationError


class TestApplicationError:
    def test_class_is_subclass_abstract(self) -> None:
        # arrange - act - assert
        assert issubclass(ApplicationError, Abstract)

    def test_class_is_subclass_exception(self) -> None:
        # arrange - act - assert
        assert issubclass(ApplicationError, Exception)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            ApplicationError()  # type: ignore
