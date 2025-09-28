from __future__ import annotations

import contextvars
import logging
import uuid
from dataclasses import dataclass, field

from logging import Logger
from contextlib import contextmanager
from collections.abc import Iterator

from src.standard.app_log.AppLogger import AppLogger


@dataclass
class _LogEntry:
    logger: Logger
    extra_attrs: dict[str, str] | None = field(default_factory=dict)


class AppLoggerImpl(AppLogger):

    def __init__(self, logger: Logger) -> None:
        self._logger_manager: contextvars.ContextVar[_LogEntry] = contextvars.ContextVar(
            AppLoggerImpl.__name__
        )
        self._logger_manager.set(_LogEntry(logger=logger))

    def debug(self, message: str, extra: dict[str, str] | None = None) -> None:
        self._generate_log(logging.DEBUG, message, extra, None)

    def info(self, message: str, extra: dict[str, str] | None = None) -> None:
        self._generate_log(logging.INFO, message, extra, None)

    def warn(self, message: str, extra: dict[str, str] | None = None) -> None:
        self._generate_log(logging.WARN, message, extra, None)

    def error(
        self, message: str, extra: dict[str, str] | None = None, exc_info: Exception | None = None
    ) -> None:
        self._generate_log(logging.ERROR, message, extra, exc_info)

    @contextmanager
    def new_scope(self, scope_name: str, extra: dict[str, str] | None = None) -> Iterator[None]:
        current_log_entry = self._logger_manager.get()
        current_logger = current_log_entry.logger.getChild(scope_name)
        scope_id = self._generate_hash()
        scope_name = f"{scope_name}-{scope_id}"

        merged_extra_attrs = {
            scope_name: scope_id,
            **(current_log_entry.extra_attrs or {}),
            **(extra or {}),
        }

        token = self._logger_manager.set(
            _LogEntry(logger=current_logger, extra_attrs=merged_extra_attrs)
        )

        try:
            yield
        finally:
            self._logger_manager.reset(token)

    def _generate_log(
        self, level: int, message: str, extra: dict[str, str] | None, exc_info: Exception | None
    ) -> None:
        current_log_entry = self._logger_manager.get()

        current_attr = extra or {}
        extra_attrs = current_log_entry.extra_attrs or {}
        merged_extra_attrs = {**extra_attrs, **current_attr}

        current_log_entry.logger.log(level, message, extra=merged_extra_attrs, exc_info=exc_info)

    @staticmethod
    def _generate_hash() -> str:
        return uuid.uuid4().hex[:8]
