from __future__ import annotations

from abc import abstractmethod
from typing import Dict, ContextManager

from src.standard.built_in.Abstract import Abstract


class AppLogger(Abstract):
    @abstractmethod
    def debug(self, message: str, extra: Dict[str, str]) -> None:
        pass

    @abstractmethod
    def info(self, message: str, extra: Dict[str, str]) -> None:
        pass

    @abstractmethod
    def warn(self, message: str, extra: Dict[str, str]) -> None:
        pass

    @abstractmethod
    def error(self, message: str, extra: Dict[str, str]) -> None:
        pass

    @abstractmethod
    def new_scope(self, scope_name: str, extra: Dict[str, str]) -> ContextManager[None]:
        pass
