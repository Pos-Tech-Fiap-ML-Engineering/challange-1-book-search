from __future__ import annotations

from abc import abstractmethod
from typing import Dict, ContextManager, Optional

from src.standard.built_in.Abstract import Abstract


class AppLogger(Abstract):
    @abstractmethod
    def debug(self, message: str, extra: Optional[Dict[str, str]] = None) -> None:
        pass

    @abstractmethod
    def info(self, message: str, extra: Optional[Dict[str, str]] = None) -> None:
        pass

    @abstractmethod
    def warn(self, message: str, extra: Optional[Dict[str, str]] = None) -> None:
        pass

    @abstractmethod
    def error(self, message: str, extra: Optional[Dict[str, str]] = None, exc_info: Optional[Exception] = None) -> None:
        pass

    @abstractmethod
    def new_scope(self, scope_name: str, extra: Optional[Dict[str, str]] = None) -> ContextManager[None]:
        pass
