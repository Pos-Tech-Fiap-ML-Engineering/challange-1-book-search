from dataclasses import dataclass
from typing import Any

from src.standard.error.ApplicationErrorCode import ApplicationErrorCode


@dataclass
class ApplicationErrorInfo:
    code: ApplicationErrorCode
    message: str
    cause: Any | None
    error: Exception | None
