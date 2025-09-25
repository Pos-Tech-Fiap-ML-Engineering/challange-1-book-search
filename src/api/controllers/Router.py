from fastapi import APIRouter

from src.api.controllers.abstractions.BaseController import BaseController
from src.standard.built_in.Static import Static


class Router(Static):
    @staticmethod
    def get_router(*, base_router: APIRouter, v1_controllers: list[BaseController]) -> APIRouter:
        base_router.prefix = "/api"
        for controller in v1_controllers:
            base_router.include_router(controller.get_router(), prefix="/v1")

        return base_router
