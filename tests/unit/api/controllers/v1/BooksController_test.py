import json
from typing import Iterator, Any, Tuple, cast
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from src.api.controllers.v1.BooksController import BooksController
from src.api.presenters.ListAllBooksUseCaseOutputPresenterImpl import ListAllBooksUseCaseOutputPresenterImpl
from src.api.schemas.output.BookOutput import BookOutput
from src.application.use_cases.book.list_all_books.ListAllBooksUseCaseInput import ListAllBooksUseCaseInput
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker
from tests.assets.mocks.UseCaseManagerMock import UseCaseManagerMock


class TestBooksController:
    _use_case_manager_mock: Mock
    _controller: BooksController

    @pytest.fixture(autouse=True)
    def setup_teardown(self, mocker: MockerFixture) -> Iterator[None]:
        self._use_case_manager_mock = UseCaseManagerMock.create(mocker)
        self._controller = BooksController(self._use_case_manager_mock)

        yield

    def test_router_path(self) -> None:
        # arrange - act - assert
        assert getattr(self._controller, "_router", None) is not None

    async def test_list_all_books_successfully(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        expected_result = BookOutput.to_output_list_json(books)

        def a(*args: Tuple[Any], **kwargs: dict[str, Any]) -> None:
            cast(ListAllBooksUseCaseOutputPresenterImpl, cast(object, args[1])).success(books)

        self._use_case_manager_mock.execute_async.side_effect = a

        # act
        result = await self._controller.list_all_books_async()

        router = self._controller.get_router()

        # assert
        assert result.status_code == 200
        assert json.loads(result.body.decode("utf-8")) == expected_result  # type: ignore
        assert router.prefix == "/books"

        assert self._use_case_manager_mock.execute_async.call_count == 1
        called_args, called_kwargs = self._use_case_manager_mock.execute_async.call_args_list[0]
        assert isinstance(called_args[0], ListAllBooksUseCaseInput)
        assert isinstance(called_args[1], ListAllBooksUseCaseOutputPresenterImpl)
        assert called_kwargs == {'meta_information': None}
