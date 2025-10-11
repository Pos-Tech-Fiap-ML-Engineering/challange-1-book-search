from __future__ import annotations

import logging
from logging import Logger

from src.infrastructure.standard.app_log.SetupAppLogger import SetupAppLogger


class TestSetupAppLogger:
    def test_uvicorn_and_gunicorn_loggers_levels_and_propagation(self) -> None:
        # arrange
        SetupAppLogger.setup_logging(level="INFO")

        # act
        uvicorn: Logger = logging.getLogger("uvicorn")
        uvicorn_err: Logger = logging.getLogger("uvicorn.error")
        uvicorn_access: Logger = logging.getLogger("uvicorn.access")
        gunicorn: Logger = logging.getLogger("gunicorn")
        gunicorn_err: Logger = logging.getLogger("gunicorn.error")
        gunicorn_access: Logger = logging.getLogger("gunicorn.access")

        # assert
        assert uvicorn.level == logging.INFO
        assert uvicorn_err.level == logging.INFO
        assert uvicorn_access.level == logging.WARNING

        assert gunicorn.level == logging.INFO
        assert gunicorn_err.level == logging.INFO
        assert gunicorn_access.level == logging.WARNING

        assert uvicorn.propagate is False
        assert uvicorn_err.propagate is False
        assert uvicorn_access.propagate is False
        assert gunicorn.propagate is False
        assert gunicorn_err.propagate is False
        assert gunicorn_access.propagate is False

    def test_custom_level_debug(self) -> None:
        # arrange
        SetupAppLogger.setup_logging(level="DEBUG")

        # act
        root: Logger = logging.getLogger()

        # assert
        assert root.level == logging.DEBUG
