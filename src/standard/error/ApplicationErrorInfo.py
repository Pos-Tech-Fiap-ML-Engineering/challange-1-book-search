from dataclasses import dataclass
from typing import Optional, Any

from src.standard.error.ApplicationErrorCode import ApplicationErrorCode


@dataclass
class ApplicationErrorInfo:
    code: ApplicationErrorCode
    message: str
    cause: Optional[Any]
    error: Optional[Exception]
