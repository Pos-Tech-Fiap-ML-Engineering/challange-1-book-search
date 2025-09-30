from collections.abc import Iterator

import httpx
import pytest


class TestHealthCheck:
    _http_client: httpx.AsyncClient

    @pytest.fixture(autouse=True)
    def setup_teardown(self, http_client: httpx.AsyncClient) -> Iterator[None]:
        self._http_client = http_client
        yield

    async def test_health_check_successfully(self) -> None:
        # arrange - act
        result = await self._http_client.get("/api/v1/health")

        # assert
        assert result.status_code == 200
