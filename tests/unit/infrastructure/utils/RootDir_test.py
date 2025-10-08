from __future__ import annotations

from pathlib import Path
import pytest

from src.infrastructure.utils.RootDir import RootDir


class TestRootDir:

    def test_find_root_when_filename_in_same_dir_as_file_parent(self, tmp_path: Path) -> None:
        # arrange - act
        proj: Path = tmp_path / "proj"
        pkg: Path = proj / "pkg"
        pkg.mkdir(parents=True, exist_ok=True)

        (pkg / "pyproject.toml").write_text("[tool]\n", encoding="utf-8")

        fake_file: Path = pkg / "module.py"

        found: Path = RootDir.find_root_by_file_name(filename="pyproject.toml", file=str(fake_file))

        # assert
        assert found == pkg

    def test_find_root_when_filename_is_in_parent_dir(self, tmp_path: Path) -> None:
        # arrange - act
        proj: Path = tmp_path / "proj"
        pkg: Path = proj / "pkg"
        mod: Path = pkg / "mod"
        mod.mkdir(parents=True, exist_ok=True)

        (pkg / "pyproject.toml").write_text("[tool]\n", encoding="utf-8")

        fake_file: Path = mod / "module.py"
        found: Path = RootDir.find_root_by_file_name(filename="pyproject.toml", file=str(fake_file))

        # assert
        assert found == pkg

    def test_find_root_picks_nearest_ancestor(self, tmp_path: Path) -> None:
        # arrange - act
        proj: Path = tmp_path / "proj"
        pkg: Path = proj / "pkg"
        mod: Path = pkg / "mod"
        mod.mkdir(parents=True, exist_ok=True)

        (proj / "pyproject.toml").write_text("root\n", encoding="utf-8")
        (pkg / "pyproject.toml").write_text("near\n", encoding="utf-8")

        fake_file: Path = mod / "module.py"

        found: Path = RootDir.find_root_by_file_name(filename="pyproject.toml", file=str(fake_file))

        # assert
        assert found == pkg

    def test_find_root_with_custom_filename(self, tmp_path: Path) -> None:
        # arrange - act
        base: Path = tmp_path / "base" / "src"
        base.mkdir(parents=True, exist_ok=True)

        (base / "custom.cfg").write_text("ok=1\n", encoding="utf-8")
        fake_file: Path = base / "anything.py"

        found: Path = RootDir.find_root_by_file_name(filename="custom.cfg", file=str(fake_file))

        # assert
        assert found == base

    def test_raise_when_filename_not_found(self, tmp_path: Path) -> None:
        # arrange - act
        deep: Path = tmp_path / "a" / "b" / "c"
        deep.mkdir(parents=True, exist_ok=True)
        fake_file: Path = deep / "nope.py"

        with pytest.raises(FileNotFoundError) as exc:
            RootDir.find_root_by_file_name(filename="missing.file", file=str(fake_file))

        # assert
        msg: str = str(exc.value)
        assert "missing.file" in msg

    def test_lru_cache_returns_same_object_instance_for_same_args(self, tmp_path: Path) -> None:
        # arrange - act
        base: Path = tmp_path / "proj"
        base.mkdir(parents=True, exist_ok=True)
        (base / "pyproject.toml").write_text("x\n", encoding="utf-8")

        fake_file: Path = base / "mod.py"

        p1: Path = RootDir.find_root_by_file_name(filename="pyproject.toml", file=str(fake_file))
        p2: Path = RootDir.find_root_by_file_name(filename="pyproject.toml", file=str(fake_file))

        # assert
        assert p1 is p2
        assert p1 == base
