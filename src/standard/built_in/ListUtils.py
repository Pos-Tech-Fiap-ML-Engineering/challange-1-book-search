from typing import TypeVar

from src.standard.built_in.Static import Static

TInput = TypeVar("TInput", bound=object)


class ListUtils(Static):

    @staticmethod
    def last(lst: list[TInput], default: TInput | None = None, /) -> TInput | None:
        return lst[-1] if lst else default
