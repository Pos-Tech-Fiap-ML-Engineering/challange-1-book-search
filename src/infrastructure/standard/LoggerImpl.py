from __future__ import annotations

import contextvars
import logging
import uuid
from dataclasses import dataclass, field

from logging import Logger
from contextlib import contextmanager
from typing import Dict, Iterator, Optional, cast

from src.standard.app_log.AppLogger import AppLogger


@dataclass
class _LogEntry:
    logger: Logger
    scope_id: Optional[str] = None
    scope_name: Optional[str] = None
    extra_attrs: Optional[Dict[str, str]] = field(default_factory=dict)


class AppLoggerImpl(AppLogger):

    def __init__(self, logger: Logger) -> None:
        self._logger_manager: contextvars.ContextVar[_LogEntry] = (
            contextvars.ContextVar(AppLoggerImpl.__name__, default=_LogEntry(logger=logger))
        )

    def debug(self, message: str, extra: Optional[Dict[str, str]]) -> None:
        self._generate_log(logging.DEBUG, message, extra)

    def info(self, message: str, extra: Optional[Dict[str, str]]) -> None:
        self._generate_log(logging.INFO, message, extra)

    def warn(self, message: str, extra: Optional[Dict[str, str]]) -> None:
        self._generate_log(logging.WARN, message, extra)

    def error(self, message: str, extra: Optional[Dict[str, str]]) -> None:
        self._generate_log(logging.ERROR, message, extra)

    def _generate_log(self, level: int, message: str, extra: Optional[Dict[str, str]]) -> None:
        current_log_entry = self._logger_manager.get()

        current_attr = extra or {}
        extra_attrs = current_log_entry.extra_attrs or {}
        merged_extra_attrs = {**extra_attrs, **current_attr}

        if current_log_entry.scope_id is not None:
            merged_extra_attrs[cast(str, current_log_entry.scope_name)] = current_log_entry.scope_id

        current_log_entry.logger.log(level, message, extra=merged_extra_attrs)

    @contextmanager
    def new_scope(self, scope_name: str, extra: Optional[Dict[str, str]]) -> Iterator[None]:
        current_logger = self._logger_manager.get().logger.getChild(scope_name)
        scope_id = self._generate_hash()
        scope_name = f"{scope_name}-{scope_id}"

        token = self._logger_manager.set(
            _LogEntry(logger=current_logger, scope_id=scope_id, scope_name=scope_name, extra_attrs=extra))

        try:
            yield
        finally:
            self._logger_manager.reset(token)

    @staticmethod
    def _generate_hash() -> str:
        return uuid.uuid4().hex[:8]
