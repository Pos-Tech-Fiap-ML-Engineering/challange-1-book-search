from collections.abc import Iterator
from unittest.mock import Mock

import pytest
from fastapi import APIRouter
from pytest_mock import MockerFixture

from src.api.controllers.Router import Router
from src.api.controllers.abstractions.BaseController import BaseController
from src.standard.built_in.Static import Static
from tests.assets.mocks.BaseControllerMock import BaseControllerMock


class TestRouter:
    _v1_controller_1_mock: Mock
    _v1_controller_2_mock: Mock
    _v1_controllers: list[BaseController]

    @pytest.fixture(autouse=True)
    def setup_teardown(
        self, request: pytest.FixtureRequest, mocker: MockerFixture
    ) -> Iterator[None]:
        self._v1_controller_1_mock = BaseControllerMock.create(mocker)
        self._v1_controller_2_mock = BaseControllerMock.create(mocker)
        self._v1_controllers = [self._v1_controller_1_mock, self._v1_controller_2_mock]
        yield

    def test_class_is_subclass_static(self) -> None:
        # arrange - act - assert
        assert issubclass(Router, Static)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            Router()

    def test_populate_routers_successfully(self, mocker: MockerFixture) -> None:
        # arrange
        base_router = APIRouter()
        base_router_spi_include_router = mocker.spy(base_router, "include_router")

        self._v1_controller_1_mock.get_router.side_effect = None
        self._v1_controller_2_mock.get_router.side_effect = None

        # act
        router_result = Router.get_router(
            base_router=base_router, v1_controllers=self._v1_controllers
        )

        # assert
        assert router_result is not None
        self._v1_controller_1_mock.get_router.assert_called_once()
        self._v1_controller_2_mock.get_router.assert_called_once()

        assert base_router.prefix == "/api"
        assert base_router_spi_include_router.call_count == 2
        base_router_spi_include_router.assert_any_call(
            self._v1_controller_1_mock.get_router(), prefix="/v1"
        )
        base_router_spi_include_router.assert_any_call(
            self._v1_controller_2_mock.get_router(), prefix="/v1"
        )
