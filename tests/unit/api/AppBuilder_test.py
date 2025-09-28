from collections.abc import Iterator

import pytest
from fastapi import FastAPI

from src.api.AppBuilder import AppBuilder, V1_CONTROLLERS
from src.api.controllers.v1.HealthController import HealthController
from src.infrastructure.application.boundaries.use_case.UseCaseManagerImpl import UseCaseManagerImpl
from src.infrastructure.standard.app_log.AppLoggerImpl import AppLoggerImpl


class TestAppBuilder:
    _app_builder: AppBuilder

    @pytest.fixture(autouse=True)
    def setup_teardown(self) -> Iterator[None]:
        self._app_builder = AppBuilder()
        yield

    def test_validate_app_logger(self) -> None:
        # arrange - act - assert
        assert isinstance(self._app_builder.app_logger, AppLoggerImpl)

    def test_use_caser_manager(self) -> None:
        # arrange - act - assert
        assert isinstance(self._app_builder.use_caser_manager, UseCaseManagerImpl)

    def test_controllers(self) -> None:
        # arrange - act - assert
        assert isinstance(self._app_builder.controllers, dict)

        # v1-controllers
        v1_controllers = self._app_builder.controllers[V1_CONTROLLERS]
        assert isinstance(v1_controllers[0], HealthController)

    def test_fast_api(self) -> None:
        # arrange - act - assert
        assert isinstance(self._app_builder.fast_api, FastAPI)
