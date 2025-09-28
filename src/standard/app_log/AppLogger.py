from __future__ import annotations

from abc import abstractmethod
from contextlib import AbstractContextManager

from src.standard.built_in.Abstract import Abstract


class AppLogger(Abstract):

    @abstractmethod
    def debug(self, message: str, extra: dict[str, str] | None = None) -> None:
        pass

    @abstractmethod
    def info(self, message: str, extra: dict[str, str] | None = None) -> None:
        pass

    @abstractmethod
    def warn(self, message: str, extra: dict[str, str] | None = None) -> None:
        pass

    @abstractmethod
    def error(
        self, message: str, extra: dict[str, str] | None = None, exc_info: Exception | None = None
    ) -> None:
        pass

    @abstractmethod
    def new_scope(
        self, scope_name: str, extra: dict[str, str] | None = None
    ) -> AbstractContextManager[None]:
        pass
