# tests/helpers/strict_mock.py
from __future__ import annotations

import inspect
from collections.abc import Iterable
from typing import Any, NoReturn, TypeVar, overload, cast
from unittest.mock import Mock, AsyncMock

from pytest_mock import MockerFixture

from src.standard.built_in.Static import Static

T = TypeVar("T")


class StrictMock(Static):
    @staticmethod
    def _raise_unconfigured(name: str) -> NoReturn:
        raise AssertionError(
            f"Mock '{name}' was called without explicitly configured "
            f"(define .side_effect in test)."
        )

    @classmethod
    @overload
    def make_strict_mock(
        cls, spec: type[T], *, allow: Iterable[str] = (), mocker: MockerFixture
    ) -> T: ...

    @classmethod
    @overload
    def make_strict_mock(
        cls,
        spec: T,
        *,
        allow: Iterable[str] = (),
        mocker: MockerFixture,
    ) -> T: ...

    @classmethod
    def make_strict_mock(
        cls, spec: type[T] | T, *, allow: Iterable[str] = (), mocker: MockerFixture
    ) -> T:
        is_instance: bool = not isinstance(spec, type)

        base_mock: Mock = cast(
            Mock, mocker.create_autospec(spec, spec_set=True, instance=is_instance)
        )

        names: set[str] = set()
        inspect_targets: list[Any] = [spec, type(spec)] if is_instance else [spec]
        for target in inspect_targets:
            for name, attr in inspect.getmembers(target):
                if name.startswith("_"):
                    continue
                if callable(attr):
                    names.add(name)

        allow_set: set[str] = set(allow)

        for name in names:
            if name in allow_set:
                continue
            try:
                sub = getattr(base_mock, name)
            except AttributeError:
                continue
            if isinstance(sub, Mock):
                sub.side_effect = lambda *a, _n=name, **kw: cls._raise_unconfigured(_n)

        return cast(T, base_mock)

    @classmethod
    def make_async_strict_mock(cls) -> AsyncMock:
        async_mock = AsyncMock()
        async_mock.side_effect = lambda *a, **kw: cls._raise_unconfigured("async_mock")
        return async_mock
