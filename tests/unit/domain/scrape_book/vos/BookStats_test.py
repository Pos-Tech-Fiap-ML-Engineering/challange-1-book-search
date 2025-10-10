from decimal import Decimal

from src.domain.scrape_book.vos.BookStats import BookStats


class TestBookStats:
    def test_initialize_book_stats(self) -> None:
        # arrange - act
        book_stats = BookStats(6, Decimal(5), {1: 5, 4: 3, 2: 7})

        # assert
        assert book_stats.total_books == 6
        assert book_stats.avg_price == Decimal(5)
        assert book_stats.rating_distribution == {1: 5, 4: 3, 2: 7}

    def test_parse_book_stats_to_dict(self) -> None:
        # arrange
        book_stats = BookStats(6, Decimal(5), {1: 5, 4: 3, 2: 7})

        # act
        result = book_stats.to_dict()

        # assert
        assert result == {
            "total_books": book_stats.total_books,
            "avg_price": book_stats.avg_price,
            "rating_distribution": book_stats.rating_distribution,
        }
