from pathlib import Path

from src.standard.built_in.Static import Static


class UtilsTest(Static):

    @staticmethod
    def find_root_by_file_name(filename: str = "pyproject.toml") -> Path:
        current = Path(__file__).resolve()
        for parent in [current, *current.parents]:
            candidate = parent.joinpath(filename)
            if candidate.exists():
                return parent

        raise FileNotFoundError(f"Can't find {filename} in {current}")

