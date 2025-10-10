from __future__ import annotations

from decimal import Decimal
from typing import Any, cast

import pytest

from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
from src.domain.scrape_book.vos.BookStats import BookStats
from src.domain.scrape_book.vos.Money import Money
from src.domain.scrape_book.vos.Rating import Rating
from tests.assets.fakers.ScrapeBookFaker import ScrapeBookFaker


class TestScrapeBooks:

    def test_append_valid_item_adds_to_list_and_categories(self) -> None:
        # arrange
        books = ScrapeBooks()
        book = ScrapeBookFaker.fake(category="Sci-Fi")

        # act
        books.append(book)

        # assert
        assert len(books) == 1
        assert books[0] is book
        assert books.categories == {"Sci-Fi"}

    def test_append_multiple_books_updates_categories(self) -> None:
        # arrange
        books = ScrapeBooks()

        # act
        sci = ScrapeBookFaker.fake(category="Sci-Fi")
        drama = ScrapeBookFaker.fake(category="Drama")

        books.append(sci)
        books.append(drama)
        books.append(ScrapeBookFaker.fake(category="Sci-Fi"))

        # assert
        assert len(books) == 3
        assert books.categories == {"Sci-Fi", "Drama"}

    def test_append_invalid_type_raises_typeerror(self) -> None:
        # arrange
        books = ScrapeBooks()

        # act - assert
        with pytest.raises(TypeError) as exec_info:
            books.append(cast(Any, "not-a-book"))
        assert "Only allowed add ScrapeBook instance" in str(exec_info.value)

    def test_inherits_list_behavior(self) -> None:
        # arrange
        books = ScrapeBooks()

        # act
        first = ScrapeBookFaker.fake(title="First")
        second = ScrapeBookFaker.fake(title="Second")

        books.append(first)
        books.append(second)

        # assert
        assert books[0].title == "First"
        assert [b.title for b in books] == ["First", "Second"]
        assert first in books
        assert ScrapeBookFaker.fake(title="Other") not in books

    def test_get_book_by_id_and_return_book_when_found(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        # act
        book = books.get_by_id(books[1].id)

        # assert
        assert book == books[1]

    def test_get_book_by_id_and_return_none_when_not_found(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())
        books.append(ScrapeBookFaker.fake())

        # act
        book = books.get_by_id(books[-1].id + 172)

        # assert
        assert book is None

    def test_list_books_by_category_or_title(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake(title="Title 0", category="1"))
        books.append(ScrapeBookFaker.fake(title="Title 1", category="1"))
        books.append(ScrapeBookFaker.fake(title="Title 2", category="1"))
        books.append(ScrapeBookFaker.fake(title="Title 3", category="2"))
        books.append(ScrapeBookFaker.fake(title="Title 4", category="2"))
        books.append(ScrapeBookFaker.fake(title="Title 5", category="3"))

        # act
        result_all_books_when_empty_title_and_category = books.list_books_by_category_or_title()
        result_all_books_in_category_1 = books.list_books_by_category_or_title(category="1")
        result_all_books_in_category_2 = books.list_books_by_category_or_title(category="2")
        result_all_books_in_category_3 = books.list_books_by_category_or_title(category="3")
        result_book_in_title_0 = books.list_books_by_category_or_title(title="Title 0")
        result_book_in_title_1 = books.list_books_by_category_or_title(title="Title 1")
        result_book_in_title_2 = books.list_books_by_category_or_title(title="Title 2")
        result_book_in_title_1_category_1 = books.list_books_by_category_or_title(title="Title 1", category="1")
        result_book_in_title_3_category_2 = books.list_books_by_category_or_title(title="Title 3", category="2")
        result_book_in_title_5_category_3 = books.list_books_by_category_or_title(title="Title 5", category="3")
        result_empty_when_not_found_books_in_category = books.list_books_by_category_or_title(category="Not Exist")
        result_empty_when_not_found_books_in_title = books.list_books_by_category_or_title(title="Not Exist")
        result_empty_when_mismatch_title_and_category = books.list_books_by_category_or_title(title="Title 0",
                                                                                              category="3")

        # assert
        assert result_all_books_when_empty_title_and_category == [books[0], books[1], books[2], books[3], books[4],
                                                                  books[5]]
        assert result_all_books_in_category_1 == [books[0], books[1], books[2]]
        assert result_all_books_in_category_2 == [books[3], books[4]]
        assert result_all_books_in_category_3 == [books[5]]
        assert result_book_in_title_0 == [books[0]]
        assert result_book_in_title_1 == [books[1]]
        assert result_book_in_title_2 == [books[2]]
        assert result_book_in_title_1_category_1 == [books[1]]
        assert result_book_in_title_3_category_2 == [books[3]]
        assert result_book_in_title_5_category_3 == [books[5]]
        assert result_empty_when_not_found_books_in_category == []
        assert result_empty_when_not_found_books_in_title == []
        assert result_empty_when_mismatch_title_and_category == []

    def test_get_stats_book_successfully(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake(price_full=Money.from_float(10), rating=Rating(1)))
        books.append(ScrapeBookFaker.fake(price_full=Money.from_float(20), rating=Rating(3)))
        books.append(ScrapeBookFaker.fake(price_full=Money.from_float(30), rating=Rating(3)))
        books.append(ScrapeBookFaker.fake(price_full=Money.from_float(40), rating=Rating(3)))
        books.append(ScrapeBookFaker.fake(price_full=Money.from_float(50), rating=Rating(5)))
        books.append(ScrapeBookFaker.fake(price_full=Money.from_float(60), rating=Rating(5)))

        # act
        book_stats = books.get_stats_books()

        # assert
        assert book_stats.total_books == 6
        assert book_stats.avg_price == Decimal(35)
        assert book_stats.rating_distribution == {1: 1, 3: 3, 5: 2}

    def test_get_stats_book_with_empty_books_successfully(self) -> None:
        # arrange
        books = ScrapeBooks()

        # act
        book_stats = books.get_stats_books()

        # assert
        assert book_stats.total_books == 0
        assert book_stats.avg_price == Decimal(0)
        assert book_stats.rating_distribution == {}

    def test_get_stats_books_by_category_successfully(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake(category="1", price_full=Money.from_float(10), rating=Rating(1)))
        books.append(ScrapeBookFaker.fake(category="1", price_full=Money.from_float(20), rating=Rating(3)))
        books.append(ScrapeBookFaker.fake(category="1", price_full=Money.from_float(30), rating=Rating(3)))
        books.append(ScrapeBookFaker.fake(category="2", price_full=Money.from_float(40), rating=Rating(3)))
        books.append(ScrapeBookFaker.fake(category="2", price_full=Money.from_float(50), rating=Rating(5)))
        books.append(ScrapeBookFaker.fake(category="3", price_full=Money.from_float(60), rating=Rating(5)))
        books.append(ScrapeBookFaker.fake(category="4", price_full=Money.from_float(60), rating=Rating(5)))

        # act
        book_stats_category = books.get_stats_books_by_category()

        # assert
        assert book_stats_category == {
            "1": BookStats(3, Decimal(20), {1: 1, 3: 2}),
            "2": BookStats(2, Decimal(45), {3: 1, 5: 1}),
            "3": BookStats(1, Decimal(60), {5: 1}),
            "4": BookStats(1, Decimal(60), {5: 1})
        }

    def test_get_stats_books_by_category_with_empty_books_successfully(self) -> None:
        # arrange
        books = ScrapeBooks()

        # act
        book_stats_category = books.get_stats_books_by_category()

        # assert
        assert book_stats_category == {}

    def test_list_top_rated_books(self) -> None:
        # arrange
        books = ScrapeBooks()
        books.append(ScrapeBookFaker.fake(model_id=1, category="1", price_full=Money.from_float(10), rating=Rating(1)))
        books.append(ScrapeBookFaker.fake(model_id=2, category="1", price_full=Money.from_float(20), rating=Rating(5)))
        books.append(ScrapeBookFaker.fake(model_id=3, category="1", price_full=Money.from_float(30), rating=Rating(3)))
        books.append(ScrapeBookFaker.fake(model_id=4, category="2", price_full=Money.from_float(40), rating=Rating(4)))
        books.append(ScrapeBookFaker.fake(model_id=5, category="2", price_full=Money.from_float(50), rating=Rating(4)))
        books.append(ScrapeBookFaker.fake(model_id=6, category="3", price_full=Money.from_float(60), rating=Rating(3)))

        # act
        top_rated_books = books.list_top_rated_books(limit=4)

        # assert
        assert top_rated_books == [books[1], books[3], books[4], books[2]]

    def test_list_top_rated_books_with_empty_books_successfully(self) -> None:
        # arrange
        books = ScrapeBooks()

        # act
        top_rated_books = books.list_top_rated_books(limit=4)

        # assert
        assert top_rated_books == []
