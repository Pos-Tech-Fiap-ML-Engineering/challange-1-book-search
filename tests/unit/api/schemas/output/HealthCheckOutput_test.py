from pydantic import BaseModel

from src.api.schemas.output.HealthCheckOutput import HealthCheckOutput


class TestHealthCheckOutput:
    def test_class_is_subclass_base_model(self) -> None:
        # arrange - act - assert
        assert issubclass(HealthCheckOutput, BaseModel)

    def test_class_can_be_instantiated(self) -> None:
        # arrange - act - assert
        HealthCheckOutput(result=True)
