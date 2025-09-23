from pydantic import BaseModel


class HealthCheckOutput(BaseModel):
    result: bool
