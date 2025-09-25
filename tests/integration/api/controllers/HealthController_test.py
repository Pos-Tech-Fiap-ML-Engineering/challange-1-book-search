from httpx import AsyncClient

from src.api.schemas.output.HealthCheckOutput import HealthCheckOutput


class TestHealthController:

    async def test_health_check_successfully(self, http_client: AsyncClient) -> None:
        # arrange
        expected_result_health: HealthCheckOutput = HealthCheckOutput(result=True)

        # act
        result = await http_client.get("/api/v1/health")

        # assert
        assert result.status_code == 200
        assert result.json() == expected_result_health.model_dump()
