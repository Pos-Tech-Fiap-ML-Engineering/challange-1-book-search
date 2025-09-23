from fastapi import APIRouter

from src.api.controllers.abstractions.BaseController import BaseController


class Router:
    _router: APIRouter = APIRouter(prefix="/api")

    @classmethod
    def get_router(cls, v1_controllers: list[BaseController]) -> APIRouter:
        for controller in v1_controllers:
            cls._router.include_router(controller.get_router(), prefix="/v1")

        return cls._router
