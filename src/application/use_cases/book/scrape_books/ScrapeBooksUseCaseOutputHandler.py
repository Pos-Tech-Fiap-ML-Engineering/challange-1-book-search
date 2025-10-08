import abc

from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler


class ScrapeBooksUseCaseOutputHandler(UseCaseOutputHandler):
    @abc.abstractmethod
    def success(self) -> None:
        pass

    @abc.abstractmethod
    def failed_to_load_site(self) -> None:
        pass

    @abc.abstractmethod
    def failed_to_load_link(self, link: str) -> None:
        pass
