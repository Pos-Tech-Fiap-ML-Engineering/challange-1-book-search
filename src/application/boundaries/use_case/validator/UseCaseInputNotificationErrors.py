from __future__ import annotations

from typing import Self


class UseCaseInputNotificationErrors:

    def __init__(self) -> None:
        self._error_messages: dict[str, list[str]] = {}
        self._has_errors: bool = False

    @property
    def has_errors(self) -> bool:
        return self._has_errors

    @property
    def errors(self) -> dict[str, list[str]]:
        return self._error_messages.copy()

    @property
    def flatten_errors(self) -> dict[str, str]:
        errors = self.errors
        return {
            f"{key}_{i}": v for key, values in errors.items() for i, v in enumerate(values, start=1)
        }

    def add(self, key: str, message: str) -> None:
        self._has_errors = True
        self._error_messages.setdefault(key, []).append(message)

    @classmethod
    def empty(cls) -> Self:
        return cls()
