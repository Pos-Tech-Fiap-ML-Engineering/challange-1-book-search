from fastapi.responses import JSONResponse

from src.api.presenters.base.BasePresenter import BasePresenter
from src.application.use_cases.category.list_categories.ListCategoriesUseCaseOutputHandler import \
    ListCategoriesUseCaseOutputHandler


class ListCategoriesUseCaseOutputPresenterImpl(BasePresenter, ListCategoriesUseCaseOutputHandler):
    def success(self, result: set[str]) -> None:
        parsed_to_list_result = list(result)
        self._set_result(JSONResponse(status_code=200,
                                      content=parsed_to_list_result))
