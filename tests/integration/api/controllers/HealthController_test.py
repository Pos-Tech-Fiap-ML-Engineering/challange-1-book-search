from collections.abc import Iterator

import pytest
from httpx import AsyncClient

from src.api.schemas.output.HealthCheckOutput import HealthCheckOutput


class TestHealthController:
    _http_client: AsyncClient

    @pytest.fixture(autouse=True)
    def setup_teardown(self, http_client: AsyncClient) -> Iterator[None]:
        self._http_client = http_client

        yield

    async def test_health_check_successfully(self) -> None:
        # arrange
        expected_result_health: HealthCheckOutput = HealthCheckOutput(result=True)

        # act
        result = await self._http_client.get("/api/v1/health")

        # assert
        assert result.status_code == 200
        assert result.json() == expected_result_health.model_dump()
