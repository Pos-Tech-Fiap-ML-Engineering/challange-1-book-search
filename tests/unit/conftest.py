from collections.abc import Iterator

import pytest
from _pytest.monkeypatch import MonkeyPatch

from src.domain.scrape_book.ScrapeBook import ScrapeBook


@pytest.fixture(scope="function", autouse=True)
def global_setup_teardown(monkeypatch: MonkeyPatch) -> Iterator[None]:
    monkeypatch.setattr(ScrapeBook, "_id_seq", 0)

    yield
