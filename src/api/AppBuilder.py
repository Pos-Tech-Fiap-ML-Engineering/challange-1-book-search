from fastapi import FastAPI

import logging

from typing import Dict, List

from src.api.controllers.Router import Router
from src.api.controllers.abstractions.BaseController import BaseController
from src.api.controllers.v1.HealthController import HealthController
from src.application.boundaries.use_case.UseCaseManager import UseCaseManager
from src.infrastructure.application.boundaries.use_case.UseCaseManagerImpl import UseCaseManagerImpl
from src.infrastructure.standard.app_log.AppLoggerImpl import AppLoggerImpl
from src.standard.app_log.AppLogger import AppLogger

V1_CONTROLLERS = 'v1'


class AppBuilder:
    _app_logger: AppLogger
    _use_caser_manager: UseCaseManager
    _controllers: Dict[str, List[BaseController]]

    def __init__(self) -> None:
        self._app_logger = self._load_app_logger()
        self._use_caser_manager = self._load_use_caser_manager()
        self._controllers = self._load_controllers()

    def _load_app_logger(self) -> AppLogger:
        logger = logging.getLogger("app")
        app_logger = AppLoggerImpl(logger=logger)
        return app_logger

    def _load_use_caser_manager(self) -> UseCaseManager:
        use_caser_manager = UseCaseManagerImpl(logger=self._app_logger,
                                               use_cases=[])

        return use_caser_manager

    def _load_controllers(self) -> Dict[str, List[BaseController]]:
        return {
            V1_CONTROLLERS: [
                HealthController(),
            ]
        }

    def build_fast_api_server(self) -> FastAPI:
        app = FastAPI(
            title="Book Search",
            version="1.0.0",
            openapi_url="/openapi.json",
            docs_url="/docs",
            redoc_url="/redoc",
        )

        routers = Router.get_router(
            v1_controllers=self._controllers[V1_CONTROLLERS],
        )
        app.include_router(routers)

        return app
