import inspect
from collections.abc import Iterator, Callable
from typing import Any
from collections.abc import Coroutine

import pytest
from fastapi import FastAPI

from src.AppBuilder import AppBuilder
from src.api.controllers.v1.HealthController import HealthController
from src.infrastructure.application.boundaries.factory.HttpClientFactoryImpl import (
    HttpClientFactoryImpl,
)
from src.infrastructure.application.boundaries.use_case.UseCaseManagerImpl import UseCaseManagerImpl
from src.infrastructure.domain.scrape_book.ScrapeBookRepositoryImpl import ScrapeBookRepositoryImpl
from src.infrastructure.standard.app_log.AppLoggerImpl import AppLoggerImpl


class TestAppBuilder:
    _app_builder: AppBuilder

    @pytest.fixture(autouse=True)
    def setup_teardown(self) -> Iterator[None]:
        self._app_builder = AppBuilder()
        yield

    def test_validate_app_logger(self) -> None:
        # arrange - act
        instance_1 = self._app_builder.app_logger
        instance_2 = self._app_builder.app_logger

        # assert
        assert isinstance(self._app_builder.app_logger, AppLoggerImpl)
        assert instance_1 == instance_2

    def test_validate_http_client_factory(self) -> None:
        # arrange - act
        instance_1 = self._app_builder.http_client_factory
        instance_2 = self._app_builder.http_client_factory

        # assert
        assert isinstance(self._app_builder.http_client_factory, HttpClientFactoryImpl)
        assert instance_1 == instance_2

    def test_validate_scrape_book_repository(self) -> None:
        # arrange - act
        instance_1 = self._app_builder.scrape_book_repository
        instance_2 = self._app_builder.scrape_book_repository

        # assert
        assert isinstance(self._app_builder.scrape_book_repository, ScrapeBookRepositoryImpl)
        assert instance_1 == instance_2

    def test_use_caser_manager(self) -> None:
        # arrange - act
        instance_1 = self._app_builder.use_caser_manager
        instance_2 = self._app_builder.use_caser_manager

        # assert
        assert isinstance(self._app_builder.use_caser_manager, UseCaseManagerImpl)
        assert instance_1 == instance_2

    def test_controllers(self) -> None:
        # arrange - act
        instance_1 = self._app_builder.controllers
        instance_2 = self._app_builder.controllers

        # assert
        assert isinstance(self._app_builder.controllers, dict)
        assert instance_1 == instance_2

        # v1-controllers
        v1_controllers = self._app_builder.controllers[AppBuilder.V1_CONTROLLERS]
        assert isinstance(v1_controllers[0], HealthController)

    def test_fast_api(self) -> None:
        # arrange - act
        instance_1 = self._app_builder.fast_api
        instance_2 = self._app_builder.fast_api

        # assert
        assert isinstance(self._app_builder.fast_api, FastAPI)
        assert instance_1 == instance_2

    def test_script_scrape_books(self) -> None:
        # arrange - act
        instance_1: Callable[[], Coroutine[Any, Any, None]] = self._app_builder.script_scrape_books
        instance_2: Callable[[], Coroutine[Any, Any, None]] = self._app_builder.script_scrape_books

        # assert
        assert isinstance(self._app_builder.fast_api, Callable)  # type: ignore
        assert inspect.iscoroutinefunction(instance_1)
        assert instance_1 != instance_2
