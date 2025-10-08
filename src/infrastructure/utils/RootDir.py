import functools
from pathlib import Path

from src.standard.built_in.Static import Static


class RootDir(Static):

    @staticmethod
    @functools.cache
    def find_root_by_file_name(filename: str = "pyproject.toml", file: str = __file__) -> Path:
        current = Path(file).resolve()
        for parent in [current, *current.parents]:
            candidate = parent.joinpath(filename)
            if candidate.exists():
                return parent

        raise FileNotFoundError(f"Can't find {filename} in {current}")
