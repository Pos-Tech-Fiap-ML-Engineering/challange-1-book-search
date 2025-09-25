from typing import Iterator

import pytest

from src.api.controllers.v1.HealthController import HealthController
from src.api.schemas.output.HealthCheckOutput import HealthCheckOutput


class TestHealthController:
    _controller: HealthController

    @pytest.fixture(autouse=True)
    def setup_teardown(self) -> Iterator[None]:
        self._controller = HealthController()

        yield

    def test_router_path(self) -> None:
        # arrange - act - assert
        assert getattr(self._controller, '_router') is not None

    async def test_get_health_async(self) -> None:
        # arrange
        expected_result_health: HealthCheckOutput = HealthCheckOutput(result=True)

        # act
        result = await self._controller.get_health_async()

        router = self._controller.get_router()

        # assert
        assert result == expected_result_health
        assert router.prefix == "/health"
