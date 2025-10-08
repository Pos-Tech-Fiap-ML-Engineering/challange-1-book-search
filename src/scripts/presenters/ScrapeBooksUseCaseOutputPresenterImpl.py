from src.application.use_cases.book.scrape_books.ScrapeBooksUseCaseOutputHandler import (
    ScrapeBooksUseCaseOutputHandler,
)
from src.scripts.presenters.base.BasePresenter import BasePresenter


class ScrapeBooksUseCaseOutputPresenterImpl(BasePresenter, ScrapeBooksUseCaseOutputHandler):

    def __init__(self) -> None:
        super().__init__()

    def success(self) -> None:
        async def _f() -> None: ...

        self._response_func = _f

    def failed_to_load_site(self) -> None:
        async def _f() -> None:
            raise Exception("Failed to load site")

        self._response_func = _f

    def failed_to_load_link(self, link: str) -> None:
        async def _f() -> None:
            raise Exception(f"Failed to load link: {link}")

        self._response_func = _f
