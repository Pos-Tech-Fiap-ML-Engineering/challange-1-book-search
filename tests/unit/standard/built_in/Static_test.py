import pytest

from src.standard.built_in.Static import Static


class TestStatic:
    def test_class_is_subclass_abstract(self) -> None:
        # arrange - act - assert
        assert issubclass(Static, object)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            Static()
