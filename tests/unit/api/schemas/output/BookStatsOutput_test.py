import json

from decimal import Decimal

from src.api.schemas.output.BookStatsOutput import BookStatsOutput
from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker


class TestBookStatsOutput:
    def test_to_output_returns_pydantic_model(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        book_stats = books.get_stats_books()

        # act
        model = BookStatsOutput.to_output(book_stats)

        # assert
        assert isinstance(model, BookStatsOutput)
        assert model.total_books == book_stats.total_books
        assert isinstance(model.avg_price, Decimal)
        assert model.avg_price == book_stats.avg_price
        assert model.rating_distribution == book_stats.rating_distribution
        assert all(isinstance(k, int) for k in model.rating_distribution)

    def test_to_output_json_returns_plain_dict_json_safe(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        book_stats = books.get_stats_books()

        # act
        data = BookStatsOutput.to_output_json(book_stats)

        # assert
        rating_distribution_expected = {
            str(k): v for k, v in book_stats.rating_distribution.items()
        }

        assert isinstance(data, dict)
        assert data["total_books"] == book_stats.total_books

        assert data["avg_price"] == str(book_stats.avg_price)
        assert isinstance(data["avg_price"], str)

        assert data["rating_distribution"] == rating_distribution_expected
        assert all(isinstance(k, str) for k in data["rating_distribution"])

    def test_to_output_json_is_dumpable_with_stdlib_json(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        book_stats = books.get_stats_books()

        # act
        data = BookStatsOutput.to_output_json(book_stats)

        dumped = json.dumps(data)

        # assert
        assert isinstance(dumped, str)
        # sanity check de conteúdo mínimo
        assert '"total_books"' in dumped
        assert '"avg_price"' in dumped

    def test_to_output_and_json_are_consistent(self) -> None:
        # arrange
        books = ScrapeBooks()
        book_stats = books.get_stats_books()

        # act
        model = BookStatsOutput.to_output(book_stats)

        # assert
        expected = model.model_dump(mode="json")
        actual = BookStatsOutput.to_output_json(book_stats)
        assert actual == expected
