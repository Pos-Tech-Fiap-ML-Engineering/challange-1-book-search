from typing import Any, TypeVar

T = TypeVar("T", bound=type)


class Static(type):
    def __new__(cls: type[T], *args: tuple, **kwargs: dict[str, Any]) -> T:
        raise TypeError("Static classes cannot be instantiated")
