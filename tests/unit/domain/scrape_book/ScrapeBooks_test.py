from __future__ import annotations

from typing import Any, cast

import pytest

from src.domain.scrape_book.ScrapeBooks import ScrapeBooks
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
