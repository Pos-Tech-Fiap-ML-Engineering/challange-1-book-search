from fastapi import APIRouter

from src.standard.built_in.Abstract import Abstract


class BaseController(Abstract):
    _router: APIRouter = APIRouter()

    def get_router(self) -> APIRouter:
        return self._router
