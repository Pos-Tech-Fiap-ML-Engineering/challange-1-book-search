from __future__ import annotations

from abc import ABC
from typing import Any, cast, Self


class Abstract(ABC):

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls is Abstract:
            raise TypeError(f"{Abstract.__name__} is an interface/Base class and cannot be instantiated directly.")
        return super().__new__(cls)
