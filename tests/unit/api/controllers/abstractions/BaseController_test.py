import pytest

from src.api.controllers.abstractions.BaseController import BaseController
from src.standard.built_in.Abstract import Abstract


class TestBaseController:
    def test_class_is_subclass_abstract(self) -> None:
        # arrange - act - assert
        assert issubclass(BaseController, Abstract)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            BaseController()
