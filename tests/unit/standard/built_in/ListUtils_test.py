from __future__ import annotations

from dataclasses import dataclass

import pytest

from src.standard.built_in.ListUtils import ListUtils


@dataclass(frozen=True)
class Thing:
    id: int


class TestListUtils:
    def test_last_returns_last_element_ints(self) -> None:
        # arrange - act
        xs: list[int] = [1, 2, 3]
        got: int | None = ListUtils.last(xs)

        # assert
        assert got == 3

    def test_last_returns_last_element_strings_even_if_falsy(self) -> None:
        # arrange - act
        xs: list[str] = ["a", "", "c"]
        got: str | None = ListUtils.last(xs)

        # assert
        assert got == "c"

    def test_last_on_singleton_list(self) -> None:
        # arrange - act
        xs: list[int] = [42]
        got: int | None = ListUtils.last(xs)

        # assert
        assert got == 42

    def test_last_empty_with_default_returns_default(self) -> None:
        # arrange - act
        xs: list[int] = []
        default: int = 999
        got: int | None = ListUtils.last(xs, default)

        # assert
        assert got == 999

    def test_last_empty_without_default_returns_none(self) -> None:
        # arrange - act
        xs: list[str] = []
        got: str | None = ListUtils.last(xs)

        # assert
        assert got is None

    def test_last_preserves_type_with_custom_objects(self) -> None:
        # arrange - act
        xs: list[Thing] = [Thing(1), Thing(2)]
        got: Thing | None = ListUtils.last(xs)

        # assert
        assert isinstance(got, Thing)
        assert got is not None and got.id == 2

    def test_last_empty_with_custom_default(self) -> None:
        # arrange - act
        xs: list[Thing] = []
        default: Thing = Thing(0)
        got: Thing | None = ListUtils.last(xs, default)

        # assert
        assert got == default

    def test_positional_only_parameter_enforced(self) -> None:
        # arrange - act - assert
        with pytest.raises(TypeError):
            _ = ListUtils.last(lst=[1, 2, 3])  # type: ignore[call-arg]
