from fastapi import APIRouter

from src.api.controllers.abstractions.BaseController import BaseController
from src.api.schemas.output.HealthCheckOutput import HealthCheckOutput


class HealthController(BaseController):
    _router: APIRouter = APIRouter(prefix="/health", tags=["health"])

    def __init__(self) -> None:
        self._router.add_api_route(
            path="",
            endpoint=self.get_health_async,
            methods=["GET"],
            response_model=HealthCheckOutput,
            summary="Get Health",
        )

    async def get_health_async(self) -> HealthCheckOutput:
        return HealthCheckOutput(result=True)
