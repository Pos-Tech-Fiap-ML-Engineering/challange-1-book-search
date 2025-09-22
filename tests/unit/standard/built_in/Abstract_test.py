from abc import ABC

import pytest

from src.standard.built_in.Abstract import Abstract


class TestAbstract:
    def test_class_is_subclass_abstract(self) -> None:
        # arrange - act - assert
        assert issubclass(Abstract, ABC)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            Abstract()
