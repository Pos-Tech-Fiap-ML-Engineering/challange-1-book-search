import pytest

from src.standard.app_log.AppLogger import AppLogger
from src.standard.built_in.Abstract import Abstract


class TestAppLogger:
    def test_class_is_subclass_abstract(self) -> None:
        # arrange - act - assert
        assert issubclass(AppLogger, Abstract)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            AppLogger()  # type: ignore
