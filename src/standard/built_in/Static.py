from typing import Self, Any, Tuple, Dict


class Static(type):
    def __new__(cls: type[Self], *args: Tuple, **kwargs: Dict[str, Any]) -> Self:
        raise TypeError('Static classes cannot be instantiated')
