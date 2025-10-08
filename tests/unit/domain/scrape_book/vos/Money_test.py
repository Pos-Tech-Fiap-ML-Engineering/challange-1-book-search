from decimal import Decimal

import pytest

from src.domain.scrape_book.vos.Money import Money


class TestMoney:

    @pytest.mark.parametrize("value", [0, 10])
    def test_initialize_default_money_successfully(self, value: int) -> None:
        # arrange - act
        money = Money(Decimal(value))

        # assert
        assert money.amount == value
        assert money.currency == "GBP"

    def test_initialize_money_with_all_params_successfully(self) -> None:
        # arrange - act
        money = Money(Decimal(5), currency="BR")

        # assert
        assert money.amount == 5
        assert money.currency == "BR"

    def test_initialize_money_from_float(self) -> None:
        # arrange - act
        money = Money.from_float(1.5)

        # assert
        assert money.amount == 1.5
        assert money.currency == "GBP"

    def test_initialize_money_from_float_all_params(self) -> None:
        # arrange - act
        money = Money.from_float(1.5, "BR")

        # assert
        assert money.amount == 1.5
        assert money.currency == "BR"

    def test_initialize_money_from_string(self) -> None:
        # arrange - act
        money = Money.from_string("4.5")

        # assert
        assert money.amount == 4.5
        assert money.currency == "GBP"

    def test_initialize_money_from_string_all_params(self) -> None:
        # arrange - act
        money = Money.from_string("5.5", "BR")

        # assert
        assert money.amount == 5.5
        assert money.currency == "BR"

    def test_raise_exception_when_money_is_negative(self) -> None:
        # arrange - act - assert
        with pytest.raises(ValueError, match="Money cannot be negative"):
            Money(Decimal(-1))
