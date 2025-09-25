from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, cast, AsyncIterator

import httpx
import pytest
from _pytest.config import Config
from _pytest.fixtures import FixtureRequest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from filelock import FileLock
from httpx import AsyncClient, ASGITransport

from src.api.AppBuilder import AppBuilder

INFRA_DIR = Path(f"{Path(__file__).parent}/pytest_tmp")
INFRA_DIR.mkdir(exist_ok=True)

STATE_TEST_FILE_PATH = INFRA_DIR / "state-test.json"
STATE_WORKERS_FILE_PATH = INFRA_DIR / "state-workers.json"
LOCK_FILE_PATH = INFRA_DIR / ".lock"

MASTER_WORKER_ID: list[str] = ["gw0", "master"]
bootstrapped_workers_env: str = "bootstrapped_workers"
bootstrapped_workers_count_env: str = "workers_count"


def _safe_write_json(path: Path, data: dict[str, Any]) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False))
    os.replace(tmp, path)  # atomic write


def _safe_read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text()) if path.exists() else {}


@pytest.fixture(scope="session", autouse=True)
def bootstrap(request: FixtureRequest, worker_id: str) -> dict[str, str]:
    data: dict[str, str] = {}
    worker_count: int = int(os.environ.get("PYTEST_XDIST_WORKER_COUNT", "1"))

    print(f"[PRINT] pid={os.getpid()} worker={worker_id}", file=sys.stderr, flush=True)

    with FileLock(LOCK_FILE_PATH, timeout=60):
        data = _safe_read_json(STATE_TEST_FILE_PATH)
        if not data:
            state_workers = _safe_read_json(STATE_WORKERS_FILE_PATH)
            state_workers[bootstrapped_workers_env] = 0
            state_workers[bootstrapped_workers_count_env] = worker_count
            _safe_write_json(STATE_WORKERS_FILE_PATH, state_workers)

            # here it will load containers and etc...
            _safe_write_json(STATE_TEST_FILE_PATH, data)

    return data


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    with FileLock(LOCK_FILE_PATH, timeout=60):
        state_workers = _safe_read_json(STATE_WORKERS_FILE_PATH)
        state_workers[bootstrapped_workers_env] = cast(int, state_workers.get(bootstrapped_workers_env)) + 1
        _safe_write_json(STATE_WORKERS_FILE_PATH, state_workers)
        print(
            f"[PRINT] current workers {state_workers[bootstrapped_workers_env]} quantity workers {state_workers[bootstrapped_workers_count_env]}",
            file=sys.stderr, flush=True)
        if state_workers[bootstrapped_workers_env] == state_workers[bootstrapped_workers_count_env]:
            _session_teardown(session.config)
            _cleanup_files()


def _session_teardown(config: Config) -> None:
    try:
        # here it will clean containers and etc...
        ...
    finally:
        ...


def _cleanup_files() -> None:
    for p in (STATE_TEST_FILE_PATH, STATE_WORKERS_FILE_PATH):
        if p.exists():
            p.unlink(missing_ok=True)


@pytest.fixture(scope="function")
async def app_builder() -> AsyncIterator[AppBuilder]:
    app_builder = AppBuilder()
    yield app_builder


@pytest.fixture(scope="function")
async def fast_api(app_builder: AppBuilder) -> AsyncIterator[FastAPI]:
    yield app_builder.build_fast_api_server()


@pytest.fixture(scope="function")
async def http_client(fast_api: FastAPI) -> AsyncIterator[httpx.AsyncClient]:
    async with LifespanManager(fast_api):
        transport = ASGITransport(app=fast_api)
        async with AsyncClient(transport=transport, base_url="http://testserver") as http_client:
            yield http_client
