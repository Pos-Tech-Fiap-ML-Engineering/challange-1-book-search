import pytest

from src.application.boundaries.factory.HttpClientFactory import HttpClientFactory
from src.standard.built_in.Abstract import Abstract


class TestHttpClientFactory:
    def test_class_is_subclass_abstract(self) -> None:
        # arrange - act - assert
        assert issubclass(HttpClientFactory, Abstract)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            HttpClientFactory()  # type: ignore
