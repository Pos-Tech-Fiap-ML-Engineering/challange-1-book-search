from __future__ import annotations

import pytest
import httpx
from httpx import AsyncClient, Timeout, Limits

from src.infrastructure.application.boundaries.factory.HttpClientFactoryImpl import (
    HttpClientFactoryImpl,
)


class TestHttpClientFactoryImpl:
    @pytest.mark.asyncio
    async def test_create_async_factory_sets_base_url_timeout_and_custom_limits(self) -> None:
        # arrange - act
        factory = HttpClientFactoryImpl()

        base_url = "https://example.com/api/"
        timeout = Timeout(connect=5.0, read=15.0, write=10.0, pool=5.0)
        limits = Limits(max_connections=20, max_keepalive_connections=10)

        client: AsyncClient = factory.create_async_factory(
            base_url=base_url,
            timeout=timeout,
            limits=limits,
        )

        # assert
        try:
            assert isinstance(client, httpx.AsyncClient)
            assert str(client.base_url) == base_url
            assert isinstance(client.timeout, Timeout)
            assert client.timeout.connect == timeout.connect
            assert client.timeout.read == timeout.read
            assert client.timeout.write == timeout.write
            assert client.timeout.pool == timeout.pool
        finally:
            await client.aclose()

    @pytest.mark.asyncio
    async def test_create_async_factory_uses_default_limits_when_none(self) -> None:
        # arrange - act
        factory = HttpClientFactoryImpl()

        base_url = "https://example.org"
        timeout = Timeout(10.0)  # simples: mesmo valor para todos os timeouts

        client: AsyncClient = factory.create_async_factory(
            base_url=base_url,
            timeout=timeout,
            limits=None,  # <- o ponto do teste
        )

        # assert
        try:
            assert str(client.base_url) == base_url
            assert isinstance(client.timeout, Timeout)
            assert client.timeout.connect == timeout.connect
            assert client.timeout.read == timeout.read
            assert client.timeout.write == timeout.write
            assert client.timeout.pool == timeout.pool

        finally:
            await client.aclose()
