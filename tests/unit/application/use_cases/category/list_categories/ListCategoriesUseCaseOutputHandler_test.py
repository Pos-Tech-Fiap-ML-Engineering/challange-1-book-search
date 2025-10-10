import pytest

from src.application.boundaries.use_case.output.UseCaseOutputHandler import UseCaseOutputHandler
from src.application.use_cases.category.list_categories.ListCategoriesUseCaseOutputHandler import (
    ListCategoriesUseCaseOutputHandler,
)


class TestListCategoriesUseCaseOutputHandler:
    def test_class_is_subclass_useCase_output_handler(self) -> None:
        # arrange - act - assert
        assert issubclass(ListCategoriesUseCaseOutputHandler, UseCaseOutputHandler)

    def test_class_can_not_be_instantiated(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            ListCategoriesUseCaseOutputHandler()  # type: ignore
