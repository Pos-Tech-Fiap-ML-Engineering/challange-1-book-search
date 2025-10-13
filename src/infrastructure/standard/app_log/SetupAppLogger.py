from logging.config import dictConfig

from src.infrastructure.standard.app_log.filters.DropLoggingFilter import DropLoggingFilter
from src.standard.built_in.Static import Static


class SetupAppLogger(Static):
    @staticmethod
    def setup_logging(level: str = "INFO") -> None:
        dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "plain": {"format": "%(asctime)s %(levelname)s %(name)s - %(message)s"}
                },
                "filters": {"drop_health": {"()": DropLoggingFilter}},
                "handlers": {
                    "default": {
                        "class": "logging.StreamHandler",
                        "formatter": "plain",
                        "filters": ["drop_health"],
                        "stream": "ext://sys.stdout",
                    }
                },
                "root": {
                    "level": level,
                    "handlers": ["default"],
                },
                "loggers": {
                    "uvicorn": {"level": level, "handlers": ["default"], "propagate": False},
                    "uvicorn.error": {"level": level, "handlers": ["default"], "propagate": False},
                    "uvicorn.access": {
                        "level": "WARNING",
                        "handlers": ["default"],
                        "propagate": False,
                    },
                    "gunicorn": {"level": level, "handlers": ["default"], "propagate": False},
                    "gunicorn.error": {"level": level, "handlers": ["default"], "propagate": False},
                    "gunicorn.access": {
                        "level": "WARNING",
                        "handlers": ["default"],
                        "propagate": False,
                    },
                },
            }
        )
