from __future__ import annotations

from abc import ABC, ABCMeta
from typing import Any, cast, Self


class _AbstractMeta(ABCMeta):
    def __new__(mcs, name: str, bases: tuple[type, ...], ns: dict[str, Any]) -> Any:
        cls = super().__new__(mcs, name, bases, ns)

        if cls.__dict__.get("__is_abstract_root__", False):
            return cls

        if any(base.__dict__.get("__is_abstract_root__", False) for base in bases):
            setattr(cls, "__is_direct_child_of_abstract__", True)

        return cls

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls.__dict__.get("__is_abstract_root__", False):
            raise TypeError(f"{cls.__name__} is abstract and cannot be instantiated.")

        if cls.__dict__.get("__is_direct_child_of_abstract__", False):
            raise TypeError(
                f"{cls.__name__} directly inherits from Abstract and cannot be instantiated."
            )

        return super().__call__(*args, **kwargs)


class Abstract(metaclass=_AbstractMeta):
    __is_abstract_root__ = True
