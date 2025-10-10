from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput


class ListBooksByCategoryTitleUseCaseInput(UseCaseInput):
    def __init__(self, title: str | None = None, category: str | None = None) -> None:
        self._title = title
        self._category = category

    @property
    def title(self) -> str | None:
        return self._title

    @property
    def category(self) -> str | None:
        return self._category