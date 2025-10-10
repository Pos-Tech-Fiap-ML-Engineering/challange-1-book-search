from src.application.boundaries.use_case.input.UseCaseInput import UseCaseInput
from src.application.use_cases.category.list_categories.ListCategoriesUseCaseInput import ListCategoriesUseCaseInput


class TestListCategoriesUseCaseInput:
    def test_class_is_subclass_input(self) -> None:
        # arrange - act - assert
        assert issubclass(ListCategoriesUseCaseInput, UseCaseInput)

    def test_class_initialized_successfully(self) -> None:
        # arrange - act - assert
        ListCategoriesUseCaseInput()