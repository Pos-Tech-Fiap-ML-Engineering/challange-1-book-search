from __future__ import annotations
import pathlib
import pytest
from _pytest.config import Config
from _pytest.nodes import Item

UNIT_DIR: pathlib.Path = pathlib.Path(__file__).parent / "unit"
INTEGRATION_DIR: pathlib.Path = pathlib.Path(__file__).parent / "integration"
E2E_DIR: pathlib.Path = pathlib.Path(__file__).parent / "e2e"


@pytest.hookimpl()
def pytest_collection_modifyitems(config: Config, items: list[Item]) -> None:
    """
    Pytest hook called immediately after collecting tests.
    It allows you to modify the list of collected tests (items):
    - add/remove tests
    - reorder
    - add tags

    Here we use it to auto-tag tests based on the directory they are in.
    """
    for item in items:
        path: pathlib.Path = pathlib.Path(str(item.fspath))
        if UNIT_DIR in path.parents:
            item.add_marker(pytest.mark.unit)
        elif INTEGRATION_DIR in path.parents:
            item.add_marker(pytest.mark.integration)
        elif E2E_DIR in path.parents:
            item.add_marker(pytest.mark.e2e)