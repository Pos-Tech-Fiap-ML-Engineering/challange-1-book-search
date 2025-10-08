from typing import Self


class Rating(int):
    __slots__ = ()

    def __new__(cls, value: int) -> Self:
        if not isinstance(value, int):
            value = int(value)

        if value not in (1, 2, 3, 4, 5):
            raise ValueError("Rating must be between 1 and 5.")

        return super().__new__(cls, value)
