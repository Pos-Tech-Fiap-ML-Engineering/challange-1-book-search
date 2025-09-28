from enum import Enum, StrEnum, IntEnum
from typing import TypeVar

from src.standard.built_in.Static import Static

E = TypeVar("E", bound=Enum)


class CustomAsserts(Static):
    @staticmethod
    def assert_enum(enum_cls: type[E], names: list[str], values: list[str | int]) -> None:
        assert issubclass(enum_cls, StrEnum) or issubclass(enum_cls, IntEnum)

        enum_cls_names = [m.name for m in enum_cls]
        enum_cls_values = [m.value for m in enum_cls]

        assert names == enum_cls_names
        assert values == enum_cls_values
