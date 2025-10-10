import abc

from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler


class ListCategoriesUseCaseOutputHandler(UseCaseOutputHandler):
    @abc.abstractmethod
    def success(self, categories: set[str]) -> None:
        pass
