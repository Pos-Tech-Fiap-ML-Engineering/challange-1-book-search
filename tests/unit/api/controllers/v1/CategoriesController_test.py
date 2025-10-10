import json

from typing import Iterator, cast, Tuple, Any
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from src.api.controllers.v1.CategoriesController import CategoriesController
from src.api.presenters.ListCategoriesUseCaseOutputPresenterImpl import ListCategoriesUseCaseOutputPresenterImpl
from src.application.use_cases.category.list_categories.ListCategoriesUseCaseInput import ListCategoriesUseCaseInput
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker
from tests.assets.mocks.UseCaseManagerMock import UseCaseManagerMock


class TestCategoriesController:
    _use_case_manager_mock: Mock
    _controller: CategoriesController

    @pytest.fixture(autouse=True)
    def setup_teardown(self, mocker: MockerFixture) -> Iterator[None]:
        self._use_case_manager_mock = UseCaseManagerMock.create(mocker)
        self._controller = CategoriesController(self._use_case_manager_mock)

        yield

    async def test_list_all_categories_successfully(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        expected_result = list(books.categories)

        def a(*args: Tuple[Any], **kwargs: dict[str, Any]) -> None:
            cast(ListCategoriesUseCaseOutputPresenterImpl, cast(object, args[1])).success(books.categories)

        self._use_case_manager_mock.execute_async.side_effect = a

        # act
        result = await self._controller.list_all_categories_async()

        router = self._controller.get_router()

        # assert
        assert result.status_code == 200
        assert json.loads(result.body.decode("utf-8")) == expected_result  # type: ignore
        assert router.prefix == "/categories"

        assert self._use_case_manager_mock.execute_async.call_count == 1
        called_args, called_kwargs = self._use_case_manager_mock.execute_async.call_args_list[0]
        assert isinstance(called_args[0], ListCategoriesUseCaseInput)
        assert isinstance(called_args[1], ListCategoriesUseCaseOutputPresenterImpl)
        assert called_kwargs == {'meta_information': None}
