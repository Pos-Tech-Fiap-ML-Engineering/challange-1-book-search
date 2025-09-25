from typing import Any, Tuple, Dict, TypeVar

T = TypeVar("T", bound=type)


class Static(type):
    def __new__(cls: type[T], *args: Tuple, **kwargs: Dict[str, Any]) -> T:
        raise TypeError('Static classes cannot be instantiated')
