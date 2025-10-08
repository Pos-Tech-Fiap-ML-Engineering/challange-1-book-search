from __future__ import annotations

import re
from contextlib import nullcontext as does_not_raise, AbstractContextManager
from dataclasses import FrozenInstanceError

import pytest

from src.domain.scrape_book.vos.Upc import Upc


class TestUpc:
    @pytest.mark.parametrize(
        "value, expectation",
        [
            ("A1B2C3", does_not_raise()),
            ("abc123XYZ", does_not_raise()),
            ("0", does_not_raise()),
            ("Z", does_not_raise()),
            ("1234567890", does_not_raise()),
            ("ABCdef", does_not_raise()),
        ],
    )
    def test_upc_valid_values(
        self, value: str, expectation: AbstractContextManager[object]
    ) -> None:
        with expectation:
            u = Upc(value=value)
            assert u.value == value
            assert re.fullmatch(r"[A-Za-z0-9]+", u.value)

    @pytest.mark.parametrize(
        "value",
        [
            "with-dash",
            "space ",
            " space",
            "ABC 123",
            "abc_",  # underscore não permitido
            "áéíóú",  # acentos
            "中文",  # unicode não alfanum LATIN
            "123-456",
            "12.3",
            "",
            " ",
            "\n",
            "abc*",
            "a/b",
            "a:b",
        ],
    )
    def test_upc_invalid_values_raise(self, value: str) -> None:
        # arrange - act -assert
        with pytest.raises(ValueError) as exc:
            Upc(value=value)
        assert "Upc invalid" in str(exc.value)

    def test_upc_is_frozen_immutable(self) -> None:
        # arrange
        u = Upc("ABC123")

        # act -assert
        with pytest.raises(FrozenInstanceError):
            # noinspection PyDataclass
            u.value = "XYZ789"  # type: ignore # type: ignore[attr-defined]

    def test_upc_equality_and_hash(self) -> None:
        # arrange - act
        a = Upc("ABC123")
        b = Upc("ABC123")
        c = Upc("XYZ789")

        # assert
        assert a == b
        assert hash(a) == hash(b)
        assert a != c
        assert hash(a) != hash(c)

    def test_upc_repr_contains_class_and_field(self) -> None:
        # arrange - act
        u = Upc("ABC123")
        r = repr(u)

        # assert
        assert "Upc" in r
        assert "value='ABC123'" in r
