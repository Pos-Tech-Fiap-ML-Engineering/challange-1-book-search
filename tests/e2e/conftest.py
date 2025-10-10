import json
from collections.abc import AsyncIterator
from functools import lru_cache
from pathlib import Path
from typing import Any, cast

import httpx
import pytest
import pytest_asyncio
from _pytest.fixtures import FixtureRequest

from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository
from src.infrastructure.domain.scrape_book.ScrapeBookRepositoryImpl import ScrapeBookRepositoryImpl
from src.infrastructure.utils.RootDir import RootDir
from tests.e2e.utils.E2EBootstrapConfigs import E2EBootstrapConfigs
from tests.e2e.utils.E2EHttpAuth import BasicAuthenticationTokenProvider, E2EHttpAuth


def _infra_path() -> Path:
    return RootDir.find_root_by_file_name().joinpath("infra.dev.json")


@lru_cache(maxsize=1)
def _load_infra() -> dict[str, Any]:
    p = _infra_path()
    with p.open("r", encoding="utf-8") as f:
        return cast(dict[str, Any], json.load(f))


@pytest.fixture(scope="session", autouse=True)
def bootstrap(request: FixtureRequest) -> E2EBootstrapConfigs:
    json_file_loaded = _load_infra()

    e2e_configs = E2EBootstrapConfigs(
        json_file_loaded["alb_service_url"]["value"], "admin", "admin"
    )

    return e2e_configs


@pytest.fixture(scope="session")
def token_provider(bootstrap: E2EBootstrapConfigs) -> BasicAuthenticationTokenProvider:
    return BasicAuthenticationTokenProvider(
        bootstrap.service_token_username, bootstrap.service_token_password
    )


@pytest_asyncio.fixture(scope="function")
async def http_client(
    bootstrap: E2EBootstrapConfigs, token_provider: BasicAuthenticationTokenProvider
) -> AsyncIterator[httpx.AsyncClient]:
    headers: httpx.Headers = httpx.Headers()

    timeout = httpx.Timeout(connect=5.0, read=15.0, write=10.0, pool=5.0)

    async with httpx.AsyncClient(
        base_url=bootstrap.service_url,
        timeout=timeout,
        follow_redirects=True,
        headers=headers,
        verify=True,
        limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
        auth=E2EHttpAuth(token_provider),
    ) as http_client:
        yield http_client


@pytest_asyncio.fixture(scope="function")
async def scrape_book_repository() -> ScrapeBookRepository:
    return ScrapeBookRepositoryImpl(
        root_dir=RootDir.find_root_by_file_name(filename="conftest.py", file=__file__)
        / "data"
        / "expected_books.csv"
    )
