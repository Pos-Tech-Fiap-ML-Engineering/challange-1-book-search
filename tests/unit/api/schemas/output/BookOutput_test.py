import pytest

from src.api.schemas.output.BookOutput import BookOutput
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker


class TestBookOutput:
    def test_to_output_list_should_return_list_of_book_outputs(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        # act
        outputs = BookOutput.to_output_list(books)

        # assert
        assert isinstance(outputs, list)
        assert len(outputs) == 2
        assert all(isinstance(b, BookOutput) for b in outputs)
        assert outputs[0].id == books[0].id
        assert outputs[1].id == books[1].id
        assert outputs[0].category == books[0].category

    def test_to_output_list_json_should_return_serializable_dicts(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())

        # act
        json_outputs = BookOutput.to_output_list_json(books)

        # assert
        assert isinstance(json_outputs, list)
        assert len(json_outputs) == 1
        data = json_outputs[0]

        assert isinstance(data, dict)
        assert data["id"] == books[0].id
        assert data["category"] == books[0].category
        assert data["price_full"] == str(books[0].price_full)
        assert data["price_excl_tax"] == str(books[0].price_excl_tax)
        assert data["tax"] == str(books[0].tax)

    def test_to_output_list_with_empty_collection_should_return_empty_list(self) -> None:
        # arrange
        books = ScrapeBooks()

        # act
        outputs = BookOutput.to_output_list(books)
        json_outputs = BookOutput.to_output_list_json(books)

        # assert
        assert outputs == []
        assert json_outputs == []

    def test_to_output_list_should_raise_if_dict_missing_required_field(self) -> None:
        # arrange
        books = ScrapeBooks()
        book = ScrapeBookFaker.fake()
        books.append(book)

        # act - assert
        def broken_to_dict() -> dict:
            data = book.to_dict()
            del data["title"]
            return data

        book.to_dict = broken_to_dict  # type: ignore

        with pytest.raises(Exception):
            BookOutput.to_output_list(books)
