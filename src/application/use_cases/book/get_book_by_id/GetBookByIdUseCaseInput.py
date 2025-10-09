from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.application.boundaries.use_case.validator.UseCaseInputNotificationErrors import UseCaseInputNotificationErrors


class GetBookByIdUseCaseInput(UseCaseInput):
    def __init__(self, book_id: int) -> None:
        self._id = book_id

    @property
    def id(self) -> int:
        return self._id

    def validate_input(self, errors: UseCaseInputNotificationErrors) -> None:
        if self.id is None or self.id < 0:
            errors.add("id", "id cannot be None or negative")