import pytest

from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository
from src.standard.built_in.Abstract import Abstract


class TestScrapeBookRepository:
    def test_class_is_subclass_abstract(self) -> None:
        # arrange - act - assert
        assert issubclass(ScrapeBookRepository, Abstract)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            ScrapeBookRepository()  # type: ignore
