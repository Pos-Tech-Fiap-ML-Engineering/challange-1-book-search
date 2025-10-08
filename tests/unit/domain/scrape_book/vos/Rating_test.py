import pytest

from src.domain.scrape_book.vos.Rating import Rating


class TestRating:
    @pytest.mark.parametrize("value", [1, 2, 3, 4, 5, "5"])
    def test_initialize_rating_successfully(self, value: int | str) -> None:
        # arrange - act
        rating = Rating(value)  # type: ignore

        # assert
        assert rating == int(value)

    @pytest.mark.parametrize("value", [-1, 0, 6, 7])
    def test_raise_when_invalid_rating(self, value: int) -> None:
        # arrange - act - assert
        with pytest.raises(ValueError, match="Rating must be between 1 and 5."):
            Rating(value)
