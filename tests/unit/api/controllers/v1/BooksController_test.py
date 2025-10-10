import json
from typing import Iterator, Any, Tuple, cast
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from src.api.controllers.v1.BooksController import BooksController
from src.api.presenters.GetBookByIdUseCaseOutputPresenterImpl import GetBookByIdUseCaseOutputPresenterImpl
from src.api.presenters.ListAllBooksUseCaseOutputPresenterImpl import ListAllBooksUseCaseOutputPresenterImpl
from src.api.presenters.ListBooksByCategoryTitleUseCaseOutputPresenterImpl import \
    ListBooksByCategoryTitleUseCaseOutputPresenterImpl
from src.api.presenters.ListTopRatedBooksUseCaseOutputPresenterImpl import ListTopRatedBooksUseCaseOutputPresenterImpl
from src.api.schemas.output.BookOutput import BookOutput
from src.application.use_cases.book.get_book_by_id.GetBookByIdUseCaseInput import GetBookByIdUseCaseInput
from src.application.use_cases.book.list_all_books.ListAllBooksUseCaseInput import ListAllBooksUseCaseInput
from src.application.use_cases.book.list_books_by_title_category.ListBooksByCategoryTitleUseCaseInput import \
    ListBooksByCategoryTitleUseCaseInput
from src.application.use_cases.book.list_top_rated_books.ListTopRatedBooksUseCaseInput import \
    ListTopRatedBooksUseCaseInput
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

    async def test_list_books_by_title_and_category_successfully(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        expected_result = BookOutput.to_output_list_json(books)

        def a(*args: Tuple[Any], **kwargs: dict[str, Any]) -> None:
            cast(ListBooksByCategoryTitleUseCaseOutputPresenterImpl, cast(object, args[1])).success(books)

        self._use_case_manager_mock.execute_async.side_effect = a

        # act
        result = await self._controller.list_books_by_title_or_category_async()

        router = self._controller.get_router()

        # assert
        assert result.status_code == 200
        assert json.loads(result.body.decode("utf-8")) == expected_result  # type: ignore
        assert router.prefix == "/books"

        assert self._use_case_manager_mock.execute_async.call_count == 1
        called_args, called_kwargs = self._use_case_manager_mock.execute_async.call_args_list[0]
        assert isinstance(called_args[0], ListBooksByCategoryTitleUseCaseInput)
        assert isinstance(called_args[1], ListBooksByCategoryTitleUseCaseOutputPresenterImpl)
        assert called_kwargs == {'meta_information': None}

    async def test_list_top_rated_books_successfully(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        expected_result = BookOutput.to_output_list_json(books)

        def a(*args: Tuple[Any], **kwargs: dict[str, Any]) -> None:
            cast(ListTopRatedBooksUseCaseOutputPresenterImpl, cast(object, args[1])).success(books)

        self._use_case_manager_mock.execute_async.side_effect = a

        # act
        result = await self._controller.list_top_rated_books_async()

        router = self._controller.get_router()

        # assert
        assert result.status_code == 200
        assert json.loads(result.body.decode("utf-8")) == expected_result  # type: ignore
        assert router.prefix == "/books"

        assert self._use_case_manager_mock.execute_async.call_count == 1
        called_args, called_kwargs = self._use_case_manager_mock.execute_async.call_args_list[0]
        assert isinstance(called_args[0], ListTopRatedBooksUseCaseInput)
        assert isinstance(called_args[1], ListTopRatedBooksUseCaseOutputPresenterImpl)
        assert called_kwargs == {'meta_information': None}

    async def test_get_book_by_id_successfully(self) -> None:
        # arrange
        book = ScrapeBookFaker.fake()

        expected_result = BookOutput.to_output_json(book)

        def a(*args: Tuple[Any], **kwargs: dict[str, Any]) -> None:
            cast(GetBookByIdUseCaseOutputPresenterImpl, cast(object, args[1])).success(book)

        self._use_case_manager_mock.execute_async.side_effect = a

        # act
        result = await self._controller.get_book_by_id_async(book.id)

        router = self._controller.get_router()

        # assert
        assert result.status_code == 200
        assert json.loads(result.body.decode("utf-8")) == expected_result  # type: ignore
        assert router.prefix == "/books"

        assert self._use_case_manager_mock.execute_async.call_count == 1
        called_args, called_kwargs = self._use_case_manager_mock.execute_async.call_args_list[0]
        assert isinstance(called_args[0], GetBookByIdUseCaseInput)
        assert isinstance(called_args[1], GetBookByIdUseCaseOutputPresenterImpl)
        assert called_kwargs == {'meta_information': {'book_id': str(book.id)}}
