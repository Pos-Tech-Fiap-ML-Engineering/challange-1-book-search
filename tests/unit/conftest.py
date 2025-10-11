import logging
from collections.abc import Iterator

import pytest
from _pytest.monkeypatch import MonkeyPatch

from src.domain.scrape_book.ScrapeBook import ScrapeBook

@pytest.fixture(scope="function",autouse=True)
def _reset_logging() -> Iterator[None]:

    yield

    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    for name in list(logging.Logger.manager.loggerDict.keys()):
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.setLevel(logging.NOTSET)
        logger.propagate = True

@pytest.fixture(scope="function", autouse=True)
def _global_setup_teardown(monkeypatch: MonkeyPatch) -> Iterator[None]:
    monkeypatch.setattr(ScrapeBook, "_id_seq", 0)

    yield
