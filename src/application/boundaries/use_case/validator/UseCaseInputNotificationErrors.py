from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Self


@dataclass
class UseCaseInputNotificationErrors:

    def __init__(self) -> None:
        self._error_messages: Dict[str, List[str]] = field(default_factory=dict, init=False)
        self._has_errors: bool = field(default=False, init=False)

    @property
    def has_errors(self) -> bool:
        return self._has_errors

    @property
    def errors(self) -> Dict[str, List[str]]:
        return self._error_messages.copy()

    def add(self, key: str, message: str) -> None:
        self._has_errors = True
        self._error_messages.setdefault(key, []).append(message)

    @classmethod
    def empty(cls) -> Self:
        return cls()
